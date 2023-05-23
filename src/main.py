from fastapi import FastAPI, Response, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from .db import crud, models
from .db.database import SessionLocal, engine
from src import schemas
from requests.structures import CaseInsensitiveDict
import requests
import json

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_token(url, user_pass):
    

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    data = {
        "grant_type": "",
        "username": user_pass["username"],
        "password": user_pass["password"],
        "scope": "",
        "client_id": "",
        "client_secret": ""
    }

    resp = requests.post(url, headers=headers, data=data)

    resp_content = resp.json()

    token = resp_content["access_token"]

    return token

@app.get("/")
async def root():
    return {"Server says It's All Good"}

@app.get("/info")
async def get_info():
    # Define get_info() function logic here
    pass

@app.post("/configStream", status_code=status.HTTP_201_CREATED)
async def config_stream(config: schemas.StreamConfig, 
                        response: Response,
                        db: Session = Depends(get_db),):
    
    json_data = jsonable_encoder(config.dict(exclude_unset=True))

    stream = crud.create_stream_config(db, json_data)

    response.headers["Location"] = f"/configStream/{stream.id}"
    return stream.id

@app.post("/start")
async def start_test(configId: int, duration: int, nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

    key = get_token(nef_base_url+"/api/v1/login/access-token", user_pass)

    #NEF Monitoring Subscription
    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["Content-Type"] = "application/json"

    monitoring_payload = {
        "externalId": "10001@domain.com",
        "notificationDestination": "http://localhost:80/api/v1/utils/monitoring/callback",
        "monitoringType": "LOCATION_REPORTING",
        "maximumNumberOfReports": 1,
        "monitorExpireTime": "2023-03-09T13:18:19.495000+00:00",
        "maximumDetectionTime": 1,
        "reachabilityType": "DATA"
    }

    requests.post(nef_base_url + "/nef/api/v1/3gpp-monitoring-event/v1/netapp/subscriptions",
                headers=headers, data=json.dumps(monitoring_payload))

    #Acquisition of UE location

    requests.get(nef_base_url + f"/api/v1/UEs", headers=headers, params={"supi":"202010000000001"})


    #Acquisition of UE Received Signal Strength Indicator (RSSI) information
    #RSSI=Serving Cell Power + Neighbour Co-Channel Cells Power + Thermal Noise https://www.techplayon.com/rssi/

    #Start loop

    requests.post(nef_base_url + f"/api/v1/ue_movement/start-loop", headers=headers, data=json.dumps({"supi":"202010000000001"}))

    #Acquisition of serving cell information

    requests.get(nef_base_url + f"/api/v1/UEs/{202010000000001}/serving_cell", headers=headers, params={"supi":"202010000000001"})

    #Acquisition of UE Reference Signal Received Power (RSRP) information

    requests.get(nef_base_url + f"/api/v1/UEs/{202010000000001}/rsrps", headers=headers, params={"supi":"202010000000001"})

    #Acquisition of UE path loss

    requests.get(nef_base_url + f"/api/v1/UEs/{202010000000001}/path_losses", headers=headers, params={"supi":"202010000000001"})

    #End Loop

    requests.post(nef_base_url + f"/api/v1/ue_movement/stop-loop", headers=headers, data=json.dumps({"supi":"202010000000001"}))

    #Acquisition of QoS sustainability - qos subscription

    qos_payload = {
        "ipv4Addr": "10.0.0.1",
        "notificationDestination": "http://localhost:80/api/v1/utils/session-with-qos/callback",
        "snssai": {
            "sst": 1,
            "sd": "000001"
        },
        "dnn": "province1.mnc01.mcc202.gprs",
        "qosReference": 9,
        "altQoSReferences": [
            0
        ],
        "usageThreshold": {
            "duration": 0,
            "totalVolume": 0,
            "downlinkVolume": 0,
            "uplinkVolume": 0
        },
        "qosMonInfo": {
            "reqQosMonParams": [
            "DOWNLINK"
            ],
            "repFreqs": [
            "EVENT_TRIGGERED"
            ],
            "latThreshDl": 0,
            "latThreshUl": 0,
            "latThreshRp": 0,
            "waitTime": 0,
            "repPeriod": 0
        }
    }

    requests.post(nef_base_url + "/nef/api/v1/3gpp-as-session-with-qos/v1/netapp/subscriptions",
                headers=headers, params={"scsAsId":"netapp"}, data=json.dumps(qos_payload))

    #Acquisition of UE handover event
    
    requests.get(nef_base_url + f"/api/v1/UEs/{202010000000002}/handovers", headers=headers, params={"supi":"202010000000002"})

    return JSONResponse(content="Done", status_code=200)
     


@app.get("/status")
async def get_status(runId: int):
    # Define get_status() function logic here
    pass

@app.post("/abort")
async def abort_test(runId: int):
    # Define abort_test() function logic here
    pass

@app.get("/report")
async def get_report(runId: int):
    # Define get_report() function logic here
    pass