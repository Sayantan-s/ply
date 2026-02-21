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
    PARSING = "warming_up"  # was PARSING
    QUEUED = "lining_up"  # was QUEUED
    PROCESSING = "churning"  # was PROCESSING
    EXTRACTING = "combing"  # was EXTRACTING
    ANALYZING = "pondering"  # was ANALYZING
    THINKING = "cooking"  # was THINKING
    MATCHED = "locked_in"  # was MATCHED
    FAILED = "fumbled"  # was FAILED
