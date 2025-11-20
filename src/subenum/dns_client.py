from __future__ import annotations
import dns.resolver, dns.exception
from typing import List, Tuple, Optional
import logging, requests

logger = logging.getLogger(__name__)

class DNSClient:
    """DNS resolver supporting dnspython (system resolver) and optional DoH via Cloudflare/Google."""
    def __init__(self, timeout: float = 3.0, nameservers: Optional[List[str]] = None, doh: bool = True):
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = timeout
        self.resolver.lifetime = timeout
        if nameservers:
            self.resolver.nameservers = nameservers
        self.timeout = timeout
        self.use_doh = doh

    def _doh_query(self, name: str, qtype: str = 'A') -> Tuple[List[str], List[str]]:
        # Using Cloudflare DoH JSON endpoint for simplicity
        ips, cnames = [], []
        try:
            params = {'name': name, 'type': qtype}
            headers = {'Accept': 'application/dns-json'}
            r = requests.get('https://cloudflare-dns.com/dns-query', params=params, headers=headers, timeout=self.timeout)
            r.raise_for_status()
            data = r.json()
            for ans in data.get('Answer', []):
                if ans.get('type') in (1, 28):  # A or AAAA
                    ips.append(ans.get('data'))
                elif ans.get('type') == 5:  # CNAME
                    cn = ans.get('data').rstrip('.')
                    cnames.append(cn)
        except Exception as e:
            logger.debug('DoH query failed for %s: %s', name, e)
        return ips, cnames

    def query_a(self, name: str) -> Tuple[List[str], List[str]]:
        ips, cnames = [], []
        # Try system resolver first
        try:
            answers = self.resolver.resolve(name, 'A')
            for r in answers:
                ips.append(r.address)
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            pass
        except dns.exception.Timeout:
            logger.debug('Timeout A for %s', name)
        except Exception as e:
            logger.debug('Resolver error A for %s: %s', name, e)

        # CNAME
        try:
            answers = self.resolver.resolve(name, 'CNAME')
            for r in answers:
                cnames.append(str(r.target).rstrip('.'))
        except Exception:
            pass

        # AAAA
        try:
            answers = self.resolver.resolve(name, 'AAAA')
            for r in answers:
                ips.append(r.address)
        except Exception:
            pass

        # Fallback to DoH if nothing found and configured
        if self.use_doh and not ips and not cnames:
            d_ips, d_cnames = self._doh_query(name, 'A')
            ips.extend(d_ips)
            cnames.extend(d_cnames)

        return ips, cnames
