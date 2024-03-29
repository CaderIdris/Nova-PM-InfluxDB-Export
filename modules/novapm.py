""" Takes csv file containing Nova PM data and parses it into a list of json
format readable by InfluxDB v2.0

CSV files generated by Nova PM sensors are read and formatted in one of two
ways depending on the format of the file. The old format used 8 columns,
the new format uses 4. The result is a list of jsons which can be read by
an InfluxDB v2.0 database, regardless of whether it's old or new.

Classes:
    NovaPM:
        Reads csv file generated by NovaPM and parses it in to a list
        of jsons

"""

__author__ = "Idris Hayward"
__copyright__ = "2021, Idris Hayward"
__credits__ = ["Idris Hayward"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.0"
__maintainer__ = "Idris Hayward"
__email__ = "CaderIdrisGH@outlook.com"
__status__ = "Stable Release"

import datetime as dt

class NovaPM:
    """ Reads csv file generated by Nova PM sensor and parses it in to a 
    list of jsons

    This class takes in the measurements stored in a csv file that were
    made by a Nova PM sensor and converts it into a list of jsons which can
    be read by an InfluxDB v2.0 database.

    Attributes:
        path (str): Absolute path to the csv file

        data_present (bool): Does the csv contain measurements?
        
        column_number (int): Number of columns in csv

        json_list (list): List of jsons, formatted for InfluxDB v2.0

        csv_data (list): CSV data, each element represents a line

    Methods:
        old_format: Formats the old format csv files

        new_format: Formats the new format csv files

    """
    def __init__(self, file_path):
        """ Initialises class, determines whether data is present in the csv
        and how many columns there are and then stores rows as elements in a
        list

        Keyword Arguments:
            file_path (str): Absolute path to the csv file
        """
        self.path = file_path
        self.data_present = True
        self.column_number = 0
        self.json_list = list()

        # Import data
        with open(self.path, "r") as csv:
            self.csv_data = csv.readlines()

        # If file is empty
        if len(self.csv_data) <= 1:
            self.data_present = False

        # 4 column (new) or 8 (old)?
        if self.data_present:
            first_line = self.csv_data[0]
            self.column_number = len(first_line.split(','))

    def old_format(self):
        """ Takes the old format csv file and parses the measurements in
        to json_list
        """
        # The old 8 column format
        for line in self.csv_data[1:]:
            if line[-1] == '\n':
                line = line[:-1]
            split_data = line.split(',')
            try:
                # With microseconds
                measurement_time = dt.datetime.strptime(split_data[7], 
                        '"%Y-%m-%d %H:%M:%S.%f%z"')        
            except ValueError:
                # Without microseconds
                measurement_time = dt.datetime.strptime(split_data[7], 
                        '"%Y-%m-%d %H:%M:%S%z"')
            # -8 hours to correct to GMT as the sensor thinks it's in China
            # but it's in London
            try:
                measurement_container = {
                    "time": measurement_time,
                    "measurement": "Nova PM",
                    "fields": {
                        "PM2.5": float(split_data[5]),
                        "PM10": float(split_data[4]),
                        "Latitude": float(split_data[2]),
                        "Longitude": float(split_data[3]),
                        "Speed": float(split_data[6])
                        },
                    "tags": {
                        "Car": split_data[0],
                        "Serial Number": split_data[1]
                        }
                    }
                self.json_list.append(measurement_container)
            except ValueError:
                pass

    def new_format(self):
        """ Takes the new format csv file and parses the measurements in
        to json_list
        """
        # The old 8 column format
        for line in self.csv_data[1:]:
            if line[-1] == '\n':
                line = line[:-1]
            split_data = line.split(',')
            try:
                # With microseconds
                measurement_time = dt.datetime.strptime(split_data[0], 
                        '%Y-%m-%dT%H:%M:%S.%f%z') - dt.timedelta(hours=8)        
            except ValueError:
                # Without microseconds
                measurement_time = dt.datetime.strptime(split_data[0], 
                        '%Y-%m-%dT%H:%M:%S%z') - dt.timedelta(hours=8)
            # -8 hours to correct to GMT as the sensor thinks it's in China
            # but it's in London
            try:
                measurement_container = {
                    "time": measurement_time,
                    "measurement": "Nova PM",
                    "fields": {
                        "PM2.5": float(split_data[2]),
                        "PM10": float(split_data[3]),
                        },
                    "tags": {
                        "Serial Number": split_data[1]
                        }
                    }
                self.json_list.append(measurement_container)
            except ValueError:
                pass
