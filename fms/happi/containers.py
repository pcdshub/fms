import re
from happi.item import EntryInfo, HappiItem, OphydItem
from happi.errors import EnforceError
from typing import List

class FMSSRCItem(OphydItem):
    port0 = EntryInfo("An ordered list of sensors on port 0", enforce=str)
    port1 = EntryInfo("An ordered list of sensors on port 1", enforce=str)
    port2 = EntryInfo("An ordered list of sensors on port 2", enforce=str)
    port3 = EntryInfo("An ordered list of sensors on port 3", enforce=str)
    port4 = EntryInfo("An ordered list of sensors on port 4", enforce=str)
    port5 = EntryInfo("An ordered list of sensors on port 5", enforce=str)
    port6 = EntryInfo("An ordered list of sensors on port 6", enforce=str)
    port7 = EntryInfo("An ordered list of sensors on port 7", enforce=str)

class FMSItem(OphydItem):
    high_alarm = EntryInfo("latching emergency alarm", enforce=int)
    moderate_alarm = EntryInfo("high warning alarm", enforce=int)
    low_alarm = EntryInfo("low warning alarm", enforce=int)
    bottom_alarm = EntryInfo("latching low emergency alarm", enforce=int)

    location = EntryInfo("wheres the device installed")

class FMSRaritanItem(FMSItem):


    def less_than_100(val):
        if int(val) <= 100:
            return val 
        else:
            raise(EnforceError)

    def regex_match_or_none(val):
        if val == re.compile(r'^[0-8]$') or None:
            return val
        else:
            raise(EnforceError)
    root_sensor_port = EntryInfo("switch port root sensor connected to 0-8", optional=True, default=None, enforce=re.compile(r'^[0-8]$'))

    parent_switch = EntryInfo("The raritan switch", optional=False, enforce=str)

    eth_dist_last = EntryInfo("Estimate the ethernet distance from last connection in feet",
    enforce_doc="must be less than 100 feet total from switch to last sensor", optional=False, enforce=less_than_100)

    last_connection_name = EntryInfo("Name of last connected sensor or leave blank for first", enforce=str)

class FMSBeckhoffItem(FMSItem):
    ek9k_rail = EntryInfo("The EK9K connected to this sensor")


