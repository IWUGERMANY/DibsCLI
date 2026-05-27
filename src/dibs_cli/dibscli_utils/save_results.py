import concurrent.futures
import importlib.metadata
import time
from datetime import datetime

import pandas as pd

from dibs_computing_core.iso_simulator.model.building import Building
from dibs_computing_core.iso_simulator.model.hours_result import Result
from dibs_computing_core.iso_simulator.model.summary_result import SummaryResult


def get_dependency_versions() -> dict[str, str | None]:
    dependencies = [
        "dibs_computing_core",
        "dibs_datasource_csv",
        "dibs_cli",
        "dibs_data",
    ]
    versions = {}
    for package in dependencies:
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = None
    return versions


def convert_end_result_to_dataframe(result: SummaryResult, file_name: str) -> pd.DataFrame:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    versions = get_dependency_versions()

    return pd.DataFrame({
        "GebÃ¤udeID": [result.building_id],
        "EnergyRefArea": [result.energy_ref_area],
        "HeatingDemand [kWh]": [result.heating_demand],
        "HeatingDemand [kwh/m2]": [result.heating_demand_surface],
        "HeatingEnergy [kWhHs]": [result.heating_energy],
        "HeatingEnergy [kwhHs/m2]": [result.heating_energy_surface],
        "HeatingEnergy_Hi [kWhHi]": [result.heating_energy_hi],
        "Heating_Sys_Electricity [kWh]": [result.heating_sys_electricity],
        "Heating_Sys_Electricity [kwh/m2]": [result.heating_sys_electricity_surface],
        "Heating_Sys_Electricity_Hi [kWhHi]": [result.heating_sys_electricity_hi],
        "Heating_Sys_Fossils [kWhHs]": [result.heating_sys_fossils],
        "Heating_Sys_Fossils [kwhHs/m2]": [result.heating_sys_fossils_surface],
        "Heating_Sys_Fossils_Hi [kWhHi]": [result.heating_sys_fossils_hi],
        "Heating_Sys_GWP [kg]": [result.heating_sys_gwp],
        "Heating_Sys_GWP [kg/m2]": [result.heating_sys_gwp_surface],
        "Heating_Sys_PE [kWh]": [result.heating_sys_pe],
        "Heating_Sys_PE [kWh/m2]": [result.heating_sys_pe_surface],
        "CoolingDemand [kWh]": [result.cooling_demand],
        "CoolingDemand [kwh/m2]": [result.cooling_demand_surface],
        "CoolingEnergy [kWhHs]": [result.cooling_energy],
        "CoolingEnergy [kwhHs/m2]": [result.cooling_energy_surface],
        "Cooling_Sys_Electricity [kWh]": [result.cooling_sys_electricity],
        "Cooling_Sys_Electricity [kwh/m2]": [result.cooling_sys_electricity_surface],
        "Cooling_Sys_Fossils [kWhHs]": [result.cooling_sys_fossils],
        "Cooling_Sys_Fossils [kwhHs/m2]": [result.cooling_sys_fossils_surface],
        "Cooling_Sys_GWP [kg]": [result.cooling_sys_gwp],
        "Cooling_Sys_GWP [kg/m2]": [result.cooling_sys_gwp_surface],
        "Cooling_Sys_PE [kWh]": [result.cooling_sys_pe],
        "Cooling_Sys_PE [kWh/m2]": [result.cooling_sys_pe_surface],
        "HotWaterDemand [kwh]": [result.hot_water_demand],
        "HotWaterDemand [kwh/m2]": [result.hot_water_demand_surface],
        "HotWaterEnergy [kwhHs]": [result.hot_water_energy],
        "HotWaterEnergy [kwhHs/m2]": [result.hot_water_energy_surface],
        "HotWaterEnergy_Hi [kwhHi]": [result.hot_water_energy_hi],
        "HotWater_Sys_Electricity [kWh]": [result.hot_water_sys_electricity],
        "HotWater_Sys_Fossils [kWhHs]": [result.hot_water_sys_fossils],
        "HeatingSupplySystem": [result.heating_supply_system],
        "CoolingSupplySystem": [result.cooling_supply_system],
        "DHWSupplySystem": [result.dhw_supply_system],
        "Heating_fuel_type": [result.heating_fuel_type],
        "Heating_f_GHG [g/kWhHi]": [result.heating_f_ghg],
        "Heating_f_PE [kWhPE/kWhHi]": [result.heating_f_pe],
        "Heating_f_Hs_Hi [kWhHs/kWhHi]": [result.heating_f_hs_hi],
        "Hotwater_fuel_type": [result.hotwater_fuel_type],
        "Hotwater_f_GHG [g/kWhHi]": [result.hotwater_f_ghg],
        "Hotwater_f_PE [kWhPE/kWhHi]": [result.hotwater_f_pe],
        "Hotwater_f_Hs_Hi [kWhHs/kWhHi]": [result.hotwater_f_hs_hi],
        "Cooling_fuel_type": [result.cooling_fuel_type],
        "Cooling_f_GHG [g/kWhHi]": [result.cooling_f_ghg],
        "Cooling_f_PE [kWhPE/kWhHi]": [result.cooling_f_pe],
        "Cooling_f_Hs_Hi [kWhHs/kWhHi]": [result.cooling_f_hs_hi],
        "LightAppl_fuel_type": [result.light_appl_fuel_type],
        "LightAppl_f_GHG [g/kWhHi]": [result.light_appl_f_ghg],
        "LightAppl_f_PE [kWhPE/kWhHi]": [result.light_appl_f_pe],
        "LightAppl_f_Hs_Hi [kWhHs/kWhHi]": [result.light_appl_f_hs_hi],
        "HotWater_Sys_GWP [kg]": [result.hotwater_sys_gwp],
        "HotWater_Sys_GWP [kg/m2]": [result.hotwater_sys_gwp_surface],
        "HotWater_Sys_PE [kWh]": [result.hotwater_sys_pe],
        "HotWater_Sys_PE [kWh/m2]": [result.hotwater_sys_pe_surface],
        "ElectricityDemandTotal [kWh]": [result.electricity_demand_total],
        "ElectricityDemandTotal [kwh/m2]": [result.electricity_demand_total_surface],
        "FossilsDemandTotal [kWh]": [result.fossils_demand_total],
        "FossilsDemandTotal [kwh/m2]": [result.fossils_demand_total_surface],
        "LightingDemand [kWh]": [result.lighting_demand],
        "LightingDemand [kWh/m2]": [result.lighting_demand_surface],
        "LightingDemand_GWP [kg]": [result.lighting_demand_gwp],
        "LightingDemand_GWP [kg/m2]": [result.lighting_demand_gwp_surface],
        "LightingDemand_PE [kWh]": [result.lighting_demand_pe],
        "LightingDemand_PE [kWh/m2]": [result.lighting_demand_pe_surface],
        "Appliance_gains_demand [kWh]": [result.appliance_gains_demand],
        "Appliance_gains_demand [kWh/m2]": [result.appliance_gains_demand_surface],
        "Appliance_gains_elt_demand [kWh]": [result.appliance_gains_elt_demand],
        "Appliance_gains_elt_demand [kWh/m2]": [result.appliance_gains_elt_demand_surface],
        "Appliance_gains_demand_GWP [kg]": [result.appliance_gains_demand_gwp],
        "Appliance_gains_demand_GWP [kg/m2]": [result.appliance_gains_demand_gwp_surface],
        "Appliance_gains_demand_PE [kWh]": [result.appliance_gains_demand_pe],
        "Appliance_gains_demand_PE [kWh/m2]": [result.appliance_gains_demand_pe_surface],
        "GWP [kg]": [result.gwp],
        "GWP [kg/m2]": [result.gwp_surface],
        "PE [kWh]": [result.pe],
        "PE [kWh/m2]": [result.pe_surface],
        "FinalEnergy_Hi [kWhHi]": [result.final_energy_hi],
        "InternalGains [kWh]": [result.internal_gains],
        "InternalGains [kWh/m2]": [result.internal_gains_surface],
        "SolarGainsTotal [kWh]": [result.solar_gains_total],
        "SolarGainsTotal [kWh/m2]": [result.solar_gains_total_surface],
        "SolarGainsSouthWindow [kWh]": [result.solar_gains_south_window],
        "SolarGainsEastWindow [kWh]": [result.solar_gains_east_window],
        "SolarGainsWestWindow [kWh]": [result.solar_gains_west_window],
        "SolarGainsNorthWindow [kWh]": [result.solar_gains_north_window],
        "TransmissionLoss [kWh]": [result.transmission_loss],
        "TransmissionLoss [kWh/m2]": [result.transmission_loss_surface],
        "DeltaUThermalBridging [W/m2K]": [result.delta_u_thermal_bridging],
        "ThermalBridgeConductance [W/K]": [result.thermal_bridge_conductance],
        "ThermalBridgingLoss [kWh]": [result.thermal_bridging_loss],
        "ThermalBridgingLoss [kWh/m2]": [result.thermal_bridging_loss_surface],
        "VentilationLoss [kWh]": [result.ventilation_loss],
        "VentilationLoss [kWh/m2]": [result.ventilation_loss_surface],
        "HeatingPeriodHours [h]": [result.heating_period_hours],
        "HeatingDays [d]": [result.heating_days],
        "HeatingDegreeDays [K d]": [result.heating_degree_days],
        "RoomHeatingDegreeDays [K d]": [result.room_heating_degree_days],
        "GlobalHorizontalRadiationTotal [kWh/m2]": [result.global_horizontal_radiation_total],
        "DirectNormalRadiationTotal [kWh/m2]": [result.direct_normal_radiation_total],
        "DiffuseHorizontalRadiationTotal [kWh/m2]": [result.diffuse_horizontal_radiation_total],
        "GlobalHorizontalRadiationMean_Annual [Wh/m2]": [result.global_horizontal_radiation_mean_annual],
        "DirectNormalRadiationMean_Annual [Wh/m2]": [result.direct_normal_radiation_mean_annual],
        "DiffuseHorizontalRadiationMean_Annual [Wh/m2]": [result.diffuse_horizontal_radiation_mean_annual],
        "DrybulbTemperatureMean_Annual [C]": [result.drybulb_temperature_mean_annual],
        "HeatingPeriodHeatingDemand [kWh]": [result.heating_period_heating_demand],
        "HeatingPeriodHeatingDemand [kWh/m2]": [result.heating_period_heating_demand_surface],
        "HeatingPeriodCoolingDemand [kWh]": [result.heating_period_cooling_demand],
        "HeatingPeriodCoolingDemand [kWh/m2]": [result.heating_period_cooling_demand_surface],
        "HeatingPeriodHotWaterDemand [kWh]": [result.heating_period_hot_water_demand],
        "HeatingPeriodHotWaterDemand [kWh/m2]": [result.heating_period_hot_water_demand_surface],
        "HeatingPeriodHotWaterEnergy [kWhHs]": [result.heating_period_hot_water_energy],
        "HeatingPeriodHotWaterEnergy [kWhHs/m2]": [result.heating_period_hot_water_energy_surface],
        "HeatingPeriodElectricityDemandTotal [kWh]": [result.heating_period_electricity_demand_total],
        "HeatingPeriodElectricityDemandTotal [kWh/m2]": [result.heating_period_electricity_demand_total_surface],
        "HeatingPeriodInternalGains [kWh]": [result.heating_period_internal_gains],
        "HeatingPeriodInternalGains [kWh/m2]": [result.heating_period_internal_gains_surface],
        "HeatingPeriodLightingDemand [kWh]": [result.heating_period_lighting_demand],
        "HeatingPeriodLightingDemand [kWh/m2]": [result.heating_period_lighting_demand_surface],
        "HeatingPeriodAppliance_gains_demand [kWh]": [result.heating_period_appliance_gains_demand],
        "HeatingPeriodAppliance_gains_demand [kWh/m2]": [result.heating_period_appliance_gains_demand_surface],
        "HeatingPeriodAppliance_gains_elt_demand [kWh]": [result.heating_period_appliance_gains_elt_demand],
        "HeatingPeriodAppliance_gains_elt_demand [kWh/m2]": [result.heating_period_appliance_gains_elt_demand_surface],
        "HeatingPeriodSolarGainsTotal [kWh]": [result.heating_period_solar_gains_total],
        "HeatingPeriodSolarGainsTotal [kWh/m2]": [result.heating_period_solar_gains_total_surface],
        "HeatingPeriodSolarGainsSouthWindow [kWh]": [result.heating_period_solar_gains_south_window],
        "HeatingPeriodSolarGainsEastWindow [kWh]": [result.heating_period_solar_gains_east_window],
        "HeatingPeriodSolarGainsWestWindow [kWh]": [result.heating_period_solar_gains_west_window],
        "HeatingPeriodSolarGainsNorthWindow [kWh]": [result.heating_period_solar_gains_north_window],
        "HeatingPeriodTransmissionLoss [kWh]": [result.heating_period_transmission_loss],
        "HeatingPeriodTransmissionLoss [kWh/m2]": [result.heating_period_transmission_loss_surface],
        "HeatingPeriodThermalBridgingLoss [kWh]": [result.heating_period_thermal_bridging_loss],
        "HeatingPeriodThermalBridgingLoss [kWh/m2]": [result.heating_period_thermal_bridging_loss_surface],
        "HeatingPeriodVentilationLoss [kWh]": [result.heating_period_ventilation_loss],
        "HeatingPeriodVentilationLoss [kWh/m2]": [result.heating_period_ventilation_loss_surface],
        "HeatingPeriodGlobalHorizontalRadiationTotal [kWh/m2]": [result.heating_period_global_horizontal_radiation_total],
        "HeatingPeriodDirectNormalRadiationTotal [kWh/m2]": [result.heating_period_direct_normal_radiation_total],
        "HeatingPeriodDiffuseHorizontalRadiationTotal [kWh/m2]": [result.heating_period_diffuse_horizontal_radiation_total],
        "GlobalHorizontalRadiationMean_HeatingPeriod [Wh/m2]": [result.global_horizontal_radiation_mean_heating_period],
        "DirectNormalRadiationMean_HeatingPeriod [Wh/m2]": [result.direct_normal_radiation_mean_heating_period],
        "DiffuseHorizontalRadiationMean_HeatingPeriod [Wh/m2]": [result.diffuse_horizontal_radiation_mean_heating_period],
        "DrybulbTemperatureMean_HeatingPeriod [C]": [result.drybulb_temperature_mean_heating_period],
        "OccupancyProfilePeople_Mean_Annual [-]": [result.occupancy_profile_people_mean_annual],
        "OccupancyProfilePeople_Mean_HeatingPeriod [-]": [result.occupancy_profile_people_mean_heating_period],
        "ApplianceProfileFactor_Mean_Annual [-]": [result.appliance_profile_factor_mean_annual],
        "ApplianceProfileFactor_Mean_HeatingPeriod [-]": [result.appliance_profile_factor_mean_heating_period],
        "AirChangeRateEffective_Mean_Annual [1/h]": [result.air_change_rate_effective_mean_annual],
        "AirChangeRateEffective_Mean_HeatingPeriod [1/h]": [result.air_change_rate_effective_mean_heating_period],
        "AirFlowRateEffective_Mean_Annual [m3/h]": [result.air_flow_rate_effective_mean_annual],
        "AirFlowRateEffective_Mean_HeatingPeriod [m3/h]": [result.air_flow_rate_effective_mean_heating_period],
        "GebÃ¤udefunktion Hauptkategorie": [result.building_function_main_category],
        "GebÃ¤udefunktion Unterkategorie": [result.building_function_sub_category],
        "Profil SIA 2024": result.profile_sia_2024,
        "Profil 18599-10": result.profile_18599,
        "EPW-File": result.epw_file,
        "profile_from_norm": [result.profile_from_norm],
        "gains_from_group_values": [result.gains_from_group_values],
        "usage_from_norm": [result.usage_from_norm],
        "weather_period": [result.weather_period],
        "dibs_computing_core": [versions["dibs_computing_core"]],
        "dibs_datasource_csv": [versions["dibs_datasource_csv"]],
        "dibs_cli": [versions["dibs_cli"]],
        "dibs_data": [versions["dibs_data"]],
        "file_name": [file_name],
        "Time and date": [now],
    })


