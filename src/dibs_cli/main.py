import os
import glob
import re
import typer
import time
import pandas as pd
from math import ceil
from rich.console import Console
from dibs_datasource_csv.datasource_csv import DataSourceCSV
from dibs_computing_core.iso_simulator.dibs.dibs import DIBS
from .dibscli_utils.validate_inputs import (
    check_the_file_given_by_the_user,
)
from .dibscli_utils.save_results import convert_result_of_all_hours_to_dataframe, convert_end_result_to_dataframe, \
    save_results_of_all_buildings_hours_in_csv_parallel_using_thread_executor, \
    build_all_results_of_all_buildings_to_dataframe
from .dibscli_utils.validate_inputs import create_result_table, validate_weather_period, validate_usage_from_norm, \
    validate_profile_from_norm, validate_gains_from_group_values, validate_summary_only, validate_primary_energy_factor
from tqdm import tqdm

console = Console()
app = typer.Typer()


@app.command()
def simulate_one_building(
        data_path: str,
        profile_from_norm: str = typer.Option('din18599', '--profile_from_norm', metavar='VALID_PROFILE_FROM_NORM',
                                              callback=validate_profile_from_norm),
        gains_from_group_values: str = typer.Option('mid', '--gains_from_group_values',
                                                    metavar='VALID_GAINS_FROM_GROUP_VALUES',
                                                    callback=validate_gains_from_group_values),
        usage_from_norm: str = typer.Option('sia2024', '--usage_from_norm', metavar='VALID_USAGE_NORM',
                                            callback=validate_usage_from_norm),
        weather_period: str = typer.Option('2007-2021', '--weather_period', metavar='VALID_WEATHER_PERIOD',
                                           callback=validate_weather_period),
        summary_only: bool = typer.Option(False, '--summary_only', callback=validate_summary_only),

        primary_energy_factor: str = typer.Option('Primary Energy Factor GEG   [-]', '--primary_energy_factor',
                                                  metavar='VALID_PRIMARY_ENERGY_FACTOR',
                                                  callback=validate_primary_energy_factor),
):
    check_the_file_given_by_the_user(data_path)

    folder_path = os.path.dirname(data_path)

    datasource_csv = DataSourceCSV(data_path, profile_from_norm, gains_from_group_values,
                                   usage_from_norm,
                                   weather_period, primary_energy_factor)

    dibs = DIBS(datasource_csv)
    file_name = os.path.basename(data_path)

    simulation_time, result_of_all_hours, summary_result = dibs.calculate_result_of_one_building()

    with tqdm(total=1, desc="Writing summary result in ", colour='red') as pbar:
        start_time = time.time()
        summary_result_dataframe = convert_end_result_to_dataframe(summary_result, file_name)
        summary_result_dataframe.to_excel(rf"{folder_path}/annualResults_summary.xlsx", index=False)
        end_time = time.time()
        saving_summary_result_time = end_time - start_time
        pbar.update(1)

    with tqdm(total=1, desc="Writing Excel", colour='red') as pbar:
        start_time = time.time()
        if not summary_only:
            all_hours_result_dataframe = convert_result_of_all_hours_to_dataframe(result_of_all_hours,
                                                                                  datasource_csv.building,
                                                                                  0)
        build_file_name = f"{datasource_csv.building.scr_gebaeude_id}.csv"
        if not summary_only:
            all_hours_result_dataframe.to_csv(f"{folder_path}/{build_file_name}")

        end_time = time.time()
        saving_all_hours_result_time = end_time - start_time
        pbar.update(1)

    console.print(
        f"Time to simulate the [bold yellow]building[/bold yellow] with the id [bold yellow]{datasource_csv.building.scr_gebaeude_id}[/bold yellow] is : [bold magenta]{simulation_time}s[/bold magenta]"
    )

    console.print(
        f"Time to save [bold yellow]results[/bold yellow] in [bold yellow]csv[/bold yellow] file is : [bold magenta]{saving_summary_result_time}s[/bold magenta]"
    )

    if not summary_only:
        console.print(
            f"Time to save [bold yellow]results of the 8760 hours[/bold yellow] in [bold yellow]Excel[/bold yellow] file is : [bold magenta]{saving_all_hours_result_time}s[/bold magenta]"
        )

    console.print(
        f"The files contain the results are [bold yellow]{build_file_name}[/bold yellow] and [bold yellow]annualResults_summary.xlsx[/bold yellow] and saved in this folder [bold magenta]{folder_path}[/bold magenta]"
    )

    create_result_table(summary_result_dataframe)


