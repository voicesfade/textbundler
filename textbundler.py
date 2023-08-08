import argparse
from pathlib import Path
import os
import uuid
import json
import datetime
from config import TB_PATH, TB_DIR, TB_INFO
from index import index
import sys


def init():
    tb_path = os.path.join(TB_PATH, TB_DIR)
    Path(tb_path).mkdir(parents=True, exist_ok=True)
    return "Success"


def user_input():
    today = datetime.datetime.now()
    month = today.strftime("%b").lower()
    day = today.strftime("%d")
    title = str()
    category = str()
    status = str()
    due = str()
    priority = str()
    try:
        while len(title) == 0:
            title = input("\nTitle: ").strip()

        while len(category) == 0:
            print(
                """
Categories: 
(t) Task
(m) Meeting
(p) Project
(n) Note
        """
            )
            response = input("Category: ")
            if response == "t":
                category = "task"
            elif response == "m":
                category = "meeting"
            elif response == "p":
                category = "project"
            elif response == "n":
                category = "note"

        while len(status) == 0:
            print(
                """
Status: 
(o) Open
(p) In Progress
(r) In Review
(b) Blocked
(c) Closed
        """
            )
            response = input("Status: ")
            if response == "o":
                status = "open"
            elif response == "p":
                status = "in progress"
            elif response == "r":
                status = "in review"
            elif response == "b":
                status = "blocked"
            elif response == "c":
                status = "closed"

        while due == str():
            response = input("\nDue today (y/n): ")
            if response == "y":
                due = f"{month} {day}"
            elif response == "n":
                due = None

        while len(priority) == 0:
            print(
                """
Priorities:
(n) New
(h) High
(m) Medium
(l) Low
    """
            )
            response = input("Priority: ")
            if response == "n":
                priority = "new"
            elif response == "h":
                priority = "high"
            elif response == "m":
                priority = "medium"
            elif response == "l":
                priority = "low"
    except:
        sys.exit(print("\n\nExiting..."))

    data = {
        "title": title,
        "category": category,
        "status": status,
        "due": due,
        "priority": priority,
    }

    return data


def create_dir():
    name = uuid.uuid4().hex
    path = os.path.join(TB_PATH, TB_DIR, name)
    Path(path).mkdir(parents=True, exist_ok=True)
    return name


def create_text(dir, data):
    path = f"{TB_PATH}/{TB_DIR}/{dir}"
    title = data["title"]
    category = data["category"]
    status = data["status"]
    due = data["due"]
    priority = data["priority"]

    with open(f"{path}/text.markdown", "w") as f:
        note = f"""# {title}

[Index]({TB_PATH}/{TB_DIR}/index.markdown#{category}) | [Edit](vscode://file{path}/?windowId=_blank)

```yaml
id: {dir}
category: {category}
status: {status}
due: {due}
priority: {priority}
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
        default=None,
        help="Provide a title.",
        type=str,
    )
    parser.add_argument(
        "--category",
        default=None,
        help=f"Provide a category",
        type=str,
    )
    args = parser.parse_args()
    title = args.title
    category = args.category
    init()
    dir = create_dir()
    if title == None and category == None:
        data = user_input()
        create_text(dir, data)
    else:
        data = {
            "title": title.strip(),
            "category": category.strip(),
            "status": "open",
            "due": None,
            "priority": None,
        }
        create_text(dir, data)
    create_info(dir, timestamp)
    create_assets(dir)
    os.system(f"/usr/local/bin/code -n {TB_PATH}/{TB_DIR}/{dir}/text.markdown")
    # os.system(f"open -a '{BROWSER_NAME}' {TB_PATH}/{TB_DIR}/{dir}/text.markdown")
    index()
    # os.system(f"/usr/local/bin/code {TB_PATH}/{TB_DIR}/{dir} -n")
    return "Success"


if __name__ == "__main__":
    main()