def convert_result_of_all_hours_to_dataframe(
        result: Result, building: Building, iteration: int
) -> pd.DataFrame:
    """
    Maps the hourly result of a simulated building to a dataframe.
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
            "ElectricityDemandTotal": result.electricity_demand_total,
            "IndoorAirTemperature": result.temp_air,
            "OutsideTemperature": result.outside_temp,
            "DrybulbTemperature": result.drybulb_temperature,
            "LightingDemand": result.lighting_demand,
            "InternalGains": result.internal_gains,
            "Appliance_gains_demand": result.appliance_gains_demand,
            "Appliance_gains_elt_demand": result.appliance_gains_elt_demand,
            "GlobalHorizontalRadiation": result.global_horizontal_radiation,
            "DirectNormalRadiation": result.direct_normal_radiation,
            "DiffuseHorizontalRadiation": result.diffuse_horizontal_radiation,
            "SolarGainsSouthWindow": result.solar_gains_south_window,
            "SolarGainsEastWindow": result.solar_gains_east_window,
            "SolarGainsWestWindow": result.solar_gains_west_window,
            "SolarGainsNorthWindow": result.solar_gains_north_window,
            "SolarGainsTotal": result.solar_gains_total,
            "TransmissionLoss": result.transmission_loss,
            "ThermalBridgingLoss": result.thermal_bridging_loss,
            "VentilationLoss": result.ventilation_loss,
            "OccupancyProfilePeople": result.occupancy_profile_people,
            "ApplianceProfileFactor": result.appliance_profile_factor,
            "AirChangeRateEffective": result.air_change_rate_effective,
            "AirFlowRateEffective": result.air_flow_rate_effective,
            "IsHeatingPeriodHour": result.is_heating_period_hour,
            "Daytime": result.DayTime,
            "iteration": iteration,
            "GebÃ¤udeID": building.scr_gebaeude_id,
        }
    )


def convert_heating_period_result_of_all_hours_to_dataframe(
        result: Result, building: Building, iteration: int
) -> pd.DataFrame:
    df = convert_result_of_all_hours_to_dataframe(result, building, iteration)
    return df[df["IsHeatingPeriodHour"]].reset_index(drop=True)


def save_results_of_all_buildings_hours_in_csv_parallel_using_thread_executor(
        buildings: list[Building], result: list[Result], folder_path: str
) -> float:
    """
    Saves hourly result files in csv format and returns the runtime.
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
        [future.result() for future in concurrent.futures.as_completed(futures)]

    end_saving_time = time.time()
    return end_saving_time - begin_saving_time


def build_all_results_of_all_buildings_to_dataframe(
        results: list[SummaryResult], file_name: str
) -> pd.DataFrame:
    list_of_results = [
        convert_end_result_to_dataframe(result, file_name) for result in results
    ]
    return pd.concat(list_of_results, ignore_index=True)


def save_buildings_all_hours_results_to_excel(
        result: Result, folder_path: str, building: Building, iteration: int
) -> None:
    """
    Saves the full-year hourly file and a heating-period-only hourly file.
    """
    full_year_df = convert_result_of_all_hours_to_dataframe(result, building, iteration)
    full_year_df.to_csv(
        rf"{folder_path}/{building.scr_gebaeude_id}.csv", index=False
    )

    heating_period_df = convert_heating_period_result_of_all_hours_to_dataframe(
        result, building, iteration
    )
    heating_period_df.to_csv(
        rf"{folder_path}/{building.scr_gebaeude_id}_heating_period.csv",
        index=False,
    )
