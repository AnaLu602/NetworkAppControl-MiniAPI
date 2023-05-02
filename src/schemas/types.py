from typing import Optional, List
from pydantic import BaseModel, Field, Extra

class ConfigBaseModel(BaseModel):
    
    class Config:
        extra = Extra.forbid

class NetworkAppInfo(ConfigBaseModel):
    name: str = Field("Autonomous Driving NetworkApp")
    version: str = Field("3.2.1")
    manufacturer: str = Field("ACME Corporation")
    maxStreams: int = Field(50, description="maximum number of simultaneous streams that can be created", ge=1)
    maxTotalBandwidthDown: int = Field(300000, description="Maximum total bandwidth that can be configured for downstream (from NetworkApp to UE), in kilobits per second (1 kbit/s = 1024 bits/s)", ge=100)
    maxTotalBandwidthUp: int = Field(300000, description="Maximum total bandwidth that can be configured for upstream (from UE to NetworkApp), in kilobits per second (1 kbit/s = 1024 bits/s)", ge=100)

class StreamConfig(ConfigBaseModel):
    """configuration parameters for streams; note that in future versions, additional parameters such as protocol type (http, https, etc.), object length, burstiness parameters could be added"""
    id: Optional[int]
    numberofStreams: int = Field(50, description="number of simultaneous streams to be created", ge=1)
    tputTotalDown: int = Field(300000, description="Total bandwidth per second to be sent downstream (from NetworkApp to UE), in kilobits per second; this is split between the number of streams configured", ge=0)
    tputTotalUp: int = Field(300000, description=" Total bandwidth per second to be sent upstream (from UE to NetworkApp), in kilobits per second; this is split between the number of streams configured", ge=0)

    class Config:
        orm_mode = True

class TestResults(ConfigBaseModel):
    """set of throughput test results"""
    duration: int = Field(description="actual test run duration (seconds)")
    tputDown: List[int] = Field(description="Downstream throughput per stream (in bytes) for the total test duration (not per second)")
    tputUp: List[int] = Field(description="Upstream throughput per stream (in bytes) for the total test duration (not per second)")
    dataLostUp: Optional[List[int]] = Field(description="Upstream data lost per stream (in bytes) for the total test duration (not per second)")
    dataLostDown: Optional[List[int]] = Field(description="Downstream data lost per stream (in bytes) for the total test duration (not per second)")
    latencyAvgUp: Optional[List[int]] = Field(description="Upstream average latency per stream (in microseconds)")
    latencyAvgDown: Optional[List[int]] = Field(description="Downstream latency per stream (in microseconds)")
    latencyMaxUp: Optional[List[int]] = Field(description="Upstream maximum latency per stream (in microseconds)")
    latencyMaxDown: Optional[List[int]] = Field(description="Downstream maximum per stream (in microseconds)")
    cpuLoadAvg: Optional[List[int]] = Field(description="array of cpu (thread) load values in percentage, for each cpu core used by the application, averaged across the test duration", ge=0, le=100)
    cpuLoadMax: Optional[List[int]] = Field(description="array of cpu (thread) load values in percentage, for each cpu core used by the application, maximum value reached at any time during the test duration", ge=0, le=100)
    avgAppStreamHealth: Optional[int] = Field(description="abstract networkApp health value between 0 (app down) to 100 (app transferred all data in perfect health), averaged across the test duration", ge=0, le=100)
    minAppStreamHealth: Optional[int] = Field(description="abstract networkApp health value between 0 (app down) to 100 (app transferred all data in perfect health), worst value during the test duration", ge=0, le=100)
    maxAppStreamHealth: Optional[int] = Field(description="abstract networkApp health value between 0 (app down) to 100 (app transferred all data in perfect health), best value during the test duration", ge=0, le=100)
    