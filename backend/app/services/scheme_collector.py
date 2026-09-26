import json
import os


def load_schemes():
    """
    Eligify ke scheme database ko load karta hai.
    """

    # ELIGIFY project root
    base_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
        )
    )

    schemes_path = os.path.join(
        base_dir,
        "data",
        "schemes",
        "schemes.json"
    )

    print("Looking for schemes at:", schemes_path)

    try:
        with open(
            schemes_path,
            "r",
            encoding="utf-8"
        ) as file:

            schemes = json.load(file)

        print("Schemes loaded:", len(schemes))

        return schemes

    except FileNotFoundError:

        print("Scheme database file nahi mili.")

        return []

    except json.JSONDecodeError:

        print("schemes.json ka JSON format invalid hai.")

        return []


def get_all_schemes():
    """
    Saari government schemes return karta hai.
    """

    return load_schemes()