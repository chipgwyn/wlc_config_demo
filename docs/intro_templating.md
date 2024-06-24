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

You'll notice there are several words surrounded by {{ }}.  These are variables that can be defined elsewhere.
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

```shell
cd ~/wlc_config_demo
cd other
ls -la
```

Files:
 - data.yml: a [YAML](https://en.wikipedia.org/wiki/YAML#Basic_components) formatted file that contains our variable definitions
 - definition-wlan.j2: A template file written using the [Jinja](https://jinja.palletsprojects.com/en/3.1.x/templates/) templating format
 - demo.py: a python script that reads in the data.yml file and then renders the jinja template

Variable definitions in the data.yml file:

```shell
$ cat data.yml
wlan_name: wlan-pod1
wlan_id: 20
wlan_ssid: POD1-NeT
wlan_password: $%mySuperSeCRetPas44**
```

Running the `demo.py` script:

```shell
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

Feel free to play around with the files to produce different results.  Not required for this lab however.   
