import requests


BASE_URL = "https://sinalevi.go.cr"


def inspect_menu_script():

    url = (
        BASE_URL +
        "/js/views/MenuLateral/MenuNormativa.js"
    )

    response = requests.get(
        url,
        timeout=30
    )

    response.raise_for_status()

    javascript = response.text

    print(
        f"JavaScript size: {len(javascript)} characters"
    )

    print("\n=== LINES RELATED TO VERSION ===")

    for line_number, line in enumerate(
        javascript.splitlines(),
        start=1
    ):

        if "version" in line.lower():

            print(
                f"{line_number}: {line.strip()}"
            )


if __name__ == "__main__":

    inspect_menu_script()