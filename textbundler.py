import argparse
from pathlib import Path
import os
import uuid
import json
import datetime
from config import BROWSER_NAME, TB_PATH, TB_DIR, TB_INFO, TB_TYPES
import index


def init():
    tb_path = os.path.join(TB_PATH, TB_DIR)
    Path(tb_path).mkdir(parents=True, exist_ok=True)
    return "Success"


def create_dir():
    bundle_name = uuid.uuid4().hex
    bundle_path = os.path.join(TB_PATH, TB_DIR, bundle_name)
    Path(bundle_path).mkdir(parents=True, exist_ok=True)
    return bundle_name


def create_text(bundle_dir, bundle_title, bundle_type):
    bundle_path = f"{TB_PATH}/{TB_DIR}/{bundle_dir}"
    with open(f"{bundle_path}/text.markdown", "w") as f:
        note = f"""# {bundle_title}

[{bundle_type.title()}s]({TB_PATH}/{TB_DIR}/index.markdown#{bundle_type}) | [Edit](vscode://file{bundle_path}/?windowId=_blank)

```yaml
status: null
due: null
priority: null
jira: null
archive: false
```
"""
        f.write(note)
    return "Success"


def create_info(bundle_dir, timestamp, bundle_type):
    info_data = TB_INFO
    info_data["id"] = bundle_dir
    info_data["type"] = bundle_type
    info_data["path"] = f"{TB_DIR}/{bundle_dir}"
    info_data["date_created"] = timestamp
    info_data["date_updated"] = timestamp
    bundle_path = f"{TB_PATH}/{TB_DIR}/{bundle_dir}"
    with open(f"{bundle_path}/info.json", "w") as f:
        note = json.dumps(info_data, indent=4)
        f.write(note)
    return "Success"


def create_assets(bundle_dir):
    bundle_path = os.path.join(TB_PATH, TB_DIR, bundle_dir, "assets")
    Path(bundle_path).mkdir(parents=True, exist_ok=True)
    return "Success"


def main():
    timestamp = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--title",
        default=f"{timestamp}",
        help="Provide a title.",
        type=str,
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=TB_TYPES,
        help=f"Provide the type of note:{str(TB_TYPES)}",
        type=str,
    )
    args = parser.parse_args()
    bundle_title = args.title
    bundle_type = args.type
    init()
    bundle_dir = create_dir()
    create_text(bundle_dir, bundle_title, bundle_type)
    create_info(bundle_dir, timestamp, bundle_type)
    create_assets(bundle_dir)
    os.system(f"open -a '{BROWSER_NAME}' {TB_PATH}/{TB_DIR}/{bundle_dir}/text.markdown")
    # os.system(f"/usr/local/bin/code {TB_PATH}/{TB_DIR}/{bundle_dir} -n")
    return "Success"


if __name__ == "__main__":
    main()
