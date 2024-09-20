import jinja2
from jinja2 import select_autoescape, FileSystemLoader


env = jinja2.Environment(
    loader=FileSystemLoader("templates"), autoescape=select_autoescape(["html", "xml"])
)
