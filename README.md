# Building Simulation CLI

This package provides the `dibs-cli` command for running DIBS building simulations
from CSV or Excel input files.

## Commands

- `dibs-cli simulate-one-building <path>`
- `dibs-cli simulate-all-building <path>`
- `dibs-cli simulate-buildings-with-batches <path>`

The optional flags remain:

- `--profile_from_norm`
- `--gains_from_group_values`
- `--usage_from_norm`
- `--weather_period`
- `--primary_energy_factor`
- `--summary_only`

Use `dibs-cli --help` to list all commands and options.

## Outputs

For each run, the CLI writes:

- `annualResults_summary.xlsx`
- one full-year hourly csv per building: `<BuildingID>.csv`
- one heating-period-only hourly csv per building: `<BuildingID>_heating_period.csv`

The summary workbook now includes:

- transmission and ventilation losses
- heating-period sums for heating, cooling, hot water, internal gains, lighting,
  appliance gains, electricity demand, and solar gains
- heating-day metrics (`HeatingDays`, `HeatingDegreeDays`, `RoomHeatingDegreeDays`)
- annual and heating-period raw weather diagnostics for:
  - global horizontal radiation
  - direct normal radiation
  - diffuse horizontal radiation
  - dry-bulb / outside temperature means
- annual and heating-period mean occupancy/appliance profile factors
- annual and heating-period mean effective air exchange diagnostics

The hourly csv exports now also include the raw weather input series used for
diagnosis:

- `DrybulbTemperature`
- `GlobalHorizontalRadiation`
- `DirectNormalRadiation`
- `DiffuseHorizontalRadiation`

## Input expectations

The input file must match the DIBS building schema, including the usual envelope,
window, thermal, ventilation, and system parameters.

Relevant window and ventilation fields include:

- `window_area_north`
- `window_area_east`
- `window_area_south`
- `window_area_west`
- `glass_solar_transmittance`
- `glass_solar_shading_transmittance`
- `ach_inf`
- `ach_win`
- `ach_vent`
- `heat_recovery_efficiency`

## Branch-linked development

For the cross-repository feature work on heating-period diagnostics, `pyproject.toml`
is pinned to:

- `dibs_computing_core@heating-period-diagnostics`
- `dibs_datasource_csv@heating-period-diagnostics`

## License

This project is licensed under the [MIT License](LICENSE).
