import os

BROWSER_NAME = "Google Chrome"
TB_PATH = os.path.expanduser("~")
TB_DIR = ".textbundles"
TB_TYPES = ["task", "project", "meeting", "note"]
TB_INFO = {
    "id": None,
    "type": None,
    "path": None,
    "date_created": None,
    "date_updated": None,
    "date_scheduled": None,
    "date_due": None,
    "tags": [],
    "archive": False,
    "priority": None,
}
