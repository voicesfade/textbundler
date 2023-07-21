import os

BROWSER_NAME = "Google Chrome"
TB_PATH = os.path.expanduser("~")  # User's home directory
# TB_PATH = os.path.expanduser(
#     "~/Library/Mobile%20Documents/com~apple~CloudDocs"
# )  # User's iCloud directory
TB_DIR = ".textbundles"
TB_TYPES = ["task", "project", "meeting", "note"]
TB_INFO = {
    "id": None,
    "type": None,
    "path": None,
    "date_created": None,
    "date_updated": None,
}
TB_FRONTMATTER = {
    "status": None,
    "priority": None,
    "due": None,
    "link": None,
    "archive": False,
}
