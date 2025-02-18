import pandas as pd
import concurrent.futures
import time
from dibs_computing_core.iso_simulator.model.summary_result import SummaryResult
from dibs_computing_core.iso_simulator.model.building import Building
from dibs_computing_core.iso_simulator.model.hours_result import Result


def convert_end_result_to_dataframe(result: SummaryResult) -> pd.DataFrame:
    """
    Maps a list of ResultOutput objects to a pandas Dataframe
    Args:
        result: result of a simulated building

    Returns:
        dataframe
    """

    return pd.DataFrame({
        "GebäudeID": result.building_id,
        "EnergyRefArea": result.energy_ref_area,
        "HeatingDemand [kWh]": result.heating_demand,
        "HeatingDemand [kwh/m2]": result.heating_demand_surface,
        "HeatingEnergy [kWhHs]": result.heating_energy,
        "HeatingEnergy [kwhHs/m2]": result.heating_energy_surface,
        "HeatingEnergy_Hi [kWhHi]": result.heating_energy_hi,
        "Heating_Sys_Electricity [kWh]": result.heating_sys_electricity,
        "Heating_Sys_Electricity [kwh/m2]": result.heating_sys_electricity_surface,
        "Heating_Sys_Electricity_Hi [kWhHi]": result.heating_sys_electricity_hi,
        "Heating_Sys_Fossils [kWhHs]": result.heating_sys_fossils,
        "Heating_Sys_Fossils [kwhHs/m2]": result.heating_sys_fossils_surface,
        "Heating_Sys_Fossils_Hi [kWhHi]": result.heating_sys_fossils_hi,
        "Heating_Sys_GWP [kg]": result.heating_sys_gwp,
        "Heating_Sys_GWP [kg/m2]": result.heating_sys_gwp,
        "Heating_Sys_PE [kWh]": result.heating_sys_pe,
        "Heating_Sys_PE [kWh/m2]": result.heating_sys_pe_surface,
        "CoolingDemand [kWh]": result.cooling_demand,
        "CoolingDemand [kwh/m2]": result.cooling_demand_surface,
        "CoolingEnergy [kWhHs]": result.cooling_energy,
        "CoolingEnergy [kwhHs/m2]": result.cooling_energy_surface,
        "Cooling_Sys_Electricity [kWh]": result.cooling_sys_electricity,
        "Cooling_Sys_Electricity [kwh/m2]": result.cooling_sys_electricity_surface,
        "Cooling_Sys_Fossils [kWhHs]": result.cooling_sys_fossils,
        "Cooling_Sys_Fossils [kwhHs/m2]": result.cooling_sys_fossils_surface,
        "Cooling_Sys_GWP [kg]": result.cooling_sys_gwp,
        "Cooling_Sys_GWP [kg/m2]": result.cooling_sys_gwp_surface,
        "Cooling_Sys_PE [kWh]": result.cooling_sys_pe,
        "Cooling_Sys_PE [kWh/m2]": result.cooling_sys_pe_surface,
        "HotWaterDemand [kwh]": result.hot_water_demand,
        "HotWaterDemand [kwh/m2]": result.hot_water_demand_surface,
        "HotWaterEnergy [kwhHs]": result.hot_water_energy,
        "HotWaterEnergy [kwhHs/m2]": result.hot_water_energy_surface,
        "HotWaterEnergy_Hi [kwhHi]": result.hot_water_energy_hi,
        "HotWater_Sys_Electricity [kWh]": result.hot_water_sys_electricity,
        "HotWater_Sys_Fossils [kWhHs]": result.hot_water_sys_fossils,
        "HeatingSupplySystem": result.heating_supply_system,
        "CoolingSupplySystem": result.cooling_supply_system,
        "DHWSupplySystem": result.dhw_supply_system,
        "Heating_fuel_type": result.heating_fuel_type,
        "Heating_f_GHG [g/kWhHi]": result.heating_f_ghg,
        "Heating_f_PE [kWhPE/kWhHi]": result.heating_f_pe,
        "Heating_f_Hs_Hi [kWhHs/kWhHi]": result.heating_f_hs_hi,
        "Hotwater_fuel_type": result.hotwater_fuel_type,
        "Hotwater_f_GHG [g/kWhHi]": result.hotwater_f_ghg,
        "Hotwater_f_PE [kWhPE/kWhHi]": result.hotwater_f_pe,
        "Hotwater_f_Hs_Hi [kWhHs/kWhHi]": result.hotwater_f_hs_hi,
        "Cooling_fuel_type": result.cooling_fuel_type,
        "Cooling_f_GHG [g/kWhHi]": result.cooling_f_ghg,
        "Cooling_f_PE [kWhPE/kWhHi]": result.cooling_f_pe,
        "Cooling_f_Hs_Hi [kWhHs/kWhHi]": result.cooling_f_hs_hi,
        "LightAppl_fuel_type": result.light_appl_fuel_type,
        "LightAppl_f_GHG [g/kWhHi]": result.light_appl_f_ghg,
        "LightAppl_f_PE [kWhPE/kWhHi]": result.light_appl_f_pe,
        "LightAppl_f_Hs_Hi [kWhHs/kWhHi]": result.light_appl_f_hs_hi,
        "HotWater_Sys_GWP [kg]": result.hotwater_sys_gwp,
        "HotWater_Sys_GWP [kg/m2]": result.hotwater_sys_gwp_surface,
        "HotWater_Sys_PE [kWh]": result.hotwater_sys_pe,
        "HotWater_Sys_PE [kWh/m2]": result.hotwater_sys_pe_surface,
        "ElectricityDemandTotal [kWh]": result.electricity_demand_total,
        "ElectricityDemandTotal [kwh/m2]": result.electricity_demand_total_surface,
        "FossilsDemandTotal [kWh]": result.fossils_demand_total,
        "FossilsDemandTotal [kwh/m2]": result.fossils_demand_total_surface,
        "LightingDemand [kWh]": result.lighting_demand,
        "LightingDemand_GWP [kg]": result.lighting_demand_gwp,
        "LightingDemand_GWP [kg/m2]": result.lighting_demand_gwp_surface,
        "LightingDemand_PE [kWh]": result.lighting_demand_pe,
        "LightingDemand_PE [kWh/m2]": result.lighting_demand_pe_surface,
        "Appliance_gains_demand [kWh]": result.appliance_gains_demand,
        "Appliance_gains_elt_demand [kWh]": result.appliance_gains_elt_demand,
        "Appliance_gains_demand_GWP [kg]": result.appliance_gains_demand_gwp,
        "Appliance_gains_demand_GWP [kg/m2]": result.appliance_gains_demand_gwp_surface,
        "Appliance_gains_demand_PE [kWh]": result.appliance_gains_demand_pe,
        "Appliance_gains_demand_PE [kWh/m2]": result.appliance_gains_demand_pe,
        "GWP [kg]": result.gwp,
        "GWP [kg/m2]": result.gwp_surface,
        "PE [kWh]": result.pe,
        "PE [kWh/m2]": result.pe_surface,
        "FinalEnergy_Hi [kWhHi]": result.final_energy_hi,
        "InternalGains [kWh]": result.internal_gains,
        "SolarGainsTotal [kWh]": result.solar_gains_total,
        "SolarGainsSouthWindow [kWh]": result.solar_gains_south_window,
        "SolarGainsEastWindow [kWh]": result.solar_gains_east_window,
        "SolarGainsWestWindow [kWh]": result.solar_gains_west_window,
        "SolarGainsNorthWindow [kWh]": result.solar_gains_north_window,
        "Gebäudefunktion Hauptkategorie": result.building_function_main_category,
        "Gebäudefunktion Unterkategorie": result.building_function_sub_category,
        "Profil SIA 2024": result.profile_sia_2024,
        "Profil 18599-10": result.profile_18599,
        "EPW-File": result.epw_file,
        "profile_from_norm": result.profile_from_norm,
        "gains_from_group_values": result.gains_from_group_values,
        "usage_from_norm": result.usage_from_norm,
        "weather_period": result.weather_period})


