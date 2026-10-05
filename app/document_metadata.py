DOCUMENT_METADATA = {
    "IngresoSalida.md": {
        "document_type": "manual",
        "institution": "Ministerio de Hacienda",
        "status": "vigente",
        "source": "Ministerio de Hacienda"
    },

    "IngresoSalidaMultimodal.md": {
        "document_type": "manual",
        "institution": "Ministerio de Hacienda",
        "status": "vigente",
        "source": "Ministerio de Hacienda"
    },

    "Ley_General_Aduanas.md": {
        "document_type": "law",
        "institution": "Asamblea Legislativa",
        "status": "vigente",
        "source": "SCIJ",
        "law_number": "7557",
        "scij_id": 25886,
        "scij_version_id": 131179,
        "version_number": 11,
        "version_total": 11
    }
}


def get_document_metadata(filename):
    return DOCUMENT_METADATA.get(
        filename,
        {
            "document_type": "unknown",
            "institution": "unknown",
            "status": "unknown",
            "source": "unknown"
        }
    )