import re
import shutil
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from app.scij import get_full_text
from app.scij_parser import (
    parse_scij_html,
    convert_to_markdown
)


BASE_URL = "https://sinalevi.go.cr"

SCIJ_ID = 25886
LAW_NUMBER = 7557
LAW_TITLE = "Ley General de Aduanas"
INSTITUTION = "Asamblea Legislativa"

CURRENT_FILE = Path(
    "knowledge_base/Ley_General_Aduanas.md"
)

METADATA_FILE = Path(
    "app/document_metadata.py"
)

BACKUP_DIRECTORY = Path(
    "knowledge_base/backups"
)

LATEST_FILE = Path(
    "knowledge_base/Ley_General_Aduanas_latest.md"
)


def get_stored_metadata():
    """
    Read the current SCIJ version from document_metadata.py.
    """

    text = METADATA_FILE.read_text(
        encoding="utf-8"
    )

    version_match = re.search(
        r'"Ley_General_Aduanas\.md":\s*\{.*?"version_number":\s*(\d+)',
        text,
        re.DOTALL
    )

    version_id_match = re.search(
        r'"Ley_General_Aduanas\.md":\s*\{.*?"scij_version_id":\s*(\d+)',
        text,
        re.DOTALL
    )

    if not version_match or not version_id_match:
        raise ValueError(
            "Could not find stored SCIJ version information."
        )

    return {
        "version_number": int(version_match.group(1)),
        "version_id": int(version_id_match.group(1))
    }


