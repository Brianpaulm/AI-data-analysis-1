import os

MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
TEMP_STORAGE_PATH = os.getenv("TEMP_STORAGE_PATH", "/tmp/secure_dashboard")
HASH_ALGORITHM = "sha256"
