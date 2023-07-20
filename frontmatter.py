import os
import pathlib
import json
from config import BROWSER_NAME, TB_PATH, TB_DIR, TB_TYPES, TB_FRONTMATTER


def get_frontmatter(tb_dir):
    with open(f"{tb_dir}/text.markdown", "r") as file:
        lines = file.readlines()
    data = None
    yaml = False
    for line in lines:
        if yaml == True:
            data = TB_FRONTMATTER
            if ":" in line:
                f_type = line[0 : line.index(":")]
                if f_type in list(TB_FRONTMATTER.keys()):
                    TB_FRONTMATTER[f_type] = line.replace(f"{f_type}: ", "").strip()
        if line.startswith("```yaml"):
            yaml = True
            continue
        if line.startswith("```") and yaml == True:
            return data
    return data


def update_title(tb_dir, frontmatter):
    with open(f"{tb_dir}/text.markdown", "r") as file:
        lines = file.readlines()
    title = lines[0].strip()
    if "[" in title:
        title = title[0 : title.index("[")]
    for f_key, f_value in frontmatter.items():
        if f_key == "due" and f_value != "null":
            title += f"[{f_key}: {f_value}]"
        if f_key == "priority" and f_value != "null":
            title += f"[{f_key}: {f_value}]"
    lines[0] = f"{title}\n"
    with open(f"{tb_dir}/text.markdown", "w") as file:
        file.writelines(lines)


def main():
    tb_path = pathlib.Path(f"{TB_PATH}/{TB_DIR}")
    for tb_dir in tb_path.iterdir():
        if os.path.isdir(tb_dir):
            frontmatter = get_frontmatter(tb_dir)
            if frontmatter != None:
                update_title(tb_dir, frontmatter)


if __name__ == "__main__":
    main()
