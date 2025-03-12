import re
from happi.item import EntryInfo, OphydItem
from happi.errors import EnforceError

class LCLSItem(OphydItem):
    name = EntryInfo(('Shorthand Python-valid name for the Python instance. '
                      'Must be between 3 and 80 characters.'),
                     optional=False,
                     enforce=re.compile(r'[a-z][a-z\_0-9]{2,78}$'))
    beamline = EntryInfo('Section of beamline the device belongs',
                         optional=False, enforce=str, default="FMS")
    location_group = EntryInfo('LUCID grouping parameter for location',
                               optional=False, enforce=str)
    functional_group = EntryInfo('LUCID grouping parameter for function',
                                 optional=False, enforce=str)
    z = EntryInfo('Beamline position of the device',
                  enforce=float, default=-1.0)
    stand = EntryInfo('Acronym for stand, must be three alphanumeric '
                      'characters like an LCLSI stand (e.g. DG3) or follow '
                      'the LCLSII stand naming convention (e.g. L0S04).',
                      enforce=re.compile(r'[A-Z0-9]{3}$|[A-Z][0-9]S[0-9]{2}$'))
    lightpath = EntryInfo("If the device should be included in the "
                          "LCLS Lightpath", enforce=bool, default=False)
    input_branches = EntryInfo(('List of branches the device can receive '
                                'beam from.'),
                               optional=True, enforce=list)
    output_branches = EntryInfo(('List of branches the device can deliver '
                                'beam to.'),
                                optional=True, enforce=list)
    ioc_engineer = EntryInfo(('Engineer for the IOC. Used to build IOC '
                             'configs.'),
                             optional=True, enforce=str)
    ioc_location = EntryInfo('Location of the IOC. Used to build IOC configs.',
                             optional=True, enforce=str)
    ioc_hutch = EntryInfo(('Hutch the IOC will be used in. Used to build IOC '
                           'configs.'), optional=True, enforce=str)
    ioc_release = EntryInfo(('Full path to IOC release directory. Used to '
                            'build IOC configs.'),
                            optional=True, enforce=str)
    ioc_arch = EntryInfo(('The IOC host architecture. Used to build IOC '
                         'configs.'), optional=True, enforce=str)
    ioc_name = EntryInfo('The name of the device IOC. Used to build the IOC.',
                         optional=True, enforce=str)
    ioc_type = EntryInfo(('The type of device IOC. Useful when multiple '
                          'device classes can occupy the same controller. Can '
                          'be used to tell higher level code how to interpret '
                          'the ioc data.'), optional=True, enforce=str)

class FMSSRCItem(LCLSItem):
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

class FMSItem(LCLSItem):
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
