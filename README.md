# pdf-docraptor-mini

A minimal Python (Poetry) project that generates a PDF from an HTML file using the **DocRaptor** Python client.

This repo is intentionally tiny so you can:

- drop in some HTML (e.g., a NOFO exported page)
- run a single command (`poetry run dr`)
- get a PDF written to `pdf/nofo.pdf`

An example NOFO is provided in `html/nofo.html`, so this repo works out of the box. If you want to print out a different NOFO, follow the instructions below: [Locally print a NOFO from simpler.nofos.grants.gov](https://github.com/pcraig3/pdf-docraptor-mini?tab=readme-ov-file#locally-print-a-nofo-from-simplernofosgrantsgov)

## Requirements

- Python **3.14**
- Poetry
- A DocRaptor API key

## Setup

1. Install dependencies:

```bash
poetry install
```

2. Create a local `.env` file from the example:

```bash
cp .env.example .env
```

3. Edit `.env` and set your DocRaptor key:

```
# .env
DOCRAPTOR_API_KEY=YOUR_API_KEY
```

4. Run the script

```bash
poetry run dr
```

- Input HTML: `html/nofo.html`
- Output PDF: `pdf/nofo.pdf`

The script (`src/pdf_docraptor_mini/main.py`) loads env vars from the repo root `.env` file (via python-dotenv).

## Locally print a NOFO from simpler.nofos.grants.gov

DocRaptor renders your HTML on their servers, so any referenced assets (CSS, fonts, images) must be accessible via absolute URLs. A NOFO page copied from the NOFO Builder uses relative asset paths like `"/static/..."`, which won’t resolve for DocRaptor unless you convert them.

1. Find the NOFO you want to test
2. Copy the entire HTML source code of the NOFO
3. Paste it into "/html/nofo.html"
   - At this point, the NOFO cannot print because all the external requests will fail
4. Do a Ctrl+F for `"/static`
5. Grab the URL root and path that includes `/static`
   - For example: `https://nofos.simpler.grants.gov/static`
6. Find+replace all instances of `"/static` for `"https://nofos.simpler.grants.gov/static`

An example NOFO is provided in `html/nofo.html`.

## Notes

- The script currently runs DocRaptor in test mode (`"test": True`), which is free but watermarked.
  - Set `"test"` to `False` for non-watermarked PDFs.
- PDF settings are configured for print output and accessibility profile via Prince options (`"profile": "PDF/UA-1"`).
