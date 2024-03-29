Nova PM Sensor Export
---

**Stable Release**

**Joe Hayward (j.d.hayward@surrey.ac.uk)**

**COPYRIGHT 2021, Joe Hayward**

**GNU General Public License v3.0**

This program was designed, tested and run on Ubuntu 21.04. It will very likely run on other Linux distributions though it has not been tested. This program has not been tested on Windows or MacOS.

This program is designed to read csv files generated by Nova PM sensors that were downloaded from a website, in collaboration with external partners. The data is not publicly available currently to our knowledge.

---

## Table of Contents

1. [Standard Operating Procedure](#standard-operating-procedure)
2. [Settings](#settings)
3. [Setup](#setup)
4. [API](#api)
5. [Components](#components)

---

## Standard Operating Procedure

### Terminal

This program is initialised via the terminal:
- `bash run.sh` or `./run.sh` 
Once the program is initialised, the opening blurb will show. If Debug Stats is set to true, it will display all information contained in config.json

---

## Settings

### config.json

config.json contains several configurable parameters for the program:
- `"File Path"`: Absolute path to the data, do not end with a /
- `"Debug Stats"`: Boolean value (`true/false`). Will output config.json to terminal if true
- `"Influx Bucket"`: Name of InfluxDB v2.0 bucket to export measurements to
- `"Influx IP"`: IP address of InfluxDB v2.0 instance ("localhost" if hosted on same machine)
- `"Influx Port"`: Port of InfluxDB v2.0 instance (Usually 8086)
- `"Influx Token"`: User token to authorise communications with database
- `"Influx Organisation"`: Organisation the token falls under

---

## Setup

### Step 1: Download program from Github

Navigate to the directory you want to store the program in and run `git clone https://github.com/Joppleganger/Nova-PM-Sensor-Export.git`

### Step 2: Run setup script

`bash venv_setup.sh` or `./venv_setup.sh` runs the setup script, installing the virtual environment needed to run the program

---

## API

### [main.py](./main.py)
The main script for running the program, utilises modules found in [modules](./modules/) using config specified in [Settings](./Settings)

#### Command line arguments:

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|-c / --config|`str`|Alternate path to config file, use `/` in place of `\`|N|Settings/config.json|

#### Functions

##### fancy_print

Makes console output nicer

###### Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*str_to_print*|`str`|String that gets printed to console|Y|None|
|*length*|`int`|Character length of output|N|70|
|*form*|`str`|Output type (listed below)|N|NORM|
|*char*|`str`|Character used as border, should only be 1 character|N|\U0001F533 (White box emoji)|
|*end*|`str`|Appended to end of string, should be `\n` unless output is to be overwritten, then use `\r`|N|\n|
|*flush*|`bool`|Flush the output stream?|N|False|

**Valid options for _form_**
| Option | Description |
|---|---|
|TITLE|Centres the string, one *char* at start and end|
\NORM|Left aligned string, one *char* at start and end|
|LINE|Prints line of *char* of specified *length*|

##### get_json

Open  json file and return as dict

###### Keyword arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*path_to_json*|`str`|The path to the json file, can be relative e.g Settings/config.json|Y|None|

###### Returns

`dict` containing contents of json file

###### Raises

|Error Type|Cause|
|---|---|
|`FileNotFoundError`|File is not present|
|`ValueError`|Formatting error in json file, e.g ' used instead of " or comma after last item| 

### [novapm.py](./modules/novapm.py)

Takes `CSV` file containing Nova PM data and parses it into a `list` of `dicts` readable by InfluxDB v2.x

#### Classes

##### NovaPM

Reads csv file generated by Nova PM sensor and parses it into a list of jsons

###### Keyword arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*file_path*|`str`|Path to the file|Y|None|

###### Attributes

| Attribute | Type | Description |
|---|---|---|
|*path*|`str`|Absolute path to the csv file|
|*data_present*|`bool`|Does the csv contain measurements?|
|*column_number*|`int`|Number of columns in the csv, should always be 4 or 8|
|*json_list*|`list`|`List` of `dicts`, formatted for InfluxDB 2.x|
|*csv_data*|`list`|CSV data, each element represents a row|

###### Methods

**old_format**

Takes the 8 column csv file, reformats the measurements and stores them in *json_list*

- Keyword arguments

None

- Returns

None

**new_format**

Takes the 4 column csv file, reformats the measurements and stores them in *json_list*

- Keyword arguments

None

- Returns

None

### [influxwrite.py](./modules/influxwrite.py)

Contains functions and classes pertaining to writing data to InfluxDB 2.x database

#### Classes

##### InfluxWriter

Handles connection and export to InfluxDB 2.x database

###### Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*influx_config*|`dict`|Contains all info relevant to connecting to InfluxDB database|

###### Attributes

| Attribute | Type | Description |
|---|---|---|
|*config*|`dict`|Config info for InfluxDB 2.x database|
|*client*|`InfluxDBClient`|Client object for InfluxDB 2.x database|
|*write_client*|`InfluxDBClient.write_api`|Write client object for InfluxDB 2.x database|

###### Methods

**write_container_list**

Writes list of measurement containers to InfluxDB 2.x database, synchronous write used as asynchronous write caused memory issues on a 16 GB machine.

- Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*list_of_containers*|`list`|Exports list of data containers to InfluxDB 2.x database|

Containers must have the following keys:
|Key|Description|
|---|---|
|*time*|Measurement time in datetime format|
|*measurement*|Name of measurement in the bucket|
|*fields*|Measurements made at *time*|
|*tags*|Metadata for measurements made at *time*|

- Returns
None

---

## Example data

The following is an example of the two csv file formats.

### Old format

|car_no|sn|lat|lng|pm10|pm2_5|speed|time|
|---|---|---|---|---|---|---|---|
|C008-0001|C008-0001|*N/A*|*N/A*|20.9|16.0|0.0|"2020-01-10 09:30:00.711000+08:00"
|C008-0003|C008-0003|*N/A*|*N/A*|21.1|16.6|0.0|"2020-01-10 09:30:02.961000+08:00"

Headings:
- **car_no**: Car number (The sensors were referred to as cars), acts as an identifier for the sensor. Files contained multiple "cars"
- **sn**: Serial number of sensor, functionally identical to **car_no**
- **lat**: Latitude coordinate, redacted here
- **lng**: Longitude coordinate, redacted here
- **pm10**: PM<sub>10</sub> measurement in μg m<sup>-3</sup>
- **pm2_5**: PM<sub>2.5</sub> measurement in μg m<sup>-3</sup>
- **speed**: Speed sensor is moving in km/h
- **time**: Timestamp in `YYYY-MM-DD HH:MM:SS.ffffff+TZ` format, unless the measurement was made exactly on the second in which case it's `YYYY-MM-DD HH:MM:SS+TZ`. Timezone was set to China despite sensor being located in London, so -8 hour correction is made in the program 

### New format

|time|sn|pm25|pm10|
|---|---|---|---|
|2020-04-17T20:39:25.182+08:00|C008-0001|8.5|25.2|
|2020-04-17T20:39:28.151+08:00|C008-0001|8|20.3|

Headings:
- **sn**: Serial number of sensor, sensors now split in to different files
- **pm10**: PM<sub>10</sub> measurement in μg m<sup>-3</sup>
- **pm2_5**: PM<sub>2.5</sub> measurement in μg m<sup>-3</sup>
- **time**: Timestamp in `YYYY-MM-DDTHH:MM:SS.ffffff+TZ` format, unless the measurement was made exactly on the second in which case it's `YYYY-MM-DDTHH:MM:SS+TZ`. Timezone was set to China despite sensor being located in London, so -8 hour correction is made in the program 
