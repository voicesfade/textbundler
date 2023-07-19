import os
import json
from config import BROWSER_NAME, TB_PATH, TB_DIR, TB_TYPES


def get_bundle_data():
    bundle_data = []
    for subdir, dirs, files in os.walk(f"{TB_PATH}/{TB_DIR}"):
        for file in files:
            file_path = os.path.join(subdir, file)
            if file == "info.json":
                with open(file_path) as f:
                    info = json.loads(f.read())
                bundle_data.append(info)
    return bundle_data


def add_bundle_title(bundle_data):
    for bundle in bundle_data:
        bundle_id = bundle["id"]
        with open(f"{TB_PATH}/{TB_DIR}/{bundle_id}/text.markdown") as f:
            title = f.readline().strip().replace("# ", "")
        bundle["title"] = title
    return bundle_data


def create_index(bundle_data):
    content = "# Index\n"
    bundle_types = {}
    for bundle_type in TB_TYPES:
        bundle_types[bundle_type] = []
    for bundle in bundle_data:
        bundle_types[bundle["type"]].append(bundle)
    for type_key, type_value in bundle_types.items():
        content += f"\n## {type_key.title()}s\n\n"
        for bundle in type_value:
            if bundle["archive"] == False:
                bundle_title = bundle["title"]
                bundle_id = bundle["id"]
                content += f"* [{bundle_title.title()}]({TB_PATH}/{TB_DIR}/{bundle_id}/text.markdown)\n"
    index_path = f"{TB_PATH}/{TB_DIR}"
    with open(f"{index_path}/index.markdown", "w") as f:
        f.write(content)
    return "Success"


def main():
    bundle_data = get_bundle_data()
    bundle_data = add_bundle_title(bundle_data)
    create_index(bundle_data)
    os.system(f"open -a '{BROWSER_NAME}' {TB_PATH}/{TB_DIR}/index.markdown")


if __name__ == "__main__":
    main()
