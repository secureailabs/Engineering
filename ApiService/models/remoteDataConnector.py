from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, StrictStr
from models.common import PyObjectId


class DatasetInfo(BaseModel):
    DatasetUuid: StrictStr = Field(...)


class RemoteDataConnector_Base(BaseModel):
    Identifier: StrictStr = Field(...)
    Datasets: List[DatasetInfo] = Field(...)
    Version: StrictStr = Field(...)


class RemoteDataConnector_db(RemoteDataConnector_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    registerTime: datetime = Field(default_factory=datetime.utcnow)


class RegisterRemoteDataConnector_In(RemoteDataConnector_Base):
    pass


class RegisterRemoteDataConnector_Out(RemoteDataConnector_Base):
    id: PyObjectId = Field(...)


class GetRemoteDataConnectors_Out(RemoteDataConnector_Base):
    pass


class UpdateRemoteDataConnector_In(RemoteDataConnector_Base):
    pass


class HeartbeatRemoteDataConnector_In(BaseModel):
    RemoteDataConnectorGuid: StrictStr = Field(...)


class VirtualMachinesWaiting(BaseModel):
    VirtualMachineUuid: StrictStr = Field(...)
    DatasetGuid: StrictStr = Field(...)
    IPAddress: StrictStr = Field(...)


class HeartbeatRemoteDataConnector_Out(BaseModel):
    VirtualMachines: List[VirtualMachinesWaiting] = Field(...)
