from __future__ import annotations
import asyncio, logging, time, os, json
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any, Set, Optional
from .dns_client import DNSClient
from .passive import PassiveCollector
from .utils import save_json, save_csv, epoch_ms, random_subdomain
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

logger = logging.getLogger(__name__)

class SubEnumRunner:
    def __init__(self, domain: str, wordlist: List[str], workers: int = 200, timeout: float = 3.0, http_validate: bool = False, use_passive: bool = True):
        self.domain = domain.lower().strip()
        self.wordlist = wordlist
        self.workers = max(1, workers)
        self.timeout = timeout
        self.http_validate = http_validate
        self.use_passive = use_passive
        self.dns = DNSClient(timeout=timeout, doh=True)
        self.passive = PassiveCollector(timeout=timeout)
        self.seen: Set[str] = set()
        self.metrics: Dict[str, Any] = {'start_ms': epoch_ms(), 'queries': 0}

    async def _probe_label(self, label: str, semaphore: asyncio.Semaphore) -> Optional[Dict[str, Any]]:
        candidate = f"{label}.{self.domain}"
        async with semaphore:
            # DNS lookups are blocking (dnspython) so run in threadpool
            loop = asyncio.get_running_loop()
            ips, cnames = await loop.run_in_executor(None, self.dns.query_a, candidate)
            self.metrics['queries'] += 1
            if not ips and not cnames:
                return None
            rec = {'hostname': candidate, 'labels': label, 'ips': ips, 'cnames': cnames}
            if self.http_validate:
                # lightweight HTTP check using requests in threadpool
                def http_probe():
                    import requests
                    try:
                        for scheme in ('https://','http://'):
                            r = requests.head(f"{scheme}{candidate}", timeout=self.timeout, allow_redirects=True)
                            return {'status': r.status_code, 'url': r.url, 'ok': r.status_code < 400}
                    except Exception:
                        return {'status': None, 'url': None, 'ok': False}
                rec['http'] = await loop.run_in_executor(None, http_probe)
            return rec

    async def _bruteforce(self, labels: List[str]) -> List[Dict[str, Any]]:
        semaphore = asyncio.Semaphore(self.workers)
        tasks = [asyncio.create_task(self._probe_label(lbl, semaphore)) for lbl in labels]
        results = []
        for fut in asyncio.as_completed(tasks):
            r = await fut
            if r:
                hn = r['hostname']
                if hn not in self.seen:
                    self.seen.add(hn)
                    results.append(r)
        return results

    def _collect_passive(self) -> List[str]:
        out = set()
        try:
            crt = self.passive.from_crtsh(self.domain)
            out.update(crt)
        except Exception as e:
            logger.debug('crtsh failed: %s', e)
        # SecurityTrails
        st_key = os.environ.get('SECURITRAILS_API_KEY')
        if st_key:
            out.update(self.passive.from_securitytrails(self.domain, api_key=st_key))
        # Shodan
        sh_key = os.environ.get('SHODAN_API_KEY')
        if sh_key:
            out.update(self.passive.from_shodan(self.domain, api_key=sh_key))
        return sorted(out)

    def _wildcard_detect(self) -> bool:
        rnd = random_subdomain(self.domain)
        ips, _ = self.dns.query_a(rnd)
        return bool(ips)

    def run(self) -> Dict[str, Any]:
        logger.info('Starting hybrid enumeration for %s', self.domain)
        start = time.time()
        results: List[Dict[str, Any]] = []
        # Passive collection
        passive_hosts = []
        if self.use_passive:
            passive_hosts = self._collect_passive()
            for p in passive_hosts:
                if p not in self.seen:
                    self.seen.add(p)
                    # lightweight try resolve to enrich
                    ips, cnames = self.dns.query_a(p)
                    results.append({'hostname': p, 'ips': ips, 'cnames': cnames, 'source': 'passive'})
        # Active bruteforce (async)
        wildcard = self._wildcard_detect()
        if wildcard:
            logger.info('Wildcard DNS detected; results will be marked but still returned.')
        # Run async bruteforce
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            bruteforce_res = loop.run_until_complete(self._bruteforce(self.wordlist))
            results.extend([{**r, 'source': 'active'} for r in bruteforce_res])
        finally:
            loop.close()
        # Postprocessing: sort, metrics
        self.metrics['end_ms'] = epoch_ms()
        self.metrics['duration_s'] = (self.metrics['end_ms'] - self.metrics['start_ms']) / 1000.0
        summary = {'domain': self.domain, 'count': len(results), 'metrics': self.metrics}
        # Generate simple HTML dashboard
        dashboard = self._render_html(results, summary)
        report = {'results': results, 'summary': summary, 'dashboard_html': dashboard}
        return report

    def _render_html(self, results: List[Dict[str, Any]], summary: Dict[str, Any]) -> str:
        rows = ''.join([f"<tr><td>{r.get('hostname')}</td><td>{', '.join(r.get('ips',[]))}</td><td>{r.get('source','')}</td></tr>" for r in results])
        html = f"""<!doctype html><html><head><meta charset='utf-8'><title>SubEnum Report - {self.domain}</title></head><body>"><h1>SubEnum Report - {self.domain}</h1><p>Found {summary['count']} entries. Duration: {summary['metrics']['duration_s']}s</p><table border='1'><thead><tr><th>Hostname</th><th>IPs</th><th>Source</th></tr></thead><tbody>{rows}</tbody></table></body></html>"""
        return html

    def save_output(self, path, results):
        p = path
        if str(p).endswith('.csv'):
            save_csv(p, results)
        else:
            save_json(p, results)
