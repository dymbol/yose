from jinja2 import Environment, Template, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)
websites = []


template = env.get_template('mytemplate.html')

websites.append({href: "http:wp.pl", status: "0"})
template.render(websites=websites)
print(template)
