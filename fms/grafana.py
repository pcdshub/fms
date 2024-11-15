import requests
import json
import re
import csv 
import argparse
from datetime import datetime, timedelta, timezone
import logging
import os


grafana_server_url = 'https://ctl-logsrv.slac.stanford.edu'
token_path = os.getenv("FMS_CFG")
with open(token_path + "/grafana_tokens.txt", 'r') as f:
    token = f.read().strip()
# Function to fetch issues from Jira
def fetch_alert_rules(grafana_server_url):
    headers = { 
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }   
    response = requests.get(
        grafana_server_url + "/api/v1/provisioning/alert-rules",
        headers=headers,
        verify=False
    )   
    return response.json()

def fetch_alert(alert_uid, grafana_server_url=grafana_server_url):
    headers = { 
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }   
    response = requests.get(
        grafana_server_url + "/api/v1/provisioning/alert-rules/" + alert_uid,
        headers=headers,
        verify=False
    )   
    return response.text

def update_alert_group(grafana_server_url, alert_uid, body):
    headers = { 
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }   
    response = requests.put(
        grafana_server_url + "/api/v1/provisioning/alert-rules/" + alert_uid,
        headers=headers,
        data=body,
        verify=False
    )   

def create_alert_rule(body, grafana_server_url=grafana_server_url):
    logging.basicConfig(level=logging.DEBUG)
    headers = { 
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }   
    response = requests.post(
        grafana_server_url + "/api/v1/provisioning/alert-rules",
        headers=headers,
        data=body,
        verify=False
    )   
    print(response.json())
    print(response.headers)

def delete_alert_rule(alert_id, grafana_server_url=grafana_server_url):
    logging.basicConfig(level=logging.DEBUG)
    headers = { 
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }   
    response = requests.delete(
        grafana_server_url + "/api/v1/provisioning/alert-rules/" + alert_id,
        headers=headers,
        verify=False
    )   
    print(response.headers)


def fetch_dashboard(grafana_server_url, dash_uid, write_to_file=None):
    headers = { 
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }   
    response = requests.get(
        grafana_server_url + "/api/dashboards/uid/" + dash_uid,
        headers=headers,
        verify=False
    )   
    if write_to_file is not None:
        f = open(write_to_file, 'w')
        f.write(response.text)
        f.close()
    else:
        return response.text


def create_dashboard(grafana_server_url, body):
    headers = { 
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }   
    response = requests.post(
        grafana_server_url + "/api/dashboards/db",
        headers=headers,
        data=body,
        verify=False
    )   
    print(response.text)

def fetch_home_dashboard(grafana_server_url):
    headers = { 
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }   
    response = requests.get(
        grafana_server_url + "/ctl/grafana/api/dashboards/home",
        headers=headers,
        verify=False
    )   
    print(response.json())

def update_dash_variable(grafana_server_url, dashboard_uid, config, write_to_file):
    fetch_dashboard(grafana_server_url, dashboard_uid, write_to_file)
    set_dashboard_variables(write_to_file, config)

    f = open(write_to_file, 'r')
    create_dashboard(grafana_server_url, f.read())
    f.close()

#print(fetch_alert_rules(grafana_server_url))
#print(fetch_alert(grafana_server_url, "cdhky4eb8ny0wb"))


##from py_grafana_tools import add_query
##add_query("alert.json", "XRT:R10:TEMP")
#f = open("alert.json", 'r')

#update_alert_group(grafana_server_url, "cdhky4eb8ny0wb", f.read())
#print(fetch_dashboard(grafana_server_url, "cdijv4zg86w3ke")) // r60 detail

#from py_grafana_tools import create_detail_rack_dash, set_dashboard_variables, set_dashboard_mappings

#create_detail_rack_dash(grafana_server_url, "MEC", "PR60", "PWR:1", "PWR:2", "https://pswww.slac.stanford.edu/ctl/grafana/d/bdijtid1t09a8c/mec-racks?orgId=1")
#create_detail_rack_dash(grafana_server_url, "MEC", "S60", "PWR:01", "PWR:2", "https://pswww.slac.stanford.edu/ctl/grafana/d/bdijtid1t09a8c/mec-racks?orgId=1")
#create_detail_rack_dash(grafana_server_url, "MEC", "R61", "PWR:1", "PWR:2", "https://pswww.slac.stanford.edu/ctl/grafana/d/bdijtid1t09a8c/mec-racks?orgId=1")
#create_detail_rack_dash(grafana_server_url, "MEC", "R21", "PWR201:2 "PWR:2", "https://pswww.slac.stanford.edu/ctl/grafana/d/bdijtid1t09a8c/mec-racks?orgId=1")
    #create_detail_rack_dash(grafana_server_url, "MEC", "R68", "PWR:01", "PWR:1", "https://pswww.slac.stanford.edu/ctl/grafana/d/bdijtid1t09a8c/mec-racks?orgId=1")

#fetch_dashboard(grafana_server_url, "bdijtid1t09a8c", "temp_rack_summary.json")
#set_dashboard_variables("temp_rack_summary.json", "./config/mec_rack_summary.yaml")

#f = open("temp_rack_summary.json", 'r')
#create_dashboard(grafana_server_url, f.read())
#f.close()

#update_dash_variable(grafana_server_url, "bdijtid1t09a8c", "./config/mec_rack_summary.yaml", "temp_rack_summary.json")

#fetch_dashboard(grafana_server_url, "bdijtid1t09a8c", "temp_rack_summary.json")
#set_dashboard_mappings("temp_rack_summary.json", "./config/mec_rack_summary.yaml")

#f = open("temp_rack_summary.json", 'r')
#create_dashboard(grafana_server_url, f.read())
#f.close()

#set_dashboard_variables("./current_dash/rack_summary.json", "./config/mec_rack_summary.yaml")

#fetch_dashboard(grafana_server_url, "ddtybk0deohdse", "xcs_pem_landing.json")