@app.command()
def simulate_all_building(
        data_path: str,
        profile_from_norm: str = typer.Option('din18599', '--profile_from_norm', metavar='VALID_PROFILE_FROM_NORM'),
        gains_from_group_values: str = typer.Option('mid', '--gains_from_group_values',
                                                    metavar='VALID_GAINS_FROM_GROUP_VALUES'),
        usage_from_norm: str = typer.Option('sia2024', '--usage_from_norm', metavar='VALID_USAGE_NORM'),
        weather_period: str = typer.Option('2007-2021', '--weather_period', metavar='VALID_WEATHER_PERIOD'),
        summary_only: bool = typer.Option(False, '--summary_only', callback=validate_summary_only),
        primary_energy_factor: str = typer.Option('Primary Energy Factor GEG   [-]', '--primary_energy_factor',
                                                  metavar='VALID_PRIMARY_ENERGY_FACTOR',
                                                  callback=validate_primary_energy_factor),
):
    folder_path = os.path.dirname(data_path)
    check_the_file_given_by_the_user(data_path)

    datasource_csv = DataSourceCSV(data_path, profile_from_norm, gains_from_group_values,
                                   usage_from_norm,
                                   weather_period,
                                   primary_energy_factor)

    dibs = DIBS(datasource_csv)

    file_name = os.path.basename(data_path)
    simulation_time, result_of_all_hours, summary_result = dibs.multi()

    with tqdm(total=1, desc="Writing summary result in ", colour='red') as pbar:
        start_time = time.time()
        summary_result_dataframe = build_all_results_of_all_buildings_to_dataframe(summary_result, file_name)
        summary_result_dataframe.to_excel(rf"{folder_path}/annualResults_summary.xlsx", index=False)
        end_time = time.time()
        saving_summary_result = end_time - start_time
        pbar.update(1)

    if not summary_only:
        with tqdm(total=1, desc="Writing hourly result in ", colour='red') as pbar:
            time_to_save_hourly_results = save_results_of_all_buildings_hours_in_csv_parallel_using_thread_executor(
                dibs.datasource.buildings,
                result_of_all_hours, folder_path)
            pbar.update(1)

    console.print(
        "---------------------------------------------------------------------------------"
    )
    console.print(
        f"All results will be saved in the folder: [bold magenta]{folder_path}s[/bold magenta]"
    )
    console.print(
        "---------------------------------------------------------------------------------"
    )
    console.print(
        f"Time to simulate all buildings is: [bold magenta]{simulation_time}s[/bold magenta]"
    )
    console.print(
        f"Time to save summary results  is: [bold gold]{saving_summary_result}s[/bold gold]"
    )
    if not summary_only:
        console.print(
            f"Time to save hourly results  is: [bold gold]{time_to_save_hourly_results}s[/bold gold]"
        )