def convert_result_of_all_hours_to_dataframe(result: Result, building: Building, iteration: int) -> pd.DataFrame:
    """
    Maps the results of the simulated building to an Excel file (all hours)
    Args:
        result: result
        building: the building to simulate
        iteration

    Returns:
        df
    """
    return pd.DataFrame(
        {
            "HeatingDemand": result.heating_demand,
            "HeatingEnergy": result.heating_energy,
            "Heating_Sys_Electricity": result.heating_sys_electricity,
            "Heating_Sys_Fossils": result.heating_sys_fossils,
            "CoolingDemand": result.cooling_demand,
            "CoolingEnergy": result.cooling_energy,
            "Cooling_Sys_Electricity": result.cooling_sys_electricity,
            "Cooling_Sys_Fossils": result.cooling_sys_fossils,
            "HotWaterDemand": result.all_hot_water_demand,
            "HotWaterEnergy": result.all_hot_water_energy,
            "HotWater_Sys_Electricity": result.hot_water_sys_electricity,
            "HotWater_Sys_Fossils": result.hot_water_sys_fossils,
            "IndoorAirTemperature": result.temp_air,
            "OutsideTemperature": result.outside_temp,
            "LightingDemand": result.lighting_demand,
            "InternalGains": result.internal_gains,
            "Appliance_gains_demand": result.appliance_gains_demand,
            "Appliance_gains_elt_demand": result.appliance_gains_elt_demand,
            "SolarGainsSouthWindow": result.solar_gains_south_window,
            "SolarGainsEastWindow": result.solar_gains_east_window,
            "SolarGainsWestWindow": result.solar_gains_west_window,
            "SolarGainsNorthWindow": result.solar_gains_north_window,
            "SolarGainsTotal": result.solar_gains_total,
            "Daytime": result.DayTime,
            "iteration": iteration,
            "GebäudeID": building.scr_gebaeude_id,
        }
    )


def save_results_of_all_buildings_hours_in_csv_parallel_using_thread_executor(buildings: list[Building],
                                                                              result: list[Result],
                                                                              folder_path: str) -> float:
    """
    Saves results in csv files and calculates the time needed
    Parameters
    buildings: list of the buildings
    result:
    folder_path:
    Returns
        saving_time
    """
    begin_saving_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                save_buildings_all_hours_results_to_excel,
                result[index],
                folder_path,
                building,
                index,
            )
            for index, building in enumerate(buildings)
        ]
        results = [
            future.result()
            for future in concurrent.futures.as_completed(futures)
        ]

    end_saving_time = time.time()
    return end_saving_time - begin_saving_time


def build_all_results_of_all_buildings_to_dataframe(results: list[SummaryResult]) -> pd.DataFrame:
    """
    Converts the results of all buildings to an Excel file saved in the result directory
    Args:
        results: results of all building

    Returns:
          df

    """
    list_of_results = [
        convert_end_result_to_dataframe(result)
        for result in results
    ]

    return pd.concat(list_of_results)


def save_buildings_all_hours_results_to_excel(result: Result, folder_path: str,
                                              building: Building, iteration: int) -> None:
    """

    Parameters
    ----------
    result: result to be saved
    folder_path: where to save csv file
    building: simulated building
    iteration:

    Returns
    -------

    """
    df = convert_result_of_all_hours_to_dataframe(result, building, iteration)
    df.to_csv(rf"{folder_path}/{building.scr_gebaeude_id}.csv", index=False)
