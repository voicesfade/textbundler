import json
from datetime import datetime, timedelta
from config import TB_PATH, TB_DIR


def get_bundle():
    success = None
    while success is not True:
        response = input("\nEnter textbundle id: ")
        try:
            with open(f"{TB_PATH}/{TB_DIR}/{response}/info.json") as f:
                bundle_info = json.loads(f.read())
            success = True
        except:
            success = False
    return bundle_info


def archive_bundle(bundle_info):
    response = None
    while response not in {"y", "n"}:
        response = input("\nArchive (y,n): ")
    if response == "y":
        bundle_info["archive"] = True
        bundle_id = bundle_info["id"]
        print(f"\n'{bundle_id}' is archived.")
    if response == "n":
        bundle_info["archive"] = False
        bundle_id = bundle_info["id"]
        print(f"\n'{bundle_id}' is not archived.")
    return bundle_info


def priority_bundle(bundle_info):
    response = None
    while response not in {"high", "medium", "low"}:
        response = input("\nPriority (high,medium,low): ")
    bundle_info["priority"] = response
    bundle_id = bundle_info["id"]
    print(f"\n{bundle_id}'s priority is {response}.")
    return bundle_info


def date_picker():
    response = None
    while response not in {"1", "2", "3", "4", "5", "6", "7"}:
        response = input("\nHow many days from today (1-7): ")
    timestamp = datetime.now()
    td = timedelta(days=4)
    future_timestamp = timestamp + td
    return future_timestamp.astimezone().replace(microsecond=0).isoformat()


def date_due(bundle_info):
    timestamp = date_picker()
    bundle_info["date_due"] = timestamp
    bundle_id = bundle_info["id"]
    print(f"\n{bundle_id}'s due date is {timestamp}.")
    return bundle_info


def update_bundle(bundle_info):
    timestamp = datetime.now().astimezone().replace(microsecond=0).isoformat()
    bundle_info["date_updated"] = timestamp
    bundle_id = bundle_info["id"]
    with open(f"{TB_PATH}/{TB_DIR}/{bundle_id}/info.json", "w") as f:
        f.write(json.dumps(bundle_info, indent=4))


def main():
    bundle_info = get_bundle()
    bundle_info = archive_bundle(bundle_info)
    bundle_info = priority_bundle(bundle_info)
    bundle_info = date_due(bundle_info)
    update_bundle(bundle_info)


if __name__ == "__main__":
    main()
