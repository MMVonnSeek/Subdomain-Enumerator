from subenum.core import SubEnumRunner
def test_runner_initialization():
    r = SubEnumRunner('example.com', ['a','b'], workers=10)
    assert r.domain == 'example.com'
    assert r.workers == 10
