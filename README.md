# Building Simulation CLI

This Python program provides a command-line interface (CLI) for simulating buildings based on data provided in a CSV or
Excel file. The program offers two main commands (`simulate_one_building` and `simulate_all_building`) to simulate
individual buildings or multiple buildings simultaneously.

#### Usage

To execute the CLI, use the provided Python script `dibs-cli.py`. The program expects the path to the file containing
building data as the first argument. The remaining four arguments are optional and have default values. If the user only
provides the path argument, the program will use default values for the other arguments. If the user provides all five
arguments, the program will simulate using the user's input.

### Command `simulate_one_building`

The `simulate_one` command performs the simulation for a single building. The building data must be provided as a CSV or
Excel file and contain only one record.

### Command `simulate_all_building`

The `simulate_all` command performs the simulation for multiple buildings. The building data must be provided as a CSV
or Excel file and contain multiple records. Each record must match the same pattern and have the same number of
attributes as a building object.

### Arguments:

- `path`: Path to the file containing building data type of `str`. (Required)
- `ermi`: type of `str`. (Optional)
- `gains_from_group_values`: type of `str`. (Optional)
- `usage_from_norm`: type of `str`. (Optional)
- `weather_period`: type of `str`. (Optional)

### CSV File Format Requirements:

- The CSV or Excel file must contain a specific number of columns.
- The column names in the CSV or Excel file must match the attributes of the building object to be simulated.

#### Example Building Object:

Suppose we have a `Building` object with the following attributes:


Corresponding CSV or Excel File Columns:
To simulate this Building object, the CSV or Excel file must have the following columns:

- `scr_gebaeude_id`: Building Screening-ID.
- `plz`: Zipcode of building's location in Germany.
- `hk_geb`: Usage type (main category)
- `uk_geb`: Usage type (subcategory)
- `max_occupancy`: Max. number of building occupants at any given time
- `wall_area_og`: Area of all walls above ground in contact with the outside [m2]
- `wall_area_ug`: Area of all walls below ground in contact with soil [m2] 
- `window_area_north`: Area of the glazed surface in contact with the outside facing north [m2]
- `window_area_east`: Area of the glazed surface in contact with the outside facing east [m2]
- `window_area_south`: Area of the glazed surface in contact with the outside facing south [m2]
- `window_area_west`: Area of the glazed surface in contact with the outside facing west [m2]
- `roof_area`: Area of the roof in contact with the outside [m2]
- `net_room_area`: Area of all floor areas from usable rooms including all floor plan levels of the building (Refers
  to "Netto-Raumfläche", DIN 277-1:2016-01) [m2]
- `energy_ref_area`: Energy reference area of the building [m2]
- `base_area`: Area for the calculation of transmission heat losses to the soil. Also used to calculate the building's
  volume. [m2]
- `gross_base_area`: Gross base area of the building gross_base_area = base_area / 0.87 (currently unused)
- `building_height`: Mean height of the building [m]
- `net_volume`: Thermally conditioned net volum of building (air filled space within the building) (currently unused) [m3]
- `gross_volume`: Thermally conditioned gross volum of building (air filled space within the building) (currently unused) [m3]
- `envelope_area`: Total area of building envelope (currently unused) [m2]
- `lighting_load`: Lighting Load [W/m2]
- `lighting_control`: Lux threshold at which the lights turn on [Lx]
- `lighting_utilisation_factor`: A factor that determines how much natural solar lumminace is effectively utilised in
  the space
- `lighting_maintenance_factor`: A factor based on how dirty the windows area
- `aw_construction`: Exterior wall construction type (currently unused)
- `shading_device`: Type of shading device for transparent surfaces including windows (currently ununsed)
- `shading_solar_transmittance`: Shading transmittance reduction factor for solar gains (currently ununsed)
- `glass_solar_transmittance`: Solar radiation passing through the window (g-value)
- `glass_solar_shading_transmittance`: Solar radiation passing through the window with active shading devices
- `glass_light_transmittance`: Solar illuminance passing through the window
- `u_windows`: U value of glazed and/or transparent surfaces [W/m2K]
- `u_walls`: U value of external walls  [W/m2K]
- `u_roof`: U value of the roof [W/m2K]
- `u_base`: U value of the floor [W/m2K]
- `temp_adj_base`: Temperature adjustment factor for the floor
- `temp_adj_walls_ug`: Temperature adjustment factor for walls below ground
- `ach_inf`: Air changes per hour through infiltration [Air Changes Per Hour]
- `ach_win`: Air changes per hour through opened windows [Air Changes Per Hour]
- `ach_vent`: Air changes per hour through ventilation [Air Changes Per Hour]
- `heat_recovery_efficiency`: Efficiency of heat recovery
- `thermal_capacitance`: Thermal capacitance of the building [J/m2K]
- `t_set_heating`: Thermal heating set point [C]
- `t_start`: Indoor air temperatur for first time step of the simulation [C]
- `t_set_cooling`: Thermal cooling set point [C]
- `night_flushing_flow`: Air changes per hour through night flushing [Air Changes Per Hour]
- `max_heating_energy_per_floor_area`: Maximum heating load per floor area. Set to no.inf for unrestricted heating [C]
- `max_cooling_energy_per_floor_area`: Maximum cooling load. Set to -np.inf for unrestricted cooling [C]
- `heating_supply_system`: The type of heating system
- `cooling_supply_system`: The type of cooling system
- `heating_emission_system`: How the heat is distributed/emitted to the building
- `cooling_emission_system`: How the cooling energy is distributed/emitted to the building
- `dhw_system`: Type of hot water generator

### Example of Execution:

To simulate using default values for the optional arguments:

```bash
dibs-cli simulate-one-building /path/to/file.csv
```

To simulate using custom values for all arguments:

```bash
dibs-cli simulate-one-building /path/to/file.csv --profile_from_norm din18599 --gains_from_group_values mid --usage_from_norm sia2024 --weather_period 2007-2021
```

The below command will use the default values for `--profile_from_norm`, `--usage_from_norm`, and `--weather_period`, while using
the provided value for `--gains_from_group_values`.

```bash
dibs-cli simulate-one-building /path/to/file.csv --gains_from_group_values mid
```

### Calling for Help

To get help on the available commands and options, use the `--help` flag. For example:

```bash
dibs-cli --help
```

This will display an overview of the available commands and their options.

## License

This program is licensed under the [MIT License](LICENSE). See the license file for more information.
