import mimetypes
from core.logging.logger import AuditLogger

logger = AuditLogger("file_intel")

def detect_mime(path: str) -> str:
    mime, _ = mimetypes.guess_type(path)
    if not mime:
        logger.log("mime_detection_failed", {"path": path})
        return "application/octet-stream"
    logger.log("mime_detected", {"path": path, "mime": mime})
    return mime
