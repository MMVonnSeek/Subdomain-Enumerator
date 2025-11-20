# helper for manual testing of passive collectors
from subenum.passive import PassiveCollector
p = PassiveCollector()
print('crtsh sample:', p.from_crtsh('example.com')[:10])
