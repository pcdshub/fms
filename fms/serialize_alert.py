from dataclasses import dataclass, field
from typing import Optional, Dict, List
from apischema import deserialize, alias, serialize
import json
from datetime import datetime

@dataclass
class Evaluator:
    params: List[int] = field(default_factory=list) 
    type_: str = field(metadata=alias("type"), default="gt")

@dataclass
class Operator:
    type_: str = field(metadata=alias("type"), default="and")

@dataclass
class Query:
    params: List[str] = field(default_factory=list)

@dataclass
class Reducer:
    type_: str = field(metadata=alias("type"), default="avg")

@dataclass
class Provenance:
    provenance : str

@dataclass
class RelativeTimeRange:
    from_: int = field(metadata=alias("from"), default=300)
    to: int = field(default=0)

@dataclass
class Model:
    alias_: Optional[str] = field(metadata=alias("alias"), default="")
    aliasPattern : str = ""
    conditions: Optional[List] = field(default_factory=list)
    datasource : Dict[str, str] = field(default_factory=lambda:dict(type="sasaki77-archiverappliance-datasource", uid="000000002"))
    frequency: str = ""
    functions: list = field(default_factory=list)
    intervalMs: int = 1000
    maxDataPoints: int = 43200 
    operator: str = ""
    refId: str = ""
    regex: bool = False
    stream: bool = True
    strmCap: str = ""
    strmInt: str = ""
    target: str = ""
    type_: Optional[str] = field(metadata=alias("type"), default="")


@dataclass
class AlertQuery:
    datasourceUid : Optional[str] = "000000002"
    model : Optional[Model] = field(default=Model())
    queryType: Optional[str] = ""
    refId: Optional[str] = ""
    relativeTimeRange: Optional[RelativeTimeRange] = RelativeTimeRange()

@dataclass
class ProvisionedAlertRule:
    annotations: Optional[Dict[str, str]] = field(default_factory=dict) 
    condition: str = "B"
    data: List[AlertQuery] = field(default_factory=list)
    execErrState: str = "Alerting"
    folderUID: str = ""
    for_: str = field(metadata=alias("for"), default="1d")
    id_: Optional[int] = field(metadata=alias("id"), default=None)
    isPaused: Optional[bool] = False
    labels: Optional[Dict[str, str]] = field(default_factory=dict) 
    noDataState: str = "NoData"
    notification_settings: Optional[None] = field(default=None)
    orgID: int = 1 
    provenance: Optional[Provenance] = field(default=None) 
    record: Optional[None] = field(default=None)
    ruleGroup: str = ""
    title: str = ""
    uid: str = ""
    updated: Optional[str] = field(default=None) 