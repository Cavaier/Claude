"""Record what was built in Klaviyo, so the send gate can match it to the approved version.

    python3 tools/record_build.py <campaign-id> <market> <klaviyo-campaign-id> <template-id>

The builder runs this right after uploading out/<market>.html. It stores the hash of the
rendered emails at that moment; scheduling is refused if the approved hash differs.
"""
import sys
import time

import yaml

from common import CAMPAIGNS, gate_hash, load


def main(cid, market, kid, template_id):
    path = CAMPAIGNS / cid / "build.yaml"
    data = load(path) or {"campaign": cid, "markets": {}}
    data["markets"][market] = {"klaviyo_campaign_id": kid, "template_id": template_id,
                               "final_hash": gate_hash(cid, "final"), "built_at": int(time.time())}
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
    print(f"recorded {cid} [{market}] → Klaviyo {kid}, hash {data['markets'][market]['final_hash']}")


if __name__ == "__main__":
    main(*sys.argv[1:5])
