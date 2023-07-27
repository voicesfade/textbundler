import os
import pathlib
from config import TB_PATH, TB_DIR, TB_CATEGORIES
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
        return f'<span style="color:orangered">{priority.title()}</span>'
    elif priority == "medium":
        return f'<span style="color:sandybrown">{priority.title()}</span>'
    elif priority == "low":
        return f'<span style="color:plum">{priority.title()}</span>'
    elif priority == "new":
        return f'<span style="color:mediumpurple">{priority.title()}✨</span>'
    else:
        return f"{priority.title()}"


def is_archived(data):
    if "archive" in data:
        if data["archive"] == True:
            return True
    return False


def get_date():
    today = datetime.datetime.now()
    month = today.strftime("%b").lower()
    day = today.strftime("%d")
    return f"{month} {day}"


def due_date(due):
    t = datetime.datetime.now()
    t_month = t.strftime("%b").lower()
    t_day = int(t.strftime("%d"))
    try:
        month = due[0:3]
        day = int(due[4:7])
    except:
        return False
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
    if month not in months:
        return False
    days = list(range(1, 32))
    if day not in days:
        return False
    if month == t_month:
        if t_day >= day:
            return True
        else:
            return False
    elif months.index(month) < months.index(t_month):
        return True
    else:
        return False


def format_bullet(bullet):
    tb_title = bullet["title"]
    tb_id = bullet["id"]
    line = []
    line.append(f"\n* [{tb_title}]({TB_PATH}/{TB_DIR}/{tb_id}/text.markdown)")
    line.append(f"[Edit](vscode://file{TB_PATH}/{TB_DIR}/{tb_id}/?windowId=_blank)")
    if "priority" in bullet:
        if bullet["priority"] != None:
            line.append(f'{priority_color(bullet["priority"])}')
        if "due" in bullet:
            if bullet["due"] != None:
                tb_due = bullet["due"]
                if due_date(bullet["due"]):
                    line.append(
                        f'<span style="color:orangered">{tb_due.title()}</span>'
                    )
                else:
                    line.append(
                        f'<span style="color:mediumseagreen">{tb_due.title()}</span>'
                    )
    return " | ".join(line)


def due(data):
    bullets = []
    for item in data:
        if is_archived(item) == False:
            if "due" in item:
                if item["due"] != None:
                    if due_date(item["due"]) == True:
                        bullets.append(format_bullet(item))
    return "\n".join(bullets)


def high_priority(data):
    bullets = []
    for item in data:
        if is_archived(item) == False:
            if "priority" in item:
                if item["priority"] == "high":
                    bullets.append(format_bullet(item))
    return "\n".join(bullets)


def category(data, category):
    bullets = []
    for item in data:
        if is_archived(item) == False:
            if "category" in item:
                if item["category"] == category:
                    bullets.append(format_bullet(item))
    return "\n".join(bullets)


def other(data):
    bullets = []
    for item in data:
        if is_archived(item) == False:
            if "category" in item:
                if item["category"] not in TB_CATEGORIES:
                    bullets.append(format_bullet(item))
    return "\n".join(bullets)


def create_index(data):
    page = f"""# Index

[Edit](vscode://file{TB_PATH}/{TB_DIR}/?windowId=_blank)

## Due/Overdue
{due(data)}

## High Priority
{high_priority(data)}

## Tasks
{category(data, "task")}

## Meetings
{category(data, "meeting")}

## Projects
{category(data, "project")}

## Notes
{category(data, "note")}

## Other
{other(data)}

"""
    index_path = f"{TB_PATH}/{TB_DIR}"
    with open(f"{index_path}/index.markdown", "w") as f:
        f.write(page)


def index():
    path = pathlib.Path(f"{TB_PATH}/{TB_DIR}")
    data = []
    for dir in path.iterdir():
        if os.path.isdir(dir):
            data.append(get_frontmatter(dir))
    create_index(data)


if __name__ == "__main__":
    index()
