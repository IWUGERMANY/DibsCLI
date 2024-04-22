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