@app.command()
def simulate_buildings_with_batches(
        data_path: str,
        profile_from_norm: str = typer.Option('din18599', '--profile_from_norm', metavar='VALID_PROFILE_FROM_NORM'),
        gains_from_group_values: str = typer.Option('mid', '--gains_from_group_values',
                                                    metavar='VALID_GAINS_FROM_GROUP_VALUES'),
        usage_from_norm: str = typer.Option('sia2024', '--usage_from_norm', metavar='VALID_USAGE_NORM'),
        weather_period: str = typer.Option('2007-2021', '--weather_period', metavar='VALID_WEATHER_PERIOD'),
        summary_only: bool = typer.Option(False, '--summary_only', callback=validate_summary_only),
        primary_energy_factor: str = typer.Option('Primary Energy Factor GEG   [-]', '--primary_energy_factor',
                                                  metavar='VALID_PRIMARY_ENERGY_FACTOR',
                                                  callback=validate_primary_energy_factor),
):
    folder_path = os.path.dirname(data_path)
    check_the_file_given_by_the_user(data_path)

    datasource_csv = DataSourceCSV(data_path, profile_from_norm, gains_from_group_values,
                                   usage_from_norm,
                                   weather_period,
                                   primary_energy_factor)

    dibs = DIBS(datasource_csv)

    file_name = os.path.basename(data_path)

    user_args = dibs.get_user_args()
    dibs.datasource.get_user_buildings()
    dibs.datasource.get_epw_pe_factors()

    buildings = dibs.datasource.buildings
    batch_size = 100
    total_buildings = len(buildings)
    batches = ceil(total_buildings / batch_size)

    for batch_index in range(batches):
        start = batch_index * batch_size
        end = min(start + batch_size, total_buildings)
        batch_results = []

        simulation_time, result_of_all_hours, summary_result = dibs.multi_with_batches(user_args, buildings, start, end,
                                                                                       batch_results)

        with tqdm(total=1, desc="Writing summary result in ", colour='red') as pbar:
            start_time = time.time()
            summary_result_dataframe = build_all_results_of_all_buildings_to_dataframe(summary_result, file_name)
            batch_file = os.path.join(folder_path, f"annualResults_summary{batch_index}.xlsx")
            summary_result_dataframe.to_excel(batch_file, index=False)
            # summary_result_dataframe.to_excel(rf"{folder_path}/annualResults_summary{batch_index}.xlsx", index=False)
            end_time = time.time()
            saving_summary_result = end_time - start_time
            pbar.update(1)

        if not summary_only:
            with tqdm(total=1, desc="Writing hourly result in ", colour='red') as pbar:
                time_to_save_hourly_results = save_results_of_all_buildings_hours_in_csv_parallel_using_thread_executor(
                    dibs.datasource.buildings,
                    result_of_all_hours, folder_path)
                pbar.update(1)

        console.print(
            "---------------------------------------------------------------------------------"
        )
        console.print(
            f"All results will be saved in the folder: [bold magenta]{folder_path}s[/bold magenta]"
        )
        console.print(
            "---------------------------------------------------------------------------------"
        )
        console.print(
            f"Time to simulate all buildings is: [bold magenta]{simulation_time}s[/bold magenta]"
        )
        console.print(
            f"Time to save summary results  is: [bold gold]{saving_summary_result}s[/bold gold]"
        )
        if not summary_only:
            console.print(
                f"Time to save hourly results  is: [bold gold]{time_to_save_hourly_results}s[/bold gold]"
            )
    # print("Merging all batch Excel files into one...")
    #
    # all_files = glob.glob(os.path.join(folder_path, "annualResults_summary*.xlsx"))
    # print(f'all files: {all_files}')
    #
    # df_list = [pd.read_excel(file) for file in all_files]
    # merged_df = pd.concat(df_list, ignore_index=True)
    #
    # final_path = os.path.join(folder_path, "annualResults_summary.xlsx")
    # merged_df.to_excel(final_path, index=False)
    #
    # for file in all_files:
    #     if file != final_path:
    #         os.remove(file)
    #
    # print(f"? Zusammenfassung gespeichert unter: {final_path}")

    all_files = glob.glob(os.path.join(folder_path, "annualResults_summary*.xlsx"))

    def extract_number(filename):
        match = re.search(r"summary(\d+)\.xlsx$", filename)
        return int(match.group(1)) if match else -1

    all_files_sorted = sorted(all_files, key=extract_number)

    df_list = [pd.read_excel(file) for file in all_files_sorted if extract_number(file) != -1]
    merged_df = pd.concat(df_list, ignore_index=True)

    final_path = os.path.join(folder_path, "annualResults_summary.xlsx")
    merged_df.to_excel(final_path, index=False)

    for file in all_files_sorted:
        if extract_number(file) != -1:
            os.remove(file)


if __name__ == "__main__":
    app()
