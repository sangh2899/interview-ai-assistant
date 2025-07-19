import json

import config
from study_planner import create_study_plan, create_fast_study_plan

if __name__ == "__main__":
    obj = study_plan = create_fast_study_plan(config.test_jd)
    print(json.dumps(obj, indent=4))