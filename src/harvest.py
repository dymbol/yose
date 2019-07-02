#Here are methods to gather data
import settings
import json
import urllib.request
import ssl
import datetime
import os

def web():
    '''
    test web pages stored in Websites list from settings.py
    '''
    websites_results = []
    for website in settings.Websites:
        status = ""
        status_code = 1
        if website["test_method"] == "json":
            try:
                f = urllib.request.urlopen(website["url"])
                status = json.loads(f.read(100))["status"]
                if status == "database connection ok":
                    status_code = 0
                else:
                    status_code = 1
            except urllib.error.HTTPError as e:
                status = "Can't connect"
                status_code = 2
                if settings.Verbose is True:
                    print(e)
            except urllib.error.URLError as e:
                status = "Can't connect"
                status_code = 3
                if settings.Verbose is True:
                    print(e)
            except ssl.CertificateError as e:
                status = "Certificate Error"
                status_code = 4
                if settings.Verbose is True:
                    print(e)

        elif website["test_method"] == "http_code":
            try:
                response_code = urllib.request.urlopen(website["url"]).getcode()
                if response_code == 200:
                    status = "Connection successfull"
                    status_code = 0
                else:
                    status = "Connection issue. HTTP status: {0}".format(response_code)
                    status_code = 3
            except urllib.error.HTTPError as e:
                status = "Can't connect"
                status_code = 2
                if settings.Verbose is True:
                    print(e)

        else:
            status = "Unknown test method: {0}".format(website["test_method"])
            status_code = 99

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
                If the date is older than backup["period"] it returns problem with backup
            '''
            if os.path.isfile(backup_definition['file_path']):
                try:
                    file = open(backup_definition['file_path'],"r")
                    restic_output = json.loads(file.read())
                    last_backup_date = datetime.datetime.strptime(restic_output[-1]['time'][:-9], '%Y-%m-%dT%H:%M:%S.%f') #2019-06-17T12:34:33.110604005+02:00
                    if (datetime.datetime.now() - last_backup_date) > datetime.timedelta(days=backup_definition['period']):
                        status = "Backup too old ({0} days)".format(backup['period'])
                        status_code = 2
                    else:
                        status = "Backup created: {0}".format(last_backup_date)
                        status_code = 0
                except as e:
                    status = "Can't open file {0}".format(backup_definition['file_path'])
                    status_code = 1
                    if settings.Verbose is True:
                        print(e)
            else:
                status = "Can't open file {0}".format(backup_definition['file_path'])
                status_code = 1


        elif backup_definition["test_method"] == "json_hydra_v1":
            '''
                This method checks the last backup's date and status from Hydra_backup json log file.
                If the date is older than backup["period"] or ststus is greater than 0 it returns problem with backup.
            '''
            if os.path.isfile(backup_definition['file_path']):
                try:
                    file = open(backup_definition['file_path'],"r")
                    bck_item = json.loads(file.read())
                    if bck_item[0]['format'] == "json_hydra_v1":
                        last_backup_date = datetime.datetime.strptime(bck_item[0]['time'], '%Y-%m-%dT%H:%M:%S.%f') #isoformat
                        if (datetime.datetime.now() - last_backup_date) > datetime.timedelta(days=backup_definition['period']):
                            status = "Backup too old ({0} days)".format(backup['period'])
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
                except as e:
                    status = "Can't open file {0}".format(backup_definition['file_path'])
                    status_code = 1
                    if settings.Verbose is True:
                        print(e)
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
        results.append(backup_results)

    return results
