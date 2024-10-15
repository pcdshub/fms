import re
from happi.item import EntryInfo, HappiItem, OphydItem
from typing import List

class FMSSRCItem(OphydItem):
    port0 = EntryInfo("An ordered list of sensors on port 0", enforce=List[str])
    port1 = EntryInfo("An ordered list of sensors on port 1", enforce=List[str])
    port2 = EntryInfo("An ordered list of sensors on port 2", enforce=List[str])
    port3 = EntryInfo("An ordered list of sensors on port 3", enforce=List[str])
    port4 = EntryInfo("An ordered list of sensors on port 4", enforce=List[str])
    port5 = EntryInfo("An ordered list of sensors on port 5", enforce=List[str])
    port6 = EntryInfo("An ordered list of sensors on port 6", enforce=List[str])
    port7 = EntryInfo("An ordered list of sensors on port 7", enforce=List[str])

    port0CurrDist = EntryInfo("Total Distance to last sensor from switch from port N")
    port1CurrDist = EntryInfo("Total Distance to last sensor from switch from port N")
    port2CurrDist = EntryInfo("Total Distance to last sensor from switch from port N")
    port3CurrDist = EntryInfo("Total Distance to last sensor from switch from port N")
    port4CurrDist = EntryInfo("Total Distance to last sensor from switch from port N")
    port5CurrDist = EntryInfo("Total Distance to last sensor from switch from port N")
    port6CurrDist = EntryInfo("Total Distance to last sensor from switch from port N")
    port7CurrDist = EntryInfo("Total Distance to last sensor from switch from port N")

class FMSItem(OphydItem):
    high_alarm = EntryInfo("latching emergency alarm", enforce=int)
    moderate_alarm = EntryInfo("high warning alarm", enforce=int)
    low_alarm = EntryInfo("low warning alarm", enforce=int)
    bottom_alarm = EntryInfo("latching low emergency alarm", enforce=int)

    location = EntryInfo("wheres the device installed")

class FMSRaritanItem(FMSItem):
    def less_than_30(val):
        return val <= 30

    parent_switch = EntryInfo("The raritan switch", optional=False, enforce=str)

    root_sensor = EntryInfo("first sensor connected to raritan switch", optional=False, enforce=bool)    

    root_sensor_port = EntryInfo("switch port root sensor connected to 0-8", optional=(root_sensor != True), enforce=re.compile(r'[0-8]'))

    eth_dist_last = EntryInfo("Estimate the ethernet distance from last connection in meters",
    enforce_doc="must be less than 30 meters total from switch to last sensor", optional=False, enforce=less_than_30)

    last_connection = EntryInfo("Name of last connected sensor", optional=True, enforce=str)

class FMSBeckhoffItem(FMSItem):
    ek9k_rail = EntryInfo("The EK9K connected to this sensor")


