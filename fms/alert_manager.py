from .py_grafana import fetch_alert 

def get_alert(alert_uid):
    alert = fetch_alert(alert_uid) 
    print(alert)