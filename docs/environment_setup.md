# Environment Setup

![setup](https://raw.githubusercontent.com/chipgwyn/wlc_config_demo/main/docs/environment_setup.gif "Environment Setup")


## Connect to the lab host

We're going to ssh to the host with your provided username

`ssh <username>@<hostname>`

If this is the first time connecting to the remote host you will be prompted to save the host's public ssh key.  Answer `y` to the question

```shell
The authenticity of host 'host.example.com (127.10.20.2)' can't be established.
ED25519 key fingerprint is SHA256:hcg+1iEUsdfsdfsdfB5OBrl42NwRSDFsdfSFSmGa28bZ6IqRc.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

## Clone the lab git repository

This lab's setup is contained in a [git repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories) located at
https://github.com/chipgwyn/wlc_config_demo.  Git provides a way to manage changes to a set of files.  This is called a Version Control System (VCS).  It allows
the ability to reference any changed version of a file or set of files while also allowing for collaboration between multiple people and then managing the
integration of those changes.  As features are added and bugs are fixed we can refer to a single place to see all the work that's going into a project.

To 'clone' the lab repo run the following command:

`git clone https://github.com/chipgwyn/wlc_config_demo.git`

The command just copied all the files from the repo from the 'main' branch down to the host and placed it in your current directory.

Have a look at what was all copied:

`tree wlc_config_demo`

The output should look something like the following:

```shell
wlc_config_demo/
├── ansible.cfg
├── inventory.yml
├── playbooks
│   └── configure.yml
├── requirements.txt
└── roles
    └── wlc_config
        ├── tasks
        │   └── main.yml
        ├── templates
        │   ├── add_definition_wlan_config.j2
        │   ├── remove_definition_wlan_config.j2
        │   └── wlc_config.j2
        └── vars
            └── main.yml

6 directories, 9 files
```

## Setup a python virtual environment

The host has python installed on it, however it does not have all the libraries and tools we need to perform our work. 
Generally we do not want to install all those things into the "system's" python environment, we want to install them
only for the job we're doing.  Installing a python library is normally done via a tool called `pip`.  The `pip` tool
will reach to [](https://pypi.org/) and then download and install the package.  Each package installed is maintained
independently (usually) of any other packages available. PyPi is just the defacto repository for hosting packages. 
As bugs are fixed and features are added to packages their versions will change. What happens when the tool you are
using requires one version of a particular package but another tool (or user) needs a different version? You have 
problems! The accepted way to work around this issue is to use a [Python Virtual Environment](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments)
. The idea is to use the same overall Python version your system uses but have a separate installation of specific 
packages to meet your needs.

To create our virtual environment run the following commands:

```
cd
python3 -m venv ./venv
```
There should now be a directory called 'venv' in your home dir:

`ls` will show the files 

We have now created the python virtual environment however we must `activate` it in order to tell the system we want
to use it over the global system's python.

To see where your environment is looking for python run `which python3`.  This should show `/usr/bin/python3`.

Now Run the command `source ./venv/bin/activate`.   You should notice that the prompt in your shell changed to indicate 
the virtual environment is activated.  It will be prefixed with `(venv) `.   

Run `which python3` again and notice that it will now point to something like `/home/<username>/venv/bin/python3`

At any time we can run `deactivate` to switch back to the global system's python.

# Install Ansible

Now that we have our virtualenv we can install ansible and related tools and packages.

**NOTE** Before proceeding be sure your python virtual environment is activated!

As noted before we can install python packages using the `pip` tool.  Pip will install the package specified and can
take an argument for the specific version as well.  The really nice thing is that any requested package installation
will have all of its package dependencies installed along side it, and then any of those package's dependencies!  This
makes installing a package pretty easy (usually).  

Lets install the `ansible-core` package by running `pip install ansible-core`.   This will get the very bare bits of
ansible installed along with the minimum required dependencies.   For our lab we want not only _ansible-core_ but
several of the additional tools as well.   The de-facto standard for what all packages to install for a given project
is to have them listed in a `requirements.txt` file.  This file lists the specific package names and versions needed
for a given environment.

Move into the `wlc_config_demo` directory and have a look at the requirements.txt file

```
cd wlc_config_demo
cat requirements.txt
```

Now we can install each of those packages one at a time or we can just tell pip to do everything listed in the file

Run the command: `pip install -r requirements.txt`


You should be seeing a lot of output showing what all is being installed.  Once completed we should be ready to start
using ansible.  One more thing before we start.   Suppose you want to confirm exactly what all packages and versions
are installed in your environment.

Run the command: `pip freeze`

You should see a list of packages and version installed.  It looks very similar to what was in the requirements.txt file.
Frequently this is what's used to generate the requirements.txt file.  When you're working on a project and you want to
save the current list of packages and versions you can just save this output in your requirements.txt and be sure that 
the environment is the same the next time you want to use it (or need to start over).

You should now be good to continue with lab
