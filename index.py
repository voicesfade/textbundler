import os
import json
import pathlib
from config import TB_PATH, TB_DIR, TB_TYPES


def get_type(tb_dir):
    with open(f"{tb_dir}/info.json", "r") as file:
        data = json.loads(file.read())
    if "type" in data:
        return data["type"]
    else:
        return "unknown"


def get_id(tb_dir):
    with open(f"{tb_dir}/info.json", "r") as file:
        data = json.loads(file.read())
    if "id" in data:
        return data["id"]
    else:
        return "unknown"


def get_tb_data(the_dir):
    data = {
        "type": get_type(the_dir),
        "id": get_id(the_dir),
    }
    with open(f"{the_dir}/text.markdown", "r") as file:
        lines = file.readlines()
    data["title"] = lines[0].replace("# ", "")
    yaml = False
    for line in lines:
        if yaml == True:
            if ":" in line:
                yaml_key = line[0 : line.index(":")]
                yaml_value = line.replace(f"{yaml_key}: ", "").strip()
                if yaml_value == "true":
                    data[yaml_key] = True
                if yaml_value == "false":
                    data[yaml_key] = False
                else:
                    data[yaml_key] = yaml_value
        if line.startswith("```yaml"):
            yaml = True
            continue
        if line.startswith("```") and yaml == True:
            return data
    return data


def create_index(the_data):
    content = "# Index\n"
    the_types = {}
    for tb_type in TB_TYPES:
        the_types[tb_type] = []
    for item in the_data:
        if "archive" in item:
            if item["archive"] == False:
                the_types[item["type"]].append(item)
        else:
            the_types[item["type"]].append(item)
    for type_key, type_value in the_types.items():
        content += f"\n## {type_key.title()}s\n\n"
        for bundle in type_value:
            bundle_id = bundle["id"]
            bundle_title = bundle["title"]
            bundle_priority = str()
            bundle_due = str()
            if "priority" in bundle:
                if bundle["priority"] != "null":
                    bundle_priority = bundle["priority"]
                    bundle_priority = f"**{bundle_priority.title()}** |"
            if "due" in bundle:
                if bundle["due"] != "null":
                    bundle_due = bundle["due"].title()
                    bundle_due = f"**{bundle_due.title()}** |"
            content += f"* [{bundle_title}]({TB_PATH}/{TB_DIR}/{bundle_id}/text.markdown) | {bundle_priority} {bundle_due} [Edit](vscode://file{TB_PATH}/{TB_DIR}/{bundle_id}/?windowId=_blank)\n"
    index_path = f"{TB_PATH}/{TB_DIR}"
    with open(f"{index_path}/index.markdown", "w") as f:
        f.write(content)
    return "Success"


def index():
    the_path = pathlib.Path(f"{TB_PATH}/{TB_DIR}")
    the_data = []
    for the_dir in the_path.iterdir():
        if os.path.isdir(the_dir):
            the_data.append(get_tb_data(the_dir))
    create_index(the_data)


if __name__ == "__main__":
    index()
