import argparse
from pathlib import Path
import os
import uuid
import json
import datetime
from config import TB_PATH, TB_DIR, TB_INFO
from index import index


def init():
    tb_path = os.path.join(TB_PATH, TB_DIR)
    Path(tb_path).mkdir(parents=True, exist_ok=True)
    return "Success"


def create_dir():
    name = uuid.uuid4().hex
    path = os.path.join(TB_PATH, TB_DIR, name)
    Path(path).mkdir(parents=True, exist_ok=True)
    return name


def create_text(dir, title, category):
    path = f"{TB_PATH}/{TB_DIR}/{dir}"
    today = datetime.datetime.now()
    month = today.strftime("%b").lower()
    day = today.strftime("%d")
    with open(f"{path}/text.markdown", "w") as f:
        note = f"""# {title}

[Index]({TB_PATH}/{TB_DIR}/index.markdown#{category}) | [Edit](vscode://file{path}/?windowId=_blank)

```yaml
id: {dir}
category: {category}
status: open
due: null
priority: new
jira: null
archive: false
```
"""
        f.write(note)
    return "Success"


def create_info(dir, timestamp):
    info = TB_INFO
    info["id"] = dir
    info["path"] = f"{TB_DIR}/{dir}"
    info["date_created"] = timestamp
    path = f"{TB_PATH}/{TB_DIR}/{dir}"
    with open(f"{path}/info.json", "w") as f:
        note = json.dumps(info, indent=4)
        f.write(note)
    return "Success"


def create_assets(dir):
    path = os.path.join(TB_PATH, TB_DIR, dir, "assets")
    Path(path).mkdir(parents=True, exist_ok=True)
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
        "--category",
        default="note",
        help=f"Provide a category",
        type=str,
    )
    args = parser.parse_args()
    title = args.title.strip()
    category = args.category.strip()
    init()
    dir = create_dir()
    create_text(dir, title, category)
    create_info(dir, timestamp)
    create_assets(dir)
    os.system(f"/usr/local/bin/code -n {TB_PATH}/{TB_DIR}/{dir}/text.markdown")
    # os.system(f"open -a '{BROWSER_NAME}' {TB_PATH}/{TB_DIR}/{dir}/text.markdown")
    index()
    # os.system(f"/usr/local/bin/code {TB_PATH}/{TB_DIR}/{dir} -n")
    return "Success"


if __name__ == "__main__":
    main()
