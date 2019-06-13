#Here are methods to gather data
import settings
import json
import urllib.request
import ssl

def web():
    '''
    test web pages basen on Websites list from settings
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
            "status_code": status_code
        }
        websites_results.append(website_results)
    return websites_results
