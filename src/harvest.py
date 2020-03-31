#Here are methods to gather data
import settings
import json
import urllib.request
import ssl
import datetime
import os
import subprocess

def web():
    '''
    test web pages stored in Websites list from settings.py
    '''
    websites_results = []
    for website in settings.Websites:
        status = ""
        status_code = 1

        try:
            if website["test_method"] == "json":
                f = urllib.request.urlopen(website["url"])
                status = json.loads(f.read(100))["status"]
                if status == "database connection ok":
                    status_code = 0
                else:
                    status_code = 1
            elif website["test_method"] == "http_code":
                response_code = urllib.request.urlopen(website["url"]).getcode()
                if response_code == 200:
                    status = "Connection successfull"
                    status_code = 0
                else:
                    status = "Connection issue. HTTP status: {0}".format(response_code)
                    status_code = 3
            else:
                status = "Unknown test method: {0}".format(website["test_method"])
                status_code = 99
        except urllib.error.HTTPError as e:
            status = "Can't connect"
            status_code = 2
            if settings.Verbose is True:
                print(status)
                print(e)
                print("=====================")
        except urllib.error.URLError as e:
            status = "Can't connect"
            status_code = 3
            if settings.Verbose is True:
                print(status)
                print(e)
                print("=====================")
        except ssl.CertificateError as e:
            status = "Certificate Error"
            status_code = 4
            if settings.Verbose is True:
                print(status)
                print(e)
                print("=====================")
        except socket.gaierror:
            status = "DNS error"
            status_code = 4
            if settings.Verbose is True:
                print(status)
                print(e)
                print("=====================")

        website_results = {
            "name": website["name"],
            "url": website["url"],
            "status": status,
            "status_code": status_code,
            "harvest_date": datetime.datetime.now()
            }
        websites_results.append(website_results)
    return websites_results


def backup():
    '''
    test backups status stored in Backup list from settings.py
    '''
    results = []
    for backup_definition in settings.Backups:
        status = ""
        status_code = 1
        if backup_definition["test_method"] == "json_restic":
            '''
                This method checks the last backup's date from restic's back log.
                If the date is older than backup_definition["period"] it returns problem with backup
            '''
            if os.path.isfile(backup_definition['file_path']):
                try:
                    file_jl = open(backup_definition['file_path'],"r")
                    restic_output = json.loads(file_jl.read())
                    last_backup_date = datetime.datetime.strptime(restic_output[-1]['time'][:-9], '%Y-%m-%dT%H:%M:%S.%f') #2019-06-17T12:34:33.110604005+02:00
                    if (datetime.datetime.now() - last_backup_date) > datetime.timedelta(days=backup_definition['period']):
                        status = "Backup too old ({0} days)".format(backup_definition['period'])
                        status_code = 2
                    else:
                        status = "Backup created: {0}".format(last_backup_date)
                        status_code = 0
                except Exception as e:
                    status = "Can't open file {0}".format(backup_definition['file_path'])
                    status_code = 1
                    if settings.Verbose is True:
                        print(status)
                        print(e)
                        print("=====================")
            else:
                status = "Can't open file {0}".format(backup_definition['file_path'])
                status_code = 1


        elif backup_definition["test_method"] == "json_hydra_v1":
            '''
                This method checks the last backup's date and status from Hydra_backup json log file.
                If the date is older than backup_definition["period"] or ststus is greater than 0 it returns problem with backup.
            '''
            if os.path.isfile(backup_definition['file_path']):
                try:
                    file_jl = open(backup_definition['file_path'],"r")
                    bck_item = json.loads(file_jl.read())
                    if bck_item[0]['format'] == "json_hydra_v1":
                        last_backup_date = datetime.datetime.strptime(bck_item[0]['time'], '%Y-%m-%dT%H:%M:%S.%f') #isoformat
                        if (datetime.datetime.now() - last_backup_date) > datetime.timedelta(days=backup_definition['period']):
                            status = "Backup too old ({0} days)".format(backup_definition['period'])
                            status_code = 2
                        else:
                            if bck_item[0]['status'] > 0: #checking for bash exit code from backup
                                status = "There were errors while creating backup"
                                status_code = 3
                            else:
                                status = "Backup created: {0}".format(last_backup_date)
                                status_code = 0
                    else:
                        status = "Unknown backup log file format {0}".format(json_output['format'])
                        status_code = 1
                        if settings.Verbose is True:
                            raise
                except Exception as e:
                    status = "Can't open file {0}".format(backup_definition['file_path'])
                    status_code = 1
                    if settings.Verbose is True:
                        print(status)
                        print(e)
                        print("=====================")
            else:
                status = "Can't open file {0}".format(backup_definition['file_path'])
                status_code = 1
        if backup_definition["test_method"] == "json_borg":
            '''
                This method checks the last backup's date from borg's output from "borg info --json" command.
                If the date is older than backup_definition["period"] it returns problem with backup
            '''
            if os.path.isfile(backup_definition['file_path']):
                try:
                    file_jl = open(backup_definition['file_path'],"r")
                    borg_output = json.loads(file_jl.read())
                    last_backup_date = datetime.datetime.strptime(borg_output["repository"]["last_modified"][:-9], '%Y-%m-%dT%H:%M:%S.%f') #2019-06-17T12:34:33.110604005+02:00
                    if (datetime.datetime.now() - last_backup_date) > datetime.timedelta(days=backup_definition['period']):
                        status = "Backup too old ({0} days)".format(backup_definition['period'])
                        status_code = 2
                    else:
                        status = "Backup created: {0}".format(last_backup_date)
                        status_code = 0
                except Exception as e:
                    status = "Can't open file {0}".format(backup_definition['file_path'])
                    status_code = 1
                    if settings.Verbose is True:
                        print(status)
                        print(e)
                        print("=====================")
            else:
                status = "Can't open file {0}".format(backup_definition['file_path'])
                status_code = 1                
        
        else:
            status = "Unknown test method: {0}".format(backup_definition["test_method"])
            status_code = 99

        backup_results = {
            "name": backup_definition["name"],
            "file_path": backup_definition["file_path"],
            "status": status,
            "status_code": status_code,
            "harvest_date": datetime.datetime.now()
            }
        if "zabbix_key" in backup_definition:
            backup_results["zabbix_key"] = backup_definition["zabbix_key"] 

        results.append(backup_results)

    return results
def services():
    '''
    test services statuses stored in Services list from settings.py
    '''
    results = []
    for service_definition in settings.Services:
        status = ""
        status_code = 1
        if service_definition["test_method"] == "command":
            result = subprocess.Popen(service_definition['command'], shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
            if result == service_definition["result_stdout"]:
                status = f"Service {service_definition['name']} works"
                status_code = 0
            else:
                status = f"Service {service_definition['name']} wrong result: {result}"
                status_code = 1
        else:
            status = f"Unknown test method: {service_definition['test_method']}"
            status_code = 99
        service_results = {
            "name": service_definition["name"],
            "command": service_definition["command"],
            "status": status,
            "status_code": status_code,
            "harvest_date": datetime.datetime.now()
            }
        results.append(service_results)
    return results
