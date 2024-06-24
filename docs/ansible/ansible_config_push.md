# Ansible Config Push

Now that we've built our inventory and proved we can connect to the device with our credentials lets actually do some
automation tasks.  In this demo we'll take the templates shown previously, fill them with some data, and push the config
to our device.

## Ansible Vars

Ansible uses variables (or vars for short) for all kinds of uses including task and playbook selection along with 
filling in data for templates.  These vars can some from many places.  A var can be defined in multiple places and this
provides a rich ability to override depending on where it is placed.  Perhaps you want to set a default value but for
certain types of device override that default with something more appropriate.  For a full description of the process
have a look at [Ansible Variable Precedence](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#ansible-variable-precedence). 

## Our Template Vars

