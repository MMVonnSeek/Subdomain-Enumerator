from __future__ import annotations
import requests, os, logging, time
from typing import List, Set, Dict, Any, Optional

logger = logging.getLogger(__name__)

class PassiveCollector:
    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout
        self.seen: Set[str] = set()

    def from_crtsh(self, domain: str) -> List[str]:
        """Query crt.sh JSON output for certificates matching domain."""
        out = set()
        try:
            q = f"%25.{domain}"
            url = 'https://crt.sh/'
            params = {'q': q, 'output': 'json'}
            r = requests.get(url, params=params, timeout=self.timeout)
            r.raise_for_status()
            data = r.json()
            for entry in data:
                name = entry.get('name_value')
                if not name:
                    continue
                # name_value may contain multiple hostnames separated by \n
                for n in str(name).split('\n'):
                    n = n.strip().lower()
                    if n.endswith('.'):
                        n = n[:-1]
                    if n.endswith(domain):
                        out.add(n)
        except Exception as e:
            logger.debug('crt.sh query failed: %s', e)
        return sorted(out)

    def from_securitytrails(self, domain: str, api_key: Optional[str]=None) -> List[str]:
        out = set()
        if not api_key:
            logger.debug('No SecurityTrails API key provided; skipping')
            return []
        try:
            url = f'https://api.securitytrails.com/v1/domain/{domain}/subdomains'
            headers = {'APIKEY': api_key}
            r = requests.get(url, headers=headers, timeout=self.timeout)
            r.raise_for_status()
            data = r.json()
            for s in data.get('subdomains', []):
                out.add(f"{s}.{domain}")
        except Exception as e:
            logger.debug('SecurityTrails query failed: %s', e)
        return sorted(out)

    def from_shodan(self, domain: str, api_key: Optional[str]=None) -> List[str]:
        out = set()
        if not api_key:
            logger.debug('No Shodan API key provided; skipping')
            return []
        try:
            url = 'https://api.shodan.io/dns/domain/' + domain
            params = {'key': api_key}
            r = requests.get(url, params=params, timeout=self.timeout)
            r.raise_for_status()
            data = r.json()
            for s in data.get('subdomains', []):
                out.add(f"{s}.{domain}")
        except Exception as e:
            logger.debug('Shodan query failed: %s', e)
        return sorted(out)
