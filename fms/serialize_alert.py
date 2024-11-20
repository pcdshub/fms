from dataclasses import dataclass, Field
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
import json
from datetime import datetime


class Evaluator(BaseModel):
    params: List[int] = Field(default_factory=list) 
    type_: str = Field(alias="type", default="gt")

    class Config:
        populate_by_name = True

class Operator(BaseModel):
    type_: str = Field(alias="type", default="and")

    class Config:
        populate_by_name = True

class Query(BaseModel):
    params: List[str] = Field(default_factory=list)

class Reducer(BaseModel):
    type_: str = Field(alias="type", default="avg")

    class Config:
        populate_by_name = True

class Provenance(BaseModel):
    provenance : str

class RelativeTimeRange(BaseModel):
    from_: int = Field(alias="from", default=300)
    to: int = Field(default=0)

    class Config:
        populate_by_name = True

class Model(BaseModel):
    alias_: Optional[str] = Field(alias="alias", default="")
    aliasPattern : str = ""
    conditions: Optional[List] = Field(default_factory=list)
    datasource : Dict[str, str] = Field(default_factory=lambda:dict(type="sasaki77-archiverappliance-datasource", uid="000000002"))
    frequency: str = ""
    functions: list = Field(default_factory=list)
    intervalMs: int = 1000
    maxDataPoints: int = 43200 
    operator: str = ""
    refId: str = ""
    regex: bool = False
    stream: bool = True
    strmCap: str = ""
    strmInt: str = ""
    target: str = ""
    type_: Optional[str] = Field(alias="type", default="")

    class Config:
        populate_by_name = True


class AlertQuery(BaseModel):
    datasourceUid : Optional[str] = "000000002"
    model : Optional[Model] = Field(default=Model())
    queryType: Optional[str] = ""
    refId: Optional[str] = ""
    relativeTimeRange: Optional[RelativeTimeRange] = RelativeTimeRange()

class ProvisionedAlertRule(BaseModel):
    annotations: Optional[Dict[str, str]] = Field(default_factory=dict) 
    condition: str = "B"
    data: List[AlertQuery] = Field(default_factory=list)
    execErrState: str = "Alerting"
    folderUID: str = ""
    for_: str = Field(alias="for", default="1d")
    id_: Optional[int] = Field(alias="id", default=None)
    isPaused: Optional[bool] = False
    labels: Optional[Dict[str, str]] = Field(default_factory=dict) 
    noDataState: str = "NoData"
    notification_settings: Optional[None] = Field(default=None)
    orgID: int = 1 
    provenance: Optional[str] = Field(default=None) 
    record: Optional[None] = Field(default=None)
    ruleGroup: str = ""
    title: str = ""
    uid: str = ""
    updated: Optional[str] = Field(default=None) 

    class Config:
        populate_by_name = True