from .grafana import create_alert_rule
from .serialize_alert import ProvisionedAlertRule, AlertQuery, Model, Evaluator, Operator, Reducer, Query, RelativeTimeRange
import json
def alert_creater():
    query_model = Model(
        alias_="test1",
        refId="A",
        target="MR1K2:SWITCH:MMS:XUP.RBV") 

    alert_query0 = AlertQuery(model=query_model, refId="A")

    query_model = Model(
        alias_="test1",
        refId="B",
        target="MR1K2:SWITCH:MMS:XDWN.RBV") 

    alert_query1 = AlertQuery(model=query_model, refId="B")

    classic_model = Model(
        alias_="test2",
        refId='C',
        conditions=[
            dict(
                evaluator=Evaluator(params=[850]),
                operator=Operator(type_="or"),
                query=Query(params=["A"]),
                reducer=Reducer()
            ),
            dict(
                evaluator=Evaluator(params=[1100]),
                operator=Operator(type_="or"),
                query=Query(params=["B"]),
                reducer=Reducer()
            )
        ],
        type_="classic_conditions") 

    classic_query = AlertQuery(
        model=classic_model,
        refId="C",
        datasourceUid="-100",
        relativeTimeRange=RelativeTimeRange(from_=0, to=0))

    alert = ProvisionedAlertRule(
        title="MR1K2 Test",
        ruleGroup="XRT Racks",
        folderUID="FRogdAwGz",
        data=[alert_query0, alert_query1, classic_query])
    
    #with open("test_serial_10.json", "w") as f:
        #f.write(json.dumps(alert.dict(by_alias=True)))
    create_alert_rule(json.dumps(alert.dict(by_alias=True)))

    #this works
    #with open("test_serial_10.json", "r") as f:
    #    create_alert_rule(f.read())