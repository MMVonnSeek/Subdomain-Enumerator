import json
from subenum.passive import PassiveCollector
def test_crtsh_monkeypatch(monkeypatch):
    # Replace requests.get to return controlled data
    class DummyResp:
        def __init__(self, jsondata):
            self._json = jsondata
        def raise_for_status(self): pass
        def json(self): return self._json
    def fake_get(url, params=None, timeout=5):
        data = [{'name_value': 'www.example.com'}, {'name_value': 'api.example.com\nmail.example.com'}]
        return DummyResp(data)
    monkeypatch.setattr('subenum.passive.requests.get', fake_get)
    p = PassiveCollector()
    out = p.from_crtsh('example.com')
    assert 'www.example.com' in out
    assert 'api.example.com' in out
