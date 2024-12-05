import re
from happi.item import EntryInfo, HappiItem, OphydItem
from happi.errors import EnforceError

class FMSSRCItem(OphydItem):
    port0 = EntryInfo("An ordered list of sensors on port 0", enforce=list)
    port1 = EntryInfo("An ordered list of sensors on port 1", enforce=list)
    port2 = EntryInfo("An ordered list of sensors on port 2", enforce=list)
    port3 = EntryInfo("An ordered list of sensors on port 3", enforce=list)
    port4 = EntryInfo("An ordered list of sensors on port 4", enforce=list)
    port5 = EntryInfo("An ordered list of sensors on port 5", enforce=list)
    port6 = EntryInfo("An ordered list of sensors on port 6", enforce=list)
    port7 = EntryInfo("An ordered list of sensors on port 7", enforce=list)

    location = EntryInfo("wheres the device installed")

    captar_in = EntryInfo("Inbound captar number", enforce=str )
    captar_out = EntryInfo("Outbound captar number", enforce=str )

class FMSItem(OphydItem):
    high_alarm = EntryInfo("latching emergency alarm", enforce=int)
    moderate_alarm = EntryInfo("high warning alarm", enforce=int)
    low_alarm = EntryInfo("low warning alarm", enforce=int)
    bottom_alarm = EntryInfo("latching low emergency alarm", enforce=int)

    location = EntryInfo("wheres the device installed")
    alert_rule_id = EntryInfo("the alert rule linked to this item in grafana", default=None)

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

    num_sensors = EntryInfo("DX2-T1H1: 3, DX2-T1: 1, DX2-WSC: 1", optional=False, enforce=int)

    captar_in = EntryInfo("Inbound captar number", enforce=str )
    captar_out = EntryInfo("Outbound captar number", enforce=str )
