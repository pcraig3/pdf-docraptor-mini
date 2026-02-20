from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


import docraptor


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_PATH = ROOT / "html" / "nofo.html"
OUT_DIR = ROOT / "pdf"
OUT_FILE = OUT_DIR / "nofo.pdf"

load_dotenv(dotenv_path=ROOT / ".env")


def main() -> None:
    DOCRAPTOR_API_KEY = os.getenv("DOCRAPTOR_API_KEY")
    if not DOCRAPTOR_API_KEY:
        raise RuntimeError(
            "Missing DOCRAPTOR_API_KEY. Make sure DOCRAPTOR_API_KEY exists in your .env file."
        )

    html = TEMPLATE_PATH.read_text(encoding="utf-8")

    doc_api = docraptor.DocApi()
    doc_api.api_client.configuration.username = DOCRAPTOR_API_KEY
    doc_api.api_client.configuration.debug = (
        True  # set False if you don't want verbose logging
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    try:
        pdf_bytes = doc_api.create_doc(
            {
                "test": True,  # TRUE = free but watermarked; set False for production
                "document_type": "pdf",
                "name": OUT_FILE.name,
                "document_content": html,
                "pipeline": 11,
                "prince_options": {"media": "print", "profile": "PDF/UA-1"},
            }
        )
    except docraptor.rest.ApiException as err:
        # Helpful error printout
        print(
            f"DocRaptor error: {getattr(err, 'status', None)} {getattr(err, 'reason', '')}"
        )
        raise

    OUT_FILE.write_bytes(bytes(pdf_bytes))
    print(f"Wrote: {OUT_FILE}")