def get_latest_version_info(
    id_ficha_norma,
    known_version_id
):
    """
    Find the latest version available in SCIJ.
    """

    url = (
        f"{BASE_URL}/ResultadosNormativa/"
        f"Informacion?param1={id_ficha_norma}"
        f"&param2={known_version_id}"
        f"&param3=1"
    )

    response = requests.get(
        url,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    cantidad_versiones = soup.find(
        "input",
        id="cantidadVersiones"
    )

    if not cantidad_versiones:
        raise ValueError(
            "SCIJ no devolvió la cantidad de versiones."
        )

    latest_version_number = int(
        cantidad_versiones.get("value")
    )

    version_url = (
        f"{BASE_URL}/ResultadosNormativa/"
        "_BuscarVersionNorma"
    )

    data = {
        "idFichaNorma": id_ficha_norma,
        "numeroVersion": latest_version_number
    }

    version_response = requests.post(
        version_url,
        data=data,
        timeout=30
    )

    version_response.raise_for_status()

    version_data = version_response.json()

    return {
        "version_number": latest_version_number,
        "version_id": version_data["idVersionNorma"]
    }


def check_for_update(
    stored_version_number,
    current_version_number
):
    """
    Return True when SCIJ has a newer version.
    """

    return current_version_number > stored_version_number


def validate_markdown_document(
    file_path,
    minimum_articles=300
):
    """
    Perform structural validation of the generated
    legal Markdown document.
    """

    path = Path(file_path)

    if not path.exists():
        print("Validation failed: document does not exist.")
        return False

    text = path.read_text(
        encoding="utf-8"
    )

    articles = re.findall(
        r"^####\s+"
        r"(?:ARTICULO|ARTÍCULO|Artículo|ArtÃ­culo|ArtÃƒÂ­culo)"
        r"\s+\d+",
        text,
        re.MULTILINE
    )

    titles = re.findall(
        r"^##\s+TITULO",
        text,
        re.MULTILINE
    )

    chapters = re.findall(
        r"^###\s+CAPITULO",
        text,
        re.MULTILINE
    )

    print("\n=== DOCUMENT VALIDATION ===")

    print(
        f"Characters: {len(text):,}"
    )

    print(
        f"Articles: {len(articles)}"
    )

    print(
        f"Titles: {len(titles)}"
    )

    print(
        f"Chapters: {len(chapters)}"
    )

    if len(text) < 100_000:
        print(
            "Validation failed: document is suspiciously small."
        )
        return False

    if len(articles) < minimum_articles:
        print(
            "Validation failed: too few article headings."
        )
        return False

    if len(titles) < 5:
        print(
            "Validation failed: too few titles."
        )
        return False

    if len(chapters) < 10:
        print(
            "Validation failed: too few chapters."
        )
        return False

    print("Validation successful.")

    return True


def download_latest_version(
    id_ficha_norma,
    version_id,
    version_number,
    output_file
):
    """
    Download, parse, convert and validate a SCIJ version.
    """

    print("\nDownloading SCIJ document...")

    result = get_full_text(
        id_ficha_norma,
        version_id
    )

    html = result.get("html")

    if not html:
        raise ValueError(
            "SCIJ no devolvió el HTML del documento."
        )

    print(
        f"HTML recibido: {len(html):,} caracteres"
    )

    print("Parsing legal document...")

    lines = parse_scij_html(
        html
    )

    print(
        f"Líneas extraídas: {len(lines):,}"
    )

    metadata = {
        "document_type": "law",
        "law_number": LAW_NUMBER,
        "title": LAW_TITLE,
        "institution": INSTITUTION,
        "source": "SCIJ",
        "scij_id": id_ficha_norma,
        "scij_version_id": version_id,
        "version_number": version_number,
        "status": "vigente"
    }

    markdown = convert_to_markdown(
        lines,
        metadata
    )

    output_path = Path(output_file)

    output_path.write_text(
        markdown,
        encoding="utf-8"
    )

    print(
        f"Markdown generado: {len(markdown):,} caracteres"
    )

    print(
        f"Archivo creado: {output_path}"
    )

    return validate_markdown_document(
        output_path
    )


def replace_document(
    new_file,
    current_file,
    backup_directory,
    current_version
):
    """
    Safely back up and replace the current legal document.
    """

    new_path = Path(new_file)
    current_path = Path(current_file)
    backup_dir = Path(backup_directory)

    if not new_path.exists():
        raise FileNotFoundError(
            f"New document not found: {new_path}"
        )

    backup_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    if current_path.exists():

        backup_file = (
            backup_dir
            / f"Ley_General_Aduanas_v{current_version}_backup.md"
        )

        if backup_file.exists():
            raise FileExistsError(
                f"Backup already exists: {backup_file}"
            )

        shutil.copy2(
            current_path,
            backup_file
        )

        print(
            f"Backup created: {backup_file}"
        )

    new_path.replace(
        current_path
    )

    print(
        "Current legal document replaced successfully."
    )


def update_metadata(
    new_version_number,
    new_version_id
):
    """
    Update the stored SCIJ version in document_metadata.py.
    """

    text = METADATA_FILE.read_text(
        encoding="utf-8"
    )

    pattern = (
        r'("Ley_General_Aduanas\.md":\s*\{.*?'
        r'"scij_version_id":\s*)\d+'
    )

    text, count = re.subn(
        pattern,
        rf"\g<1>{new_version_id}",
        text,
        count=1,
        flags=re.DOTALL
    )

    if count != 1:
        raise ValueError(
            "Could not update scij_version_id."
        )

    pattern = (
        r'("Ley_General_Aduanas\.md":\s*\{.*?'
        r'"version_number":\s*)\d+'
    )

    text, count = re.subn(
        pattern,
        rf"\g<1>{new_version_number}",
        text,
        count=1,
        flags=re.DOTALL
    )

    if count != 1:
        raise ValueError(
            "Could not update version_number."
        )

    pattern = (
        r'("Ley_General_Aduanas\.md":\s*\{.*?'
        r'"version_total":\s*)\d+'
    )

    text, count = re.subn(
        pattern,
        rf"\g<1>{new_version_number}",
        text,
        count=1,
        flags=re.DOTALL
    )

    if count != 1:
        raise ValueError(
            "Could not update version_total."
        )

    METADATA_FILE.write_text(
        text,
        encoding="utf-8"
    )

    print(
        "Document metadata updated."
    )


def rebuild_index():
    import json
    import os

    from app.indexer import create_index

    production_index = Path("knowledge_base/index.json")
    temporary_index = Path("knowledge_base/index_temp.json")

    print("\n=== REBUILDING INDEX ===")
    print("Building temporary index...")

    # Create the new index without touching the production index.
    chunk_count = create_index(
        output_file=str(temporary_index)
    )

    # Validate the temporary index.
    if not temporary_index.exists():
        raise RuntimeError(
            "Temporary index was not created."
        )

    with open(
        temporary_index,
        "r",
        encoding="utf-8"
    ) as file:
        temporary_data = json.load(file)

    if not isinstance(temporary_data, list):
        raise RuntimeError(
            "Temporary index is not a valid list."
        )

    if len(temporary_data) != chunk_count:
        raise RuntimeError(
            "Temporary index chunk count mismatch."
        )

    if chunk_count == 0:
        raise RuntimeError(
            "Temporary index is empty."
        )

    print(
        f"Temporary index validated: {chunk_count} chunks."
    )

    # Replace production index only after validation succeeds.
    os.replace(
        temporary_index,
        production_index
    )

    print("Production index replaced successfully.")


def run_update():
    """
    Complete SCIJ update workflow.
    """

    print("=== TRADEFLOW SCIJ UPDATE CHECK ===")

    stored = get_stored_metadata()

    print(
        f"Stored version: {stored['version_number']}"
    )

    print(
        f"Stored version ID: {stored['version_id']}"
    )

    latest = get_latest_version_info(
        SCIJ_ID,
        stored["version_id"]
    )

    print(
        f"SCIJ latest version: {latest['version_number']}"
    )

    print(
        f"SCIJ latest version ID: {latest['version_id']}"
    )

    if not check_for_update(
        stored["version_number"],
        latest["version_number"]
    ):
        print("\nNo update needed.")
        return

    print("\nUPDATE AVAILABLE")

    if LATEST_FILE.exists():
        LATEST_FILE.unlink()

    valid = download_latest_version(
        SCIJ_ID,
        latest["version_id"],
        latest["version_number"],
        LATEST_FILE
    )

    if not valid:
        print(
            "\nUpdate stopped."
            "\nCurrent legal document was NOT changed."
        )
        return

    replace_document(
        LATEST_FILE,
        CURRENT_FILE,
        BACKUP_DIRECTORY,
        stored["version_number"]
    )

    rebuild_index()

    update_metadata(
        latest["version_number"],
        latest["version_id"]
    )

    print(
        "\n=== SCIJ UPDATE COMPLETED ==="
    )


if __name__ == "__main__":
    run_update()