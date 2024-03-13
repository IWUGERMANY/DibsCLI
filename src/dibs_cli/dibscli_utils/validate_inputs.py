from rich.console import Console
from rich.table import Table
import re
import os
import argparse

VALID_PROFILE_FROM_NORM = ["din18599", "sia2024"]

VALID_GAINS_FROM_GROUP_VALUES = ["low", "mid", "max"]

VALID_USAGE_NORM = ["din18599", "sia2024"]

Valid_WEATHER_PERIOD = ["2004-2018", "2007-2021"]

UNITS = [
    "",
    "",
    "[kWh]",
    "[kwh/m2]",
    "[kWhHs]",
    "[kwhHs/m2]",
    "[kWhHi]",
    "[kWh]",
    "[kwh/m2]",
    "[kWhHi]",
    "[kWhHs]",
    "[kwhHs/m2]",
    "[kWhHi]",
    "[kg]",
    "[kg/m2]",
    "[kWh]",
    "[kWh/m2]",
    "[kWh]",
    "[kWh/m2]",
    "[kWhHs]",
    "[kwhHs/m2]",
    "[kWh]",
    "[kwh/m2]",
    "[kWhHs]",
    "[kwhHs/m2]",
    "[kg]",
    "[kg/m2]",
    "[kWh]",
    "[kWh/m2]",
    "[kwh]",
    "[kwh/m2]",
    "[kwhHs]",
    "[kwhHs/m2]",
    "[kwhHi]",
    "[kWh]",
    "[kWhHs]",
    "",
    "",
    "",
    "",
    "[g/kWhHi]",
    "[kWhPE/kWhHi]",
    "[kWhHs/kWhHi]",
    "",
    "[g/kWhHi]",
    "[kWhPE/kWhHi]",
    "[kWhHs/kWhHi]",
    "[kWhHs/kWhHi]",
    "",
    "[g/kWhHi]",
    "[kWhPE/kWhHi]",
    "[kWhHs/kWhHi]",
    "",
    "[g/kWhHi]",
    "[kWhPE/kWhHi]",
    "[kWhHs/kWhHi]",
    "[kg]",
    "[kg/m2]",
    "[kWh]",
    "[kWh/m2]",
    "[kWh]",
    "[kWh/m2]",
    "[kWh]",
    "[kWh/m2]",
    "[kWh]",
    "[kg]",
    "[kg/m2]",
    "[kWh]",
    "[kWh/m2]",
    "[kWh]",
    "[kWh]",
    "[kg]",
    "[kg/m2]",
    "[kWh]",
    "[kWh/m2]",
    "[kWh]",
    "[kWh/m2]",
    "[kg]",
    "[kg/m2]",
    "[kWh]",
    "[kWh/m2]",
    "[kWhHi]",
    "[kWh]",
    "[kWh]",
    "[kWh]",
    "[kWh]",
    "[kWh]",
    "[kWh]",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]


def get_user_arguments(
        gains_from_group_values, profile_from_norm, usage_from_norm, weather_period
):
    user_args = [
        profile_from_norm,
        gains_from_group_values,
        usage_from_norm,
        weather_period,
    ]
    return user_args


def validate_profile_from_norm(profile_from_norm: str):
    if profile_from_norm not in VALID_PROFILE_FROM_NORM:
        raise argparse.ArgumentTypeError(
            f"Invalid profile norm Please choose one of: {', '.join(VALID_PROFILE_FROM_NORM)}"
        )
    return profile_from_norm


def validate_gains_from_group_values(gains_from_group_values: str):
    if gains_from_group_values not in VALID_GAINS_FROM_GROUP_VALUES:
        raise argparse.ArgumentTypeError(
            f"Invalid profile norm Please choose one of: {', '.join(VALID_GAINS_FROM_GROUP_VALUES)}"
        )
    return gains_from_group_values


def validate_usage_from_norm(usage_from_norm: str):
    if usage_from_norm not in VALID_USAGE_NORM:
        raise argparse.ArgumentTypeError(
            f"Invalid profile norm Please choose one of: {', '.join(VALID_USAGE_NORM)}"
        )
    return usage_from_norm


def validate_weather_period(weather_period: str):
    pattern = re.compile(r"^\d{4}-\d{4}$")
    if not pattern.match(weather_period):
        raise argparse.ArgumentTypeError("Invalid date range format. Please use 'YYYY-YYYY'.")
    if weather_period not in Valid_WEATHER_PERIOD:
        raise argparse.ArgumentTypeError(
            f"Invalid weather period Please choose one of: {', '.join(Valid_WEATHER_PERIOD)}"
        )
    return weather_period


def check_the_file_given_by_the_user(path):
    console = Console()
    if not os.path.exists(path):
        file_name = os.path.basename(path)
        console.print(f"The path to the file {file_name} does not exist")
    _, file_extension = os.path.splitext(path)
    if file_extension.lower() not in [".csv", ".xlsx"]:
        console.print(
            f"The file extension [bold magenta]{file_extension}[/bold magenta] is not supported"
        )
        console.print(
            "Supported file extensions are:  [bold magenta].csv[/bold magenta] or [bold magenta].xlsx[/bold magenta]"
        )


def parse_user_args():
    parser = argparse.ArgumentParser(description='Simulate one building')
    parser.add_argument('data_path', type=str, help='Path to data (cvs or xlsx)')
    parser.add_argument('--profile_from_norm', type=validate_profile_from_norm, default='din18599',
                        help='Choose a profile from', metavar='PROFILE_FROM_NORM')
    parser.add_argument('--gains_from_group_values', type=validate_gains_from_group_values, default='mid',
                        help='Choose a gain from', metavar='GAINS_FROM_GROUP_VALUES')
    parser.add_argument('--usage_from_norm', type=validate_usage_from_norm, default='sia2024',
                        help='Choose a usage norm from', metavar='USAGE_FROM_NORM')
    parser.add_argument('--weather_period', type=validate_weather_period, default='2007-2021',
                        help="Invalid date range format. Please use 'YYYY-YYYY'.", metavar='WEATHER_PERIOD')

    return parser


def create_result_table(end_result_dataframe):
    console = Console()
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("FEATURE", min_width=20)
    table.add_column("VALUE", min_width=13)
    table.add_column("UNIT", width=10)
    for index, (column_name, series) in enumerate(end_result_dataframe.items()):
        table.add_row(
            str(index),
            column_name,
            f"[bold magenta]{str(series.iloc[0])}[/bold magenta]",
            f'[bold cyan]{UNITS[index].replace("[", "").replace("]", "")}[/bold cyan]',
        )
    console.print(table)
