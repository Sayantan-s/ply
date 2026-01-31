from enum import Enum

GDRIVE_PATTERN = (
    r"(?:drive|docs)\.google\.com\/(?:file\/d|document\/d)\/([a-zA-Z0-9_-]+)"
)
DROPBOX_PATTERN = r"dropbox\.com\/s(?:h)?\/([a-zA-Z0-9_-]+)"

SUPPORTED_TYPES = [
    "application/pdf",
    "application/octet-stream",
    "officedocument",
    "msword",
]

DEFAULT_FILENAME = "downloaded_resume.pdf"


class JdMatchStatus(Enum):
    PARSING = "parsing"
    QUEUED = "queued"
    PROCESSING = "processing"
    EXTRACTING = "extracting"
    ANALYZING = "analyzing"
    THINKING = "thinking"
    MATCHED = "matched"
    FAILED = "failed"
