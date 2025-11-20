from subenum.dns_client import DNSClient
def test_query_example():
    d = DNSClient(timeout=2.0, doh=True)
    ips, cnames = d.query_a('example.com')
    assert isinstance(ips, list)
    assert isinstance(cnames, list)
