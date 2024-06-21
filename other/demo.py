#!/usr/bin/env python3

from ruamel.yaml import YAML
from jinja2 import Environment, FileSystemLoader

yaml = YAML()
j2_env = Environment(loader=FileSystemLoader("./"))
data = yaml.load(open("./data.yml", "r"))

wlan_template = j2_env.get_template("./definition-wlan.j2")
#wlan_tag_template =  j2_env.get_template("./definition-wlan-tag-policy.j2")


print(wlan_template.render(**data))
#print(wlan_tag_template.render(**data))
