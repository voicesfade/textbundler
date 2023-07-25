import os

BROWSER_NAME = "Google Chrome"
TB_PATH = os.path.expanduser("~")  # User's home directory
# TB_PATH = os.path.expanduser(
#     "~/Library/Mobile%20Documents/com~apple~CloudDocs"
# )  # User's iCloud directory
TB_DIR = ".textbundles"
TB_INFO = {
    "id": None,
    "type": None,
    "path": None,
    "date_created": None,
    "date_updated": None,
}
TB_CATEGORIES = [
    "task",
    "meeting",
    "project",
    "note",
]
