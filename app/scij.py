import requests
from bs4 import BeautifulSoup


BASE_URL = "https://sinalevi.go.cr"


def get_document(url):
    response = requests.get(
        url,
        timeout=30
    )

    response.raise_for_status()

    return response.text


def get_full_text(id_ficha_norma, version, busqueda=""):
    url = (
        f"{BASE_URL}/ResultadosNormativa/"
        "_CargarTextoCompleto"
    )

    data = {
        "idFichaNorma": id_ficha_norma,
        "version": version,
        "busqueda": busqueda
    }

    response = requests.post(
        url,
        data=data,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


if __name__ == "__main__":

    id_ficha_norma = 25886
    version = 131179

    result = get_full_text(
        id_ficha_norma,
        version
    )

    print("=== RESPUESTA SCIJ ===")
    print(result.keys())

    html = result.get("html")

    if html:

        with open(
            "knowledge_base/scij_ley_7557.html",
            "w",
            encoding="utf-8"
        ) as file:
            file.write(html)

        print("\nHTML guardado correctamente.")
        print(f"Tamaño: {len(html)} caracteres")

        soup = BeautifulSoup(html, "html.parser")

        print("\n=== HTML DEL PRIMER ARTICULO ===")

        article = soup.find(
            string=lambda text: text and "Ficha Artículo 1" in text
        )

        if article:
            parent = article.parent

            print(
                parent.parent.prettify()[:10000]
            )
        else:
            print("No se encontró el primer artículo.")

        print("\n=== TITULOS ENCONTRADOS ===")

        for tag in soup.find_all(["h1", "h2", "h3", "h4"]):
            text = tag.get_text(" ", strip=True)

            if text:
                print(
                    f"{tag.name.upper()}: {text}"
                )

        print("\n=== PRIMERAS COINCIDENCIAS DE 'ARTÍCULO' ===")

        text = soup.get_text("\n", strip=True)

        lines = text.splitlines()

        count = 0

        for i, line in enumerate(lines):
            if "Artículo" in line:
                print("\n---")
                print("LINEA:", i)
                print(line)

                if i + 1 < len(lines):
                    print(lines[i + 1])

                if i + 2 < len(lines):
                    print(lines[i + 2])

                count += 1

                if count >= 10:
                    break        

        print("\n=== ELEMENTO DEL PRIMER ARTICULO ===")

        link = soup.find(
            "a",
            string=lambda text: text and "Ficha Artículo 1" in text
        )

        if link:

            print("LINK ENCONTRADO:")
            print(link)

            print("\nPADRE:")
            print(link.parent.prettify()[:5000])

            print("\nPADRE DEL PADRE:")
            print(link.parent.parent.prettify()[:10000])

        else:
            print("No se encontró el enlace.")        

    else:
        print("\nNo se recibió HTML.")