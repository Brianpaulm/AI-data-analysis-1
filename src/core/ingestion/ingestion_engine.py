from core.ingestion.file_intelligence import detect_mime
from core.logging.logger import AuditLogger

logger = AuditLogger("ingestion")

class IngestionEngine:
    def ingest(self, path: str):
        mime = detect_mime(path)
        logger.log("file_ingested", {"path": path, "mime": mime})
        return {"path": path, "mime": mime}
