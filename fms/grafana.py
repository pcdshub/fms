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

def update_alert_rule(alert_uid, body, grafana_server_url=grafana_server_url):
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
    print(response)

def fetch_alert_group(folder_uid, group, grafana_server_url=grafana_server_url):
    print(folder_uid)
    print(group)
    headers = { 
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }   
    response = requests.get(
        grafana_server_url + "/api/v1/provisioning/folder/" + folder_uid + "/rule-groups/" + group,
        headers=headers,
        verify=False
    )   
    return response.json()

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
    #print(response.json())
    #print(response.headers)

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
    #print(response.headers)


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
