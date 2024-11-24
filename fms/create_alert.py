from .grafana import create_alert_rule
from .serialize_alert import ProvisionedAlertRule, AlertQuery, Model, Evaluator, Operator, Reducer, Query, RelativeTimeRange
from happi import Client
from happi.errors import DuplicateError
import json

fms_happi_database = "fms_test.json"

folder_uid = dict(xrt="FRogdAwGz")
rule_groups = dict(xrt_racks="XRT Racks", xrt_pcw="XRT_PCW", xrt_flood="XRT Water Leak Detection")

class AlertCreater:
    def create_alert(self, value, *, alert_title=None, folder_name=None, rule_group=None, polarity="gt",pv=None, happi_name=None, client=None):

        alias = ""
        target = ""
        if pv == None and happi_name == None:
            raise ValueError("Must include PV or Happi Name")
        elif alert_title == None:
            raise ValueError("Must include alert_title")
        elif folder_name not in folder_uid:
            valid_folders = ",\n".join(folder_uid.keys())
            raise ValueError("Must include valid folder name, options:\n" + valid_folders)
        elif rule_group not in rule_groups:
            valid_groups = ",\n".join(rule_groups.keys())
            raise ValueError("Must include valid rule group, options:\n" + valid_groups)
        elif rule_group not in rule_groups:
            raise ValueError("Must include valid rule group {rule_groups}")
        
        if happi_name != None:
            #make an alert base on happi item.
            if client == None:
                client = Client(path=fms_happi_database)
                item = client.find_item(happi_name)

            if item.alert_rule_id != None:
                raise DuplicateError("alert uid already exists, update alert instead")

            alias = item.name
            target = item.prefix
        else:
            #make an alert with a PV.
            target = pv

        query_model = Model(
            alias_=alias,
            refId="A",
            target=target) 

        alert_query0 = AlertQuery(model=query_model, refId="A")

        classic_model = Model(
            alias_="classic",
            refId='B',
            conditions=[
                dict(
                    evaluator=Evaluator(params=[value, 0]),
                    operator=Operator(type_=""),
                    query=Query(params=["A"]),
                    reducer=Reducer()
                )
            ],
            type_="classic_conditions") 

        classic_query = AlertQuery(
            model=classic_model,
            refId="B",
            datasourceUid="-100",
            relativeTimeRange=RelativeTimeRange(from_=0, to=0)
        )
        
        alert = ProvisionedAlertRule(
            title=alert_title,
            ruleGroup=rule_groups[rule_group],
            folderUID=folder_uid[folder_name],
            condition= 'B',
            data=[alert_query0, classic_query])

        create_alert_rule(json.dumps(alert.dict(by_alias=True)))

    def create_summary_alert():
        query_model = Model(
            alias_="test1",
            refId="A",
            target="MR1K2:SWITCH:MMS:XUP.RBV") 

        alert_query0 = AlertQuery(model=query_model, refId="A")

        query_model = Model(
            alias_="test2",
            refId="B",
            target="MR1K2:SWITCH:MMS:XDWN.RBV") 

        alert_query1 = AlertQuery(model=query_model, refId="B")
        classic_model = Model(
            alias_="test2",
            refId='C',
            conditions=[
                dict(
                    evaluator=Evaluator(params=[850, 0]),
                    operator=Operator(type_="or"),
                    query=Query(params=["A"]),
                    reducer=Reducer()
                ),
                dict(
                    evaluator=Evaluator(params=[1100, 0]),
                    operator=Operator(type_="or"),
                    query=Query(params=["B"]),
                    reducer=Reducer()
                ),
            ],
            type_="classic_conditions") 

        classic_query = AlertQuery(
            model=classic_model,
            refId="C",
            datasourceUid="-100",
            relativeTimeRange=RelativeTimeRange(from_=0, to=0)
        )
        
        alert = ProvisionedAlertRule(
            title="MR1K2 Test",
            ruleGroup="XRT Racks",
            folderUID="FRogdAwGz",
            condition= 'C',
            data=[alert_query0, alert_query1, classic_query])
        
        create_alert_rule(json.dumps(alert.dict(by_alias=True)))