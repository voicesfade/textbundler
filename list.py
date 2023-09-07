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


def main():
    path = pathlib.Path(f"{TB_PATH}/{TB_DIR}")
    os.system("clear")
    for dir in path.iterdir():
        if os.path.isdir(dir):
            frontmatter = get_frontmatter(dir)
            if frontmatter["due"] != None:
                due = due_date(frontmatter["due"])
                if due == True and frontmatter["archive"] == False:
                    print(
                        frontmatter["title"]
                        + "\n--> "
                        + str(path)
                        + "/"
                        + frontmatter["id"]
                        + "\n"
                    )


if __name__ == "__main__":
    main()
