# Building Simulation CLI
This Python program provides a command-line interface (CLI) for simulating buildings with the [Dynamic ISO Building Simulator (DIBS)](https://iwugermany.github.io/dibs/) based on data provided in a CSV or Excel file. The program offers two main commands (`simulate_one_building` and `simulate_all_building`) to simulate individual buildings or multiple buildings (buildings stocks) simultaneously.

## Installation
To install the DIBS Command Line Interface (DibsCLI) use the following command:

```bash
pip install dibs_cli
```

To use the full DIBS [model](https://iwugermany.github.io/dibs/overview) it is recomended to install 
the [DibsCLI](https://github.com/IWUGERMANY/DibsCLI) package installs the full DIBS [model](https://iwugermany.github.io/dibs/overview) bundling the [DibsComputingCore](https://github.com/IWUGERMANY/DibsComputingCore), [DibsDataSourceCSV](https://github.com/IWUGERMANY/DibsDataSourceCSV) and the [DibsData](https://github.com/IWUGERMANY/DibsData). 



## Usage
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

## Further information
For a detailed installation guide and further information on DIBS see the [wiki](https://github.com/IWUGERMANY/DibsCLI/wiki) and the [DIBS Project Page](https://iwugermany.github.io/dibs/).

## How to cite
Please cite the Dynamic ISO Building Simulator (DIBS) as defined [here](https://iwugermany.github.io/dibs/contri).

## Legacy
The current Dynamic ISO Building Simulator (DIBS) is a PyPI package implementation of the initial [DIBS implementation](https://github.com/IWUGERMANY/DIBS---Dynamic-ISO-Building-Simulator) by Julian Bischof, Simon Knoll and Michael Hörner.


## License
This program is licensed under the [MIT License](LICENSE). See the license file for more information.

## Acknowledgement
The Dynamic ISO Building Simulator has been developed in context of the 'ENOB:DataNWG Forschungsdatenbank Nichtwohngebäude' (www.datanwg.de) project and the project 'FlexGeber - Demonstration of flexibility options in the building sector and their integration with the energy system in Germany' at Institut Wohnen und Umwelt (IWU), Darmstadt. The preparation of the publication as a [Python package on Pypi](https://pypi.org/project/dibs-computing-core/) was undertaken within the [EnOB:LezBAU](https://www.lezbau.de/) project, where the DIBS model provides the basis for the calculation of the operational energy within the LezBAU web tool.
<p float="left">
  <img src="https://github.com/IWUGERMANY/DibsComputingCore/blob/main/src/img/IWU_Logo.PNG" width="15%" /> 
</p>  

<b>ENOB:DataNWG<b>
<b>Funding code:</b>  Fkz.: 03ET1315  
<b>Project duration:</b>  01.12.2015 until 31.05.2021

<b>FlexGeber<b>
<b>Funding code:</b>  Fkz.: 03EGB0001  
<b>Project duration:</b>  01.10.2017 until 31.07.2022

<b>ENOB:LezBAU<b>
<b>Funding code:</b>  Fkz.: 03EN1074A
</br><b>Project duration:</b>  01.01.2023 until 31.12.2025
  
<b>All funded by:</b> 
<p float="left">
  <img src="https://github.com/IWUGERMANY/DibsComputingCore/blob/main/src/img/BMWi_Logo.png" width="30%" /> 
</p> 
in accordance with the parliamentary resolution of the German Parliament.
