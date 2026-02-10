from core.ingestion.file_intelligence import detect_mime

def test_detect_mime():
    assert detect_mime("example.csv") in (
        "text/csv",
        "application/octet-stream",
    )
