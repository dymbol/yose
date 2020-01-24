from jinja2 import Environment, Template, FileSystemLoader
import harvest
import settings
import os, sys
from datetime import datetime

workdir = os.path.dirname(os.path.realpath(sys.argv[0]))
#get data
web_anal = harvest.web()
backup_anal = harvest.backup()
service_anal = harvest.services()

env = Environment(
    loader=FileSystemLoader("{0}/templates".format(workdir))
)

template = env.get_template('index.html')
output = template.render(web_anal=web_anal, backup_anal=backup_anal, service_anal=service_anal, gen_date=datetime.now(), title=settings.TITLE,meta_restart_page_s=settings.meta_restart_page_s)

file = open("{0}/index.html".format(settings.OutputDir),"w")
file.write(output)
file.close()
