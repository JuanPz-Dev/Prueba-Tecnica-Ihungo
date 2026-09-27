import argparse
import logging
import os

from .excel_processor import ExcelProcessor
from .paralleldots_provider import ParallelDotsProvider


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analiza el sentimiento de un archivo Excel."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Ruta del archivo Excel de entrada.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Ruta del archivo Excel de salida.",
    )
    parser.add_argument(
        "--sheet",
        required=True,
        help="Nombre de la hoja que se va a procesar.",
    )
    parser.add_argument(
        "--text-column",
        type=int,
        required=True,
        help="Número de la columna que contiene el texto.",
    )

    return parser.parse_args()
def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    args = parse_arguments()
    api_key = os.getenv("PARALLELDOTS_API_KEY")

    if not api_key:
        raise ValueError(
            "No se encontró la variable de entorno PARALLELDOTS_API_KEY."
        )
    provider = ParallelDotsProvider(api_key)
    processor = ExcelProcessor(
        provider=provider,
        input_file=args.input,
        output_file=args.output,
        sheet_name=args.sheet,
        text_column=args.text_column,
    )

    processor.process()

if __name__ == "__main__":
    main()