#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path
from subenum.core import SubEnumRunner
from subenum.utils import configure_logging, load_wordlist

def build_parser():
    p = argparse.ArgumentParser(prog='subenum', description='Hybrid Subdomain Enumerator')
    p.add_argument('-d','--domain', required=True, help='Target domain (example.com)')
    p.add_argument('-w','--wordlist', required=True, help='Wordlist path')
    p.add_argument('--workers', type=int, default=200, help='Concurrency (async tasks)')
    p.add_argument('--timeout', type=float, default=3.0, help='Network timeout seconds')
    p.add_argument('--output', type=str, default='results.json', help='Output JSON or CSV file')
    p.add_argument('--dashboard', type=str, default=None, help='Write HTML dashboard to file')
    p.add_argument('--http-validate', action='store_true', help='Validate discovered hosts via HTTP(S)')
    p.add_argument('--no-passive', action='store_true', help='Disable passive sources (crt.sh, SecurityTrails, Shodan)')
    p.add_argument('--log-level', default='INFO', help='Logging level')
    return p

def main(argv=None):
    argv = argv or sys.argv[1:]
    args = build_parser().parse_args(argv)
    configure_logging(args.log_level)
    wordlist = load_wordlist(Path(args.wordlist))
    runner = SubEnumRunner(
        domain=args.domain,
        wordlist=wordlist,
        workers=args.workers,
        timeout=args.timeout,
        http_validate=args.http_validate,
        use_passive=not args.no_passive
    )
    report = runner.run()
    # save outputs
    out = Path(args.output)
    runner.save_output(out, report['results'])
    if args.dashboard and report.get('dashboard_html'):
        Path(args.dashboard).write_text(report['dashboard_html'], encoding='utf-8')
        print(f"Dashboard written to {args.dashboard}")
    print(f"Finished. results saved to {out}")

if __name__ == '__main__':
    main()
