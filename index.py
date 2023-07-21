import os
import json
import pathlib
from config import TB_PATH, TB_DIR, TB_TYPES, TB_FRONTMATTER


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


def get_bundle_data(tb_dir):
    with open(f"{tb_dir}/text.markdown", "r") as file:
        lines = file.readlines()
    tb_type = get_type(tb_dir)
    tb_id = get_id(tb_dir)
    title = lines[0].strip()
    data = {
        "title": title,
        "type": tb_type,
        "id": tb_id,
    }
    yaml = False
    for line in lines:
        if yaml == True:
            data = TB_FRONTMATTER
            data["title"] = title.strip()
            data["type"] = tb_type
            data["id"] = tb_id
            if ":" in line:
                f_type = line[0 : line.index(":")]
                if f_type in list(TB_FRONTMATTER.keys()):
                    v = line.replace(f"{f_type}: ", "").strip()
                    if v == "true":
                        TB_FRONTMATTER[f_type] = True
                    if v == "false":
                        TB_FRONTMATTER[f_type] = False
                    else:
                        TB_FRONTMATTER[f_type] = v
        if line.startswith("```yaml"):
            yaml = True
            continue
        if line.startswith("```") and yaml == True:
            return data
    return data


def create_index(bundle_data):
    content = "# Index\n"
    bundle_types = {}
    for bundle_type in TB_TYPES:
        bundle_types[bundle_type] = []
    for bundle in bundle_data:
        if "archive" in bundle:
            if bundle["archive"] == False:
                bundle_types[bundle["type"]].append(bundle)
        else:
            bundle_types[bundle["type"]].append(bundle)
    for type_key, type_value in bundle_types.items():
        content += f"\n## {type_key.title()}s\n\n"
        for bundle in type_value:
            bundle_title = bundle["title"]
            bundle_type = bundle["type"]
            bundle_id = bundle["id"]
            bundle_priority = "No Priority"
            bundle_due = "No Due Date"
            if "priority" in bundle:
                if bundle_priority != None:
                    bundle_priority = bundle["priority"].title()
            if "due" in bundle:
                if bundle_due != None:
                    bundle_due = bundle["due"].title()
            content += f"* [{bundle_title}]({TB_PATH}/{TB_DIR}/{bundle_id}/text.markdown) | {bundle_priority} | {bundle_due} | [Edit](vscode://file{TB_PATH}/{TB_DIR}/{bundle_id}/?windowId=_blank)\n"
    index_path = f"{TB_PATH}/{TB_DIR}"
    with open(f"{index_path}/index.markdown", "w") as f:
        f.write(content)
    return "Success"


def main():
    bundle_data = []
    tb_path = pathlib.Path(f"{TB_PATH}/{TB_DIR}")
    for tb_dir in tb_path.iterdir():
        if os.path.isdir(tb_dir):
            bundle_data.append(get_bundle_data(tb_dir))
    # print(json.dumps(bundle_data, indent=4))
    create_index(bundle_data)
    # os.system(f"open -a '{BROWSER_NAME}' {TB_PATH}/{TB_DIR}/index.markdown")


if __name__ == "__main__":
    main()
