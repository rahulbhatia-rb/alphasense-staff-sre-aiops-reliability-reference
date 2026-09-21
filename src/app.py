import json,sys
from src.readiness import Service,assess
for l in sys.stdin:
 if l.strip():print(json.dumps(assess(Service.from_dict(json.loads(l)))))
