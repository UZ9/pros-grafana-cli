import datetime
import json
import re

from prosgrafana.gui_data.db.sqlite_wrapper import SQLiteWrapper

# Headers are responsible for differentiating information coming from the V5 brain. Based on a header, the data can
# be used as a configuration, raw data for a graph/display, or as a logging statement. For sending configuration
# data, sometimes the data is too large for the VexOS buffer and needs to be broken into chunks. To solve this,
# data is placed in a buffer, where the program will wait until an entire concatenated bytearray contains both
# CONFIG_HEADER and CONFIG_END_HEADER. In the future, the data strings will also need to be put in a similar buffer.
#
# DATA_HEADER - Found at the beginning of a statement containing variable data
# CONFIG_HEADER - Found at the beginning of a configuration message
# CONFIG_END_HEADER - Found at the end of a configuration message
DATA_HEADER = "GUI_DATA_8378"
CONFIG_HEADER = "GUI_DATA_CONF_8378"
CONFIG_END_HEADER = "GUI_DATA_CONF_3434_END"


class ChartManager:
    """
    Responsible for parsing data from the V5 brain and writing it to the SQLite file.
    """

    class Status:
        """
        Represents the current status of the ChartManager.

        STOPPED - The ChartManager is currently not functioning
        AWAITING_CONFIGURATION - The ChartManager is waiting to receive both the CONFIG_HEADER and CONFIG_END_HEADER
        RECEIVING_DATA - The ChartManager has received the configuration, and is now actively listening for any new
                         data coming through
        """
        STOPPED = 0
        AWAITING_CONFIGURATION = 1
        RECEIVING_DATA = 2

    def __init__(self):
        self.status = self.Status.AWAITING_CONFIGURATION
        self.config_string = ""
        self.config_json = None
        self.db = None
        self.table = None

        return

    def parse(self, gui_application, raw_data_string):
        """
        Parses an incoming raw string from the V5 brain.

        @param gui_application: The current GUIApplication, used for sending data back to the brain
        @param raw_data_string: The data string received from the V5 brain to be parsed
        """
        try:
            header, data = self.__parse_data(raw_data_string)

            # If the header was unable to be parsed, it's likely a normal debug statement. In this case, we just print
            # it in the same way a Terminal would.
            if header == "" or data == "":
                gui_application.console.write(raw_data_string)
                return

            if self.status == self.Status.AWAITING_CONFIGURATION:
                if data.strip().endswith(CONFIG_END_HEADER):
                    # The program has found the end of the configuration data, append the last bit excluding the end
                    # header string
                    self.config_string += data[0:-(len(CONFIG_END_HEADER) + 1)]

                    self.config_json = json.loads(self.config_string)

                    columns = {}

                    # To add each chart element to a new SQLite table, we need to assign it a variable type of REAL
                    # (REAL is a floating point number in SQLite)
                    for chart in self.config_json:
                        columns[chart] = "REAL"

                    # Initialize the database and open a connection
                    self.db = SQLiteWrapper("guidata")
                    self.db.open()

                    # Create the table
                    self.db.begin()
                    self.table = self.db.create_table("data", time="text", **columns)
                    self.db.commit()

                    self.status = self.Status.RECEIVING_DATA
                    return
                else:
                    # The program hasn't found the end configuration header yet, keep appending any new information
                    self.config_string += re.sub('\n', '', self.config_string)
                    return
            elif self.status == self.Status.RECEIVING_DATA:
                if header.strip() == DATA_HEADER:
                    data_json = json.loads(data)

                    data_values = []

                    # As the JSON will be loaded in the same order everytime, we can simply loop through each json item
                    # and append it to data_values, a list of floats ready to be sent to the SQLite table.
                    for key, value in data_json.items():
                        data_values.append(value)

                    # Insert a new record containing the data_values information
                    self.db.begin()

                    # Retrieve a datetime with the RFC3339 format
                    date = datetime.datetime.utcnow()
                    date_str = date.isoformat("T") + "Z"
                    
                    self.table.insert_row(date_str, *data_values)
                    self.db.commit()
                    return
        except TypeError:
            return

    def __parse_data(self, raw_data_string):
        """
        Parses a raw data string into its header and data components @param raw_data_string: @return: The header and
        data parsed from the raw_data_string. If the parse was unsuccessful, the method will return none.
        """

        split = raw_data_string.split("|")

        # We need to have at least 2 elements when splitting off of '|'
        if len(split) != 2:
            return "", ""

        # Split into header and data components
        header = split[0]  # Contains the file header
        data = split[1]  # Contains the JSON data

        return header, data
