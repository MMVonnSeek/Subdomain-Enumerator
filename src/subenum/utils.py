from __future__ import annotations
from pathlib import Path
from typing import List, Iterable, Dict, Any
import logging, json, csv, random, time

logger = logging.getLogger(__name__)

def load_wordlist(path: Path) -> List[str]:
    if not path.exists():
        raise FileNotFoundError(f"Wordlist not found: {path}")
    with path.open('r', encoding='utf-8', errors='ignore') as fh:
        words = [line.strip() for line in fh if line.strip() and not line.startswith('#')]
    return words

def configure_logging(level: str = 'INFO') -> None:
    import logging, sys, json
    class JsonFormatter(logging.Formatter):
        def format(self, record):
            d = {'time': self.formatTime(record), 'level': record.levelname, 'name': record.name, 'msg': record.getMessage()}
            return json.dumps(d)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    root.handlers = [handler]

def save_json(path: Path, data: Any) -> None:
    with path.open('w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)

def save_csv(path: Path, records: Iterable[Dict[str, Any]]) -> None:
    records = list(records)
    if not records: return
    keys = sorted({k for r in records for k in r.keys()})
    with path.open('w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=keys)
        writer.writeheader()
        writer.writerows(records)

def random_subdomain(domain: str) -> str:
    return f"{random.randint(1000000,9999999)}.{domain}"

def epoch_ms() -> int:
    return int(time.time() * 1000)
