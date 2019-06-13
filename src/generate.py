from jinja2 import Environment, Template, FileSystemLoader
import harvest
import settings

#get data
web_anal = harvest.web()
#backup_anal = harvest.backup()
#services_anal = harvest.services()

env = Environment(
    loader=FileSystemLoader("templates")
)

template = env.get_template('index.html')
output = template.render(web_anal=web_anal)

file = open("{0}/index.html".format(settings.OutputDir),"w")
file.write(output)
file.close()
