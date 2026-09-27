import argparse

from bouncy import least_number_with_bouncy_ratio


def main(args=None) -> None:
    parser = argparse.ArgumentParser(
        description="Calcula el primer número con un porcentaje exacto de números bouncy."
    )

    parser.add_argument(
        "percent",
        type=int,
        help="Porcentaje de números bouncy entre 1 y 99.",
    )

    parsed_args = parser.parse_args(args)

    try:
        result = least_number_with_bouncy_ratio(parsed_args.percent)
        print(result)
    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()