import os
import pathlib
from config import TB_PATH, TB_DIR
import json


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


def create_index(data):
    content = "# Index\n"
    categories = {}
    for item in data:
        if "archive" in item:
            if item["archive"] == False:
                if "category" in item:
                    if item["category"] not in categories:
                        categories[item["category"]] = []
                    categories[item["category"]].append(item)
    for cat_key, cat_val in categories.items():
        content += f"\n## {cat_key.title()}s\n\n"
        for tb in cat_val:
            tb_id = tb["id"]
            tb_title = tb["title"]
            tb_priority = str()
            tb_due = str()
            if "priority" in tb:
                if tb["priority"] != None:
                    tb_priority = tb["priority"]
                    tb_priority = f"**{tb_priority.title()}** |"
            if "due" in tb:
                if tb["due"] != None:
                    tb_due = tb["due"].title()
                    tb_due = f"**{tb_due.title()}** |"
            content += f"* [{tb_title}]({TB_PATH}/{TB_DIR}/{tb_id}/text.markdown) | {tb_priority} {tb_due} [Edit](vscode://file{TB_PATH}/{TB_DIR}/{tb_id}/?windowId=_blank)\n"
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
