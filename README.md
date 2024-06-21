# Cisco WLC Config Demo

This lab covers a general method for automating the deployment of wireless lan on a Cisco Wireless Lan Controller

The usernames and passwords for this should be provided by lab instructor

Refer to the [Environment Setup](docs/environment_setup.md) to get your environment configured

# Let's Automate!

Assuming you are logged into the lab host and have ansible installed and the lab repo cloned you should be good to
start.


## Goal

The goal of this exercise is to deploy your own "test" SSID to a Cisco Wireless Lan Controller (WLC) using automation.

## The config

```
wlan {{ wlan_name|upper }} {{ wlan_id }} {{ wlan_ssid|title }}
  security wpa psk set-key ascii 0 {{ wlan_password }}
  no security wpa akm dot1x
  security wpa akm psk
  no shutdown
wireless tag policy {{ wlan_name|upper }}-policy-tag
  description "Policy Tag for {{ wlan_name|upper }}-policy-tag"
  wlan {{ wlan_name|upper }} policy COMPANY-POL-PROF
```

## Templates

What you see above is the configuration snippet that will define a wifi network and then attach that definition
to a particular wireless policy.

You'll notice there are several words surrounded by {{ }}.  These are variables that can be defined elsewhere
Effectively what the above is showing is a template for the config.  We can fill in those variables with names and IDs
that meet our needs.  The rest of the config is pretty much the same.  We can repeat this 100 times, defining 100 lans,
and know that they are all configured correctly; no lines missing, ensure a description is added, configured to meet our
exact specifications and needs.      

Some things to note here.  
 - We want the "wlan_name" to always be uppercase, aids in spotting the specific config when looking at 100s of lines
 - We want the "wlan_ssid" to use TitleCase, purely aesthetic choice
 - The wlan ID should always be an integer.  If the data provided is not an integer and error will be raised

You'll notice that after some of the variable names inside the template have `int` or `title` or `upper`.  These are
further definitions that will convert whatever is provided to an integer (int), make the name all upper case (upper), or
make the string use Title Case (title).   So now not only is our config consistent but the format of our provided variables
are consistent as well.  When perusing the config it makes non-standard config stand out easier.

If needed we can build templates for multiple use cases.  In the above example the authentication is just using a 
pre-shared-key, a password shared with everyone that wants to connect to wifi.   Perhaps we wanted another template that
defined a wifi network that was more secure where every user had their own username and password.  We could build a
template in the same manner.  Now we have the ability to define wifi networks that use user-specific authentication or
networks that use a shared password.  Either way we can make sure that when those networks are written to the config of 
the WLC we know they are configured in a consistent manner.

On a given WLC there may be 100s of these configs and they may have been deployed at different times by different
people.  Consistency gives confidence that nothing has been forgotten and that our network administrators have a higher
level of familiarity with the configurations on the device.  This makes the overall config easier to understand and
aids the administrators learn how the overall pieces fit together for a more complete understanding of the system.  

### Working Example

Move into the 'other' directory.

```
cd ~/wlc_config_demo
cd other
ls -la
```

Files:
 - data.yml: a [YAML](https://en.wikipedia.org/wiki/YAML#Basic_components) formatted file that contains our variable definitions
 - definition-wlan.j2: A template file written using the [Jinja](https://jinja.palletsprojects.com/en/3.1.x/templates/) templating format
 - demo.py: a python script that reads in the data.yml file and then renders the jinja template

Variable definitions in the data.yml file:

```
$ cat data.yml
wlan_name: wlan-pod1
wlan_id: 20
wlan_ssid: POD1-NeT
wlan_password: $%mySuperSeCRetPas44**
```

Running the `demo.py` script:

```
$ ./demo.py
wlan WLAN-POD1 20 Pod1-Net
  security wpa psk set-key ascii 0 $%mySuperSeCRetPas44**
  no security wpa akm dot1x
  security wpa akm psk
  no shutdown
wireless tag policy WLAN-POD1-policy-tag
  description "Policy Tag for WLAN-POD1-policy-tag"
  wlan WLAN-POD1 policy COMPANY-POL-PROF
```

## Automation

We've already touched on this a bit with the use of templates; things are consistent, repeatable, and expected.  This 
greatly aids the administrators in their day-to-day work, cuts down on errors and misconfigurations, and speeds 
troubleshooting.   

The templating is only part of our goal. We've got the config that we're going to apply standardized!  This is great!
Now we need to get that config onto the device.  The user will take the generated config and copy and paste the config
onto the device.  This has problems as well.  Sometimes the user might not copy all the config, leaving out a line or
perhaps a character at the end of the line.  

### I'll just write a script to do it!

We can write a program to take in a file of wireless lan definitions, combine them with our templates, and then push
them to the WLC over [ssh](https://www.openssh.com/) (_ssh is the native connection method for managing the WLC 
config_).  We soon find that writing on our own code to interact with the WLC is fraught with peril.  There are multiple
ways to authenticate and then gain admin privileges.  We have to write code to identify which method is being used
and then react accordingly.  This is not insurmountable but isn't strictly in the scope of what we're trying to 
accomplish.  We forge ahead however and get that solved.   

At this point we've connected to our device and authenticated.  We now need to enable the config mode of the device at
which point it may tell us we're not authorized, someone else is already in config mode, or many other various
possibilities.  Again, not impossible to figure out since we can code to the most likely scenarios and just raise errors
and abort for unexpected or infrequent use cases.   

Now we must send our rendered config template to the device.  This is not just copying a file but emulating typing the
file out line by line to the WLC.  Depending on the device and its current status it may not work well if we send each
line too fast.  The "config engine" on the device has to interpret the config as it receives each word/line.  If we send
things too fast it may not be able to keep up and skip some of the config we've sent.  This leaves us in a bad spot of 
incomplete or errored config, so we may get unexpected results.  Ok, we can slow down the sending of each word/line to
make sure the device gets all our config.  

So how exactly do we "make sure" our config was deployed correctly?  Now we should pull the current config of the device
after we insert and make sure that our lines (in the order specified) exist in the config.  Generally this works pretty
well but we find some situations where the device has changed the order of the lines from our template or perhaps the
spacing of the config is changed slightly from our template.  We have to go back to our template and make these changes
there to match.   

This works most of the time but we find situations where even if we slow down the insertion of the config to 5 seconds
per line we still get errors.  After some troubleshooting we find that these instances happen 






















