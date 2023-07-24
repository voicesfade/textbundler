import os
import pathlib
from config import TB_PATH, TB_DIR
import datetime


def get_frontmatter(dir):
    data = {}
    with open(f"{dir}/text.markdown", "r") as file:
        lines = file.readlines()
    data["title"] = lines[0].replace("# ", "").strip()
    yaml = False
    for line in lines:
        if yaml == True:
            if ":" in line:
                yaml_key = line[0 : line.index(":")]
                yaml_value = line.replace(f"{yaml_key}: ", "").strip()
                data[yaml_key] = str()
                if yaml_value == "null":
                    data[yaml_key] = None
                elif yaml_value == "true":
                    data[yaml_key] = True
                elif yaml_value == "false":
                    data[yaml_key] = False
                else:
                    data[yaml_key] = yaml_value.strip()
        if line.startswith("```yaml"):
            yaml = True
            continue
        if line.startswith("```") and yaml == True:
            return data
    return data


def priority_color(priority):
    priority = priority.lower()
    if priority == "high":
        return f'<span style="color:red">{priority.title()}</span>'
    elif priority == "medium":
        return f'<span style="color:orange">{priority.title()}</span>'
    elif priority == "low":
        return f'<span style="color:purple">{priority.title()}</span>'
    elif priority == "new":
        return f"✨ **{priority.title()}** ✨"
    else:
        return f"{priority.title()}"


def due_data(due):
    today = datetime.datetime.now()
    months = [
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
    ]
    days = list(range(1, 32))
    due = due.lower()
    month = due[0:3]
    day = due[4:7]
    if len(day) == 1:
        day = "0" + day
    if month in months and int(day) in days:
        if today.strftime("%b").lower() == month and int(today.strftime("%d")) >= int(
            day
        ):
            return f'<span style="color:red">{due.title()}</span>'
        else:
            return f'<span style="color:green">{due.title()}</span>'
    else:
        return due


def create_index(data):
    content = f"""# Index
[Open in VS Code](vscode://file{TB_PATH}/{TB_DIR}/?windowId=_blank)\n
"""
    categories = {}
    for item in data:
        if "archive" in item:
            if item["archive"] == False:
                if "category" in item:
                    if item["category"] not in categories:
                        categories[item["category"]] = []
                    categories[item["category"]].append(item)
    for cat_key, cat_val in categories.items():
        content += f"\n## {cat_key.title()}\n\n"
        for tb in cat_val:
            tb_id = tb["id"]
            tb_title = tb["title"]
            links = [f"* [{tb_title}]({TB_PATH}/{TB_DIR}/{tb_id}/text.markdown)"]
            if "priority" in tb:
                if tb["priority"] != None:
                    links.append(priority_color(tb["priority"]))
            if "due" in tb:
                if tb["due"] != None:
                    links.append(due_data(tb["due"]))
            links.append(
                f"[Edit](vscode://file{TB_PATH}/{TB_DIR}/{tb_id}/?windowId=_blank)\n"
            )
            content += " | ".join(links)
    index_path = f"{TB_PATH}/{TB_DIR}"
    with open(f"{index_path}/index.markdown", "w") as f:
        f.write(content)
    return "Success"


def index():
    path = pathlib.Path(f"{TB_PATH}/{TB_DIR}")
    data = []
    for dir in path.iterdir():
        if os.path.isdir(dir):
            data.append(get_frontmatter(dir))
    create_index(data)


if __name__ == "__main__":
    index()
