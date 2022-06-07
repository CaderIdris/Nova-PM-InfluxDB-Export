""" Contains classes and methods that write data to InfluxDB v2.0
database

Communicates with InfluxDB 2.0 instance, location specified by config
file and writes data to it synchronously. It accepts data in varying
formats (TBD, currently only accepts list of jsons)

    Classes:
        InfluxWriter: Handles connection to InfluxDB 2.0 database and
        writes data to it

"""

__author__ = "Idris Hayward"
__copyright__ = "2021, Idris Hayward"
__credits__ = ["Idris Hayward"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.0"
__maintainer__ = "Idris Hayward"
__email__ = "CaderIdrisGH@outlook.com"
__status__ = "Stable Release"

from influxdb_client import InfluxDBClient, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxWriter:
    """ Handles connection to InfluxDB 2.0 database and writes data to
    it

    An instance of this class connects to an InfluxDB 2.0 database,
    with all connection and authentication info passed to it via a
    config file. Once connection is established, data can be writted to
    the database via a variety (tbd, currently only accepts list of
    jsons) of methods depending on format

    Attributes:
        config (dict): Contains all information needed to connect and
        write data to InfluxDB 2.0 database

        client (InfluxDBClient): Instance of an InfluxDBClient which
        handles the connection to the database

        write_client (InfluxDBClient): Subinstance of client, handles
        writing daya to the database

    Methods:
        write_container_list (list): Writes list of containers to an
        InfluxDB 2.0 database
    """
    def __init__(self, influx_config):
        """ Initialises class and connects to InfluxDB 2.0 database

            Keyword arguments:
                influx_config (dict): Contains all info relevant to
                connecting to InfluxDB database. The following keys
                are required:
                    - "Influx Bucket": The bucket to send data to
                    - "Influx IP": The IP address of the influxdb
                                   database, 'localhost' if on same
                                   machine
                    - "Influx Port": Port of InfluxDB database,
                                     usually 8086
                    - "Influx Token": User token used to authorise
                                      connection
                    - "Influx Organisation": The organisation the
                                             user belongs to


        """
        self.config = influx_config
        self.client = InfluxDBClient(url=f'http://{self.config["Influx IP"]}' \
            f':{self.config["Influx Port"]}', token=self.config["Influx Token"],
            org=self.config["Influx Organisation"],
            timeout=150000)
        self.write_client = self.client.write_api(write_options=SYNCHRONOUS)

    def write_container_list(self, list_of_containers):
        """ Writes list of containers to an InfluxDB 2.0 database

        Takes list of containers as input and writes it. The containers
        must have the following keys:
            - "time": Measurement time, in datetime format
            - "measurement": The name of the measurement in the bucket
            - "fields": Measurements made at "time"
            - "tags": Tags corresponding to the particular measurement
                      e.g Sensor ID, measurement flag (Valid etc)

        """
        self.write_client.write(self.config["Influx Bucket"],
            self.config["Influx Organisation"],
            list_of_containers)
