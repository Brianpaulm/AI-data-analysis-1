import logging
import json
from datetime import datetime

class AuditLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        self.logger.addHandler(handler)

    def log(self, event_type: str, details: dict):
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "details": details,
        }
        self.logger.info(json.dumps(record))
