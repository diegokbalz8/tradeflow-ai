DOCUMENT_METADATA = {
    "IngresoSalida.md": {
        "title": "Manual de Procedimientos Aduaneros - Ingreso y Salida de Mercancías",
        "document_type": "manual",
        "institution": "Ministerio de Hacienda",
        "status": "vigente",
        "source": "Ministerio de Hacienda"
    },

    "IngresoSalidaMultimodal.md": {
        "title": "Manual de Procedimientos Aduaneros - Ingreso y Salida de Mercancías por Transporte Multimodal",
        "document_type": "manual",
        "institution": "Ministerio de Hacienda",
        "status": "vigente",
        "source": "Ministerio de Hacienda"
    },

    "Ley_General_Aduanas.md": {
        "title": "Ley General de Aduanas N.º 7557",    
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
            "title": "unknown",
            "document_type": "unknown",
            "institution": "unknown",
            "status": "unknown",
            "source": "unknown"
        }
    )