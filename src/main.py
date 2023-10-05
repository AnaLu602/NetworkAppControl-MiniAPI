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
import re

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


#Login - pass
@app.post("/start/1/1")
async def start_test_1_1(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

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

#Create Monitoring Subscription - pass
@app.post("/start/1/2")
async def start_test_1_2(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

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

#Get UE Location Acquisiton - pass
@app.post("/start/1/3")
async def start_test_1_3(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

    key = get_token(nef_base_url+"/api/v1/login/access-token", user_pass)

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["Content-Type"] = "application/json"

    requests.get(nef_base_url + f"/api/v1/UEs", headers=headers, params={"supi":"202010000000001"})

#Get UE Serving Cell - pass
@app.post("/start/1/4")
async def start_test_1_4(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

    key = get_token(nef_base_url+"/api/v1/login/access-token", user_pass)

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["Content-Type"] = "application/json"

    requests.post(nef_base_url + f"/api/v1/ue_movement/start-loop", headers=headers, data=json.dumps({"supi":"202010000000001"}))

    #Acquisition of serving cell information

    requests.get(nef_base_url + f"/test/api/v1/UEs/{202010000000001}/serving_cell", headers=headers, params={"supi":"202010000000001"})

    requests.post(nef_base_url + f"/api/v1/ue_movement/stop-loop", headers=headers, data=json.dumps({"supi":"202010000000001"}))

#Create QoS Subscription
@app.post("/start/1/5")
async def start_test_1_5(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

    key = get_token(nef_base_url+"/api/v1/login/access-token", user_pass)

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["Content-Type"] = "application/json"

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

#Login - pass wrong credentials
@app.post("/start/2/1")
async def start_test_2_1(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

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

#Create Monitoring Subscription - fail login wrong credentials
@app.post("/start/2/2")
async def start_test_2_2(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

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

#Create QoS Subscription - fail login wrong credentials
@app.post("/start/2/3")
async def start_test_2_3(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

    key = get_token(nef_base_url+"/api/v1/login/access-token", user_pass)

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["Content-Type"] = "application/json"

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

#Login - wrong implementation
@app.post("/start/3/1")
async def start_test_3_1(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_pass,
        "password": nef_username
    }

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

#Create Monitoring Subscription - fail login doesnt work
@app.post("/start/3/2")
async def start_test_3_2(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_pass,
        "password": nef_username
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

#Get UEs Location Acquisiton - fail login doesnt work
@app.post("/start/3/3")
async def start_test_3_3(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_pass,
        "password": nef_username
    }

    key = get_token(nef_base_url+"/api/v1/login/access-token", user_pass)

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["Content-Type"] = "application/json"

    requests.get(nef_base_url + f"/api/v1/UEs", headers=headers, params={"supi":"202010000000001"})

#Get UE Path Losses - fail login doesnt work
@app.post("/start/3/4")
async def start_test_3_4(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_pass,
        "password": nef_username
    }

    key = get_token(nef_base_url+"/api/v1/login/access-token", user_pass)

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["Content-Type"] = "application/json"

    requests.post(nef_base_url + f"/api/v1/ue_movement/start-loop", headers=headers, data=json.dumps({"supi":"202010000000001"}))

    #Acquisition of UE Path Losses information

    requests.get(nef_base_url + f"/test/api/v1/UEs/{202010000000001}/path_losses", headers=headers, params={"supi":"202010000000001"})

    requests.post(nef_base_url + f"/api/v1/ue_movement/stop-loop", headers=headers, data=json.dumps({"supi":"202010000000001"}))

#Create Monitoring Subscription - fail login doesnt exist
@app.post("/start/4/1")
async def start_test_4_1(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Monitoring Subscription
    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
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

#Get UE Serving Cell - fail login doesnt exist
@app.post("/start/4/2")
async def start_test_4_2(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Content-Type"] = "application/json"

    requests.post(nef_base_url + f"/api/v1/ue_movement/start-loop", headers=headers, data=json.dumps({"supi":"202010000000001"}))

    #Acquisition of serving cell information

    requests.get(nef_base_url + f"/test/api/v1/UEs/{202010000000001}/serving_cell", headers=headers, params={"supi":"202010000000001"})

    requests.post(nef_base_url + f"/api/v1/ue_movement/stop-loop", headers=headers, data=json.dumps({"supi":"202010000000001"}))

#Get UE Handovers - fail login doesnt exist
@app.post("/start/4/3")
async def start_test_4_3(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Content-Type"] = "application/json"

    #Acquisition of UE handover event
    requests.get(nef_base_url + f"/test/api/v1/UEs/{202010000000002}/handovers", headers=headers, params={"supi":"202010000000002"})

#Create QoS Subscription - fail login doesnt exist
@app.post("/start/4/4")
async def start_test_4_4(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Content-Type"] = "application/json"

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

#Login - pass
@app.post("/start/5/1")
async def start_test_5_1(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

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

#Get UEs Location Acquisiton - pass
@app.post("/start/5/2")
async def start_test_5_2(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

    key = get_token(nef_base_url+"/api/v1/login/access-token", user_pass)

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["Content-Type"] = "application/json"

    requests.get(nef_base_url + f"/api/v1/UEs", headers=headers, params={"supi":"202010000000001"})

#Get UE Path Losses - fail no emulation
@app.post("/start/5/3")
async def start_test_5_3(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

    key = get_token(nef_base_url+"/api/v1/login/access-token", user_pass)

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["Content-Type"] = "application/json"

    #Acquisition of UE Path Losses information
    requests.get(nef_base_url + f"/test/api/v1/UEs/{202010000000001}/path_losses", headers=headers, params={"supi":"202010000000001"})

#Get UE Serving Cell - pass
@app.post("/start/5/4")
async def start_test_5_4(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

    key = get_token(nef_base_url+"/api/v1/login/access-token", user_pass)

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["Content-Type"] = "application/json"

    #Acquisition of serving cell information
    requests.get(nef_base_url + f"/test/api/v1/UEs/{202010000000001}/serving_cell", headers=headers, params={"supi":"202010000000001"})

#Create QoS Subscription
@app.post("/start/5/5")
async def start_test_5_5(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

    key = get_token(nef_base_url+"/api/v1/login/access-token", user_pass)

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["Content-Type"] = "application/json"

    #Acquisition of QoS sustainability - qos subscription
    qos_payload = {
        "ipv4Addr": "10.0.0.2",
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

#Login - pass
@app.post("/start/6/1")
async def start_test_6_1(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

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

#Create Monitoring Subscription - wrong payload
@app.post("/start/6/2")
async def start_test_6_2(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

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
        "maximumNumberOfReports": "one",
        "monitorExpireTime": "2023-03-09T13:18:19.495000+00:00",
        "maximumDetectionTime": 1,
        "reachabilityType": "DATA"
    }

    requests.post(nef_base_url + "/nef/api/v1/3gpp-monitoring-event/v1/netapp/subscriptions",
                headers=headers, data=json.dumps(monitoring_payload))

#Get UE Handovers - pass
@app.post("/start/6/3")
async def start_test_6_3(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Content-Type"] = "application/json"

    #Acquisition of UE handover event
    requests.get(nef_base_url + f"/test/api/v1/UEs/{202010000000001}/handovers", headers=headers, params={"supi":"202010000000001"})

#Create QoS Subscription
@app.post("/start/6/4")
async def start_test_6_4(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

    key = get_token(nef_base_url+"/api/v1/login/access-token", user_pass)

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["Content-Type"] = "application/json"

    #Acquisition of QoS sustainability - qos subscription
    qos_payload = {
        "ipv4Addr": "10.0.0.1",
        "notificationDestination": "http://localhost:80/api/v1/utils/session-with-qos/callback",
        "snssai": {
            "sst": 1,
            "sd": "000001"
        },
        "dnn": "province1.mnc01.mcc202.gprs",
        "qosReference": "nine",
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

#Login - pass
@app.post("/start/7/1")
async def start_test_8_1(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

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

#Create Monitoring Subscription - wrong method used
@app.post("/start/7/2")
async def start_test_7_2(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

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
        "maximumNumberOfReports": "one",
        "monitorExpireTime": "2023-03-09T13:18:19.495000+00:00",
        "maximumDetectionTime": 1,
        "reachabilityType": "DATA"
    }

    requests.get(nef_base_url + "/nef/api/v1/3gpp-monitoring-event/v1/netapp/subscriptions",
                headers=headers, data=json.dumps(monitoring_payload))

#Create QoS Subscription - pass - already exists
@app.post("/start/7/3")
async def start_test_7_3(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

    key = get_token(nef_base_url+"/api/v1/login/access-token", user_pass)

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["Content-Type"] = "application/json"

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

#Login - pass
@app.post("/start/8/1")
async def start_test_8_1(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

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

#Create Monitoring Subscription - pass
@app.post("/start/8/2")
async def start_test_8_2(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

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
        "externalId": "10002@domain.com",
        "notificationDestination": "http://localhost:80/api/v1/utils/monitoring/callback",
        "monitoringType": "LOCATION_REPORTING",
        "maximumNumberOfReports": 1,
        "monitorExpireTime": "2023-03-09T13:18:19.495000+00:00",
        "maximumDetectionTime": 1,
        "reachabilityType": "DATA"
    }

    requests.post(nef_base_url + "/nef/api/v1/3gpp-monitoring-event/v1/netapp/subscriptions",
                headers=headers, data=json.dumps(monitoring_payload))

#Get UE Serving Cell - pass
@app.post("/start/8/3")
async def start_test_8_3(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

    key = get_token(nef_base_url+"/api/v1/login/access-token", user_pass)

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["Content-Type"] = "application/json"

    requests.post(nef_base_url + f"/api/v1/ue_movement/start-loop", headers=headers, data=json.dumps({"supi":"202010000000002"}))

    #Acquisition of serving cell information

    requests.get(nef_base_url + f"/test/api/v1/UEs/{202010000000002}/serving_cell", headers=headers, params={"supi":"202010000000002"})

    requests.post(nef_base_url + f"/api/v1/ue_movement/stop-loop", headers=headers, data=json.dumps({"supi":"202010000000002"}))

#Get UE Handovers - pass
@app.post("/start/8/4")
async def start_test_8_4(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Content-Type"] = "application/json"

    #Acquisition of UE handover event
    requests.get(nef_base_url + f"/test/api/v1/UEs/{202010000000002}/handovers", headers=headers, params={"supi":"202010000000002"})

#Get UEs Location Acquisiton - pass
@app.post("/start/8/5")
async def start_test_8_5(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

    key = get_token(nef_base_url+"/api/v1/login/access-token", user_pass)

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["Content-Type"] = "application/json"

    requests.get(nef_base_url + f"/api/v1/UEs", headers=headers, params={"supi":"202010000000002"})

#Get UE Path Losses - pass
@app.post("/start/8/6")
async def start_test_8_6(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

    key = get_token(nef_base_url+"/api/v1/login/access-token", user_pass)

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["Content-Type"] = "application/json"

    requests.post(nef_base_url + f"/api/v1/ue_movement/start-loop", headers=headers, data=json.dumps({"supi":"202010000000002"}))

    #Acquisition of UE Path Losses information

    requests.get(nef_base_url + f"/test/api/v1/UEs/{202010000000002}/path_losses", headers=headers, params={"supi":"202010000000002"})

    requests.post(nef_base_url + f"/api/v1/ue_movement/stop-loop", headers=headers, data=json.dumps({"supi":"202010000000002"}))

#Create QoS Subscription - fail wrong method
@app.post("/start/8/7")
async def start_test_8_7(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

    key = get_token(nef_base_url+"/api/v1/login/access-token", user_pass)

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["Content-Type"] = "application/json"

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

    requests.get(nef_base_url + "/nef/api/v1/3gpp-as-session-with-qos/v1/netapp/subscriptions",
                headers=headers, params={"scsAsId":"netapp"}, data=json.dumps(qos_payload))


#Login - pass
@app.post("/start/9/1")
async def start_test_9_1(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

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


#Test generating values
@app.post("/start/9/2")
async def start_test_9_2(nef_ip: str, nef_port: str, nef_username: str, nef_pass: str):

    #NEF Login
    nef_base_url = f"http://{nef_ip}:{nef_port}"

    user_pass = {
        "username": nef_username,
        "password": nef_pass
    }

    key = get_token(nef_base_url+"/api/v1/login/access-token", user_pass)

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer " + key
    headers["Content-Type"] = "application/json"

    #Acquisition of QoS sustainability - qos subscription
    qos_payload = {
        "ipv4Addr": "10.0.0.3",
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

    response = requests.post(nef_base_url + "/nef/api/v1/3gpp-as-session-with-qos/v1/netapp/subscriptions",
                headers=headers, params={"scsAsId":"netapp"}, data=json.dumps(qos_payload))

    response_json = response.json()

    url = response_json["link"]

    url_parts = url.split('/')
    supi = url_parts[-1]

    #star broker
    requests.post(nef_base_url + f"/test/api/v1/broker/start", headers=headers)

    parameters = {
        "amplitude": 20,
        "frequency": 0.3,
        "phase": 2,
        "offset": 50
    }

    #update parameters
    requests.post(nef_base_url + f"/test/api/v1/broker/update_sinusoidal_parameters", headers=headers, data=json.dumps(parameters))

    #trigger qos
    requests.post(nef_base_url + f"/test/api/v1/broker/trigger_qos?param=usageThreshold-uplinkVolume", headers=headers, params={"param": "usageThreshold-uplinkVolume"})

    #get qos

    qos_response = requests.get(nef_base_url + f"/nef/api/v1/3gpp-as-session-with-qos/v1/netapp/subscriptions/{supi}", params={"scsAsId":"netapp", "subscriptionId": supi}, headers=headers)

    qos_response_json = qos_response.json()

    uplinkVolume = qos_response_json["usageThreshold"]["uplinkVolume"]

    if uplinkVolume != 0:
        print("Updated with success.")

    #stop qos
    requests.post(nef_base_url + f"/test/api/v1/broker/stop_qos", headers=headers)

    #stop broker
    requests.post(nef_base_url + f"/test/api/v1/broker/stop", headers=headers)

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