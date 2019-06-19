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
            except urllib.error.HTTPError:
                status = "Can't connect"
                status_code = 2
            except urllib.error.URLError:
                status = "Can't connect"
                status_code = 3
            except ssl.CertificateError:
                status = "Certificate Error"
                status_code = 4
        elif website["test_method"] == "http_code":
            response_code = urllib.request.urlopen(website["url"]).getcode()
            if response_code == 200:
                status = "Connection successfull"
                status_code = 0
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
                except:
                    status = "Can't open file {0}".format(backup_definition['file_path'])
                    status_code = 1
                    raise
            else:
                status = "Can't open file {0}".format(backup_definition['file_path'])
                status_code = 1


        if backup_definition["test_method"] == "json_hydra_v1":
            '''
                This method checks the last backup's date and status from Hydra_backup json log file.
                If the date is older than backup["period"] or ststus is greater than 0 it returns problem with backup.
            '''
            if os.path.isfile(backup_definition['file_path']):
                try:
                    file = open(backup_definition['file_path'],"r")
                    json_output = json.loads(file.read())
                    if json_output[0]['format'] == "json_hydra_v1":
                        for bck_item in json_output[1]:
                            last_backup_date = datetime.datetime.strptime(bck_item['time'], '%Y-%m-%dT%H:%M:%S.%f') #isoformat
                            if (datetime.datetime.now() - last_backup_date) > datetime.timedelta(days=backup_definition['period']):
                                status = "Backup too old ({0} days)".format(backup['period'])
                                status_code = 2
                            else:
                                if bck_item['status'] > 0 #checking for bash exit code from backup
                                    status = "There were errors while creating backup"
                                    status_code = 3
                                else:
                                    status = "Backup created: {0}".format(last_backup_date)
                                    status_code = 0
                            backup_results = {
                                "name": bck_item["name"],
                                "file_path": backup_definition["file_path"],
                                "status": status,
                                "status_code": status_code,
                                "harvest_date": datetime.datetime.now()
                                }
                            results.append(backup_results)

                    else:
                        status = "Unknown backup log file format {0}".format(json_output['format'])
                        status_code = 1
                        raise

                except:
                    status = "Can't open file {0}".format(backup['file_path'])
                    status_code = 1
                    raise
            else:
                status = "Can't open file {0}".format(backup['file_path'])
                status_code = 1
        else:
            status = "Unknown test method: {0}".format(backup["test_method"])
            status_code = 99

    backup_results = {
        "name": backup["name"],
        "file_path": backup["file_path"],
        "status": status,
        "status_code": status_code,
        "harvest_date": datetime.datetime.now()
        }
    if len(results) == 0:   #if results not yet added than add it
        results.append(backup_results)

    return results
