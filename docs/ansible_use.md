# Ansible

For the lab we're going to be using [Ansible](https://ansible.readthedocs.io/projects/ansible-core/en/devel/getting_started/index.html)
to perform most of our work.  Ansible is a framework to do "things" on remote hosts.  There are many ways to connect
to those hosts and also many "actions" that can be performed on those hosts.  These actions can be configured into 
"tasks" that can then be composed into a "play".  Further, plays can be made of reusable "roles" to achieve the 
desired state of a device.

We'll now configure ansible to connect to our WLC and push the configuration of our wireless lan.

## A Note on Editors

When working in the shell of a linux host there are usually at least two tools availble to edit files; vi and nano.
Which one you choose to use is of personal preference and deciding which one you *should* use is the source of many
debates.   For the purpose of this tutorial we'll be using nano.  If you are familiar with vi and would prefer to use
it, feel free to.  Both are excellent tools.

- [Using vi](https://www.tutorialspoint.com/unix/unix-vi-editor.htm)
- [Using nano](https://help.ubuntu.com/community/Nano)

## Ansible Demos

  - [Ansible Inventory](ansible/ansible_inventory.md)
  - [Ansible Config Pus](ansible/ansible_config_push.md)