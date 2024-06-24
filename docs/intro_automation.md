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

This works most of the time but we find a situations where even if we slow down the insertion of the config to 5 seconds
per line we still get errors.  After some troubleshooting we find that these instances happen when the CPU usage of the
WLC is at 80% or higher.  The high CPU indicates the controller is busy doing other tasks or something has gone wrong.
Now we must check the CPU before we begin the configuration.  So we code that.

...

The point of explaining all this is to illustrate that tasks we believe to be simple and straightforward can become
cumbersome and complex in practice.   Additionally, the code we've just written is very specific to this use case.
Assume we wanted to deploy some configuration to a network switch, a linux host, or a windows host.  We now have more
edge cases to take into consideration.  If we're lucky to have good programmers and who also have a deep understanding
of the platforms we can modularize the code for re-use and composition.

### Automation Frameworks

Lucky for us we can stand on the shoulders of giants and those who have come before us and leverage tools built for this 
specific problem domain.

 - [Ansible](https://docs.ansible.com/ansible/latest/getting_started/introduction.html)
 - [Salt](https://docs.saltproject.io/en/master/topics/tutorials/walkthrough.html#salt-in-10-minutes/)
 - [Terraform](https://www.terraform.io/)
 - [Nornir](https://nornir.readthedocs.io/en/latest/)
 - [Cisco Catalyst Center](https://www.cisco.com/site/us/en/products/networking/catalyst-center/index.html)

Some of these are vendor specific, open source, closed source, cater to networking, or cloud environments and services;
there are lots to choose from based on the specific needs of your situation.  Tooling can be used in concert with each
other to cover many use cases and platforms.

For our demo today we will focus on using Ansible and further focus on network automation.

## Idempotency

Before we get into some details we should cover the idea of idempotency.

> Idempotence, is the property of certain operations in mathematics and computer science whereby they can be applied
> multiple times without changing the result beyond the initial application.
[Wikipedia](https://en.wikipedia.org/wiki/Idempotence)

For our use this describes the idea that if we make a change to a system, by some function, that repeating that function
makes no additional change to the system other than the change that was initially made.  

For example if we wanted to add a wireless lan config to our WLC we can run a function that does that.  If we run that
function again we're not going to add "additional" config to the system.  The function should recognize that the config
we want to exist is already there and thus not perform a change.   

The idea here is that we feel comfortable running an ansible playbook multiple times and it will make no changes once
the desired state of the device is achieved.

## Declarative vs Imperative Functions

Most of the automation platforms and frameworks use a "declarative" style of interaction.  This means that we describe
the intended state of the system and not necessarily the exact steps to get there.  Obviously those have to bd defined
somewhere, that part is usually covered by the functions provided by the automation platform itself.  We don't (usually)
have to define those bits.  We tell the platform what we want the system to look like and the platform will decide what
steps are needed to achieve that state based on the situation.   

The exact actions that take place to achieve the desired state are written in the "imperative" manner.  The difference 
here is subtle but should be understood. Imperative is a stringent set of individual steps that achieve the desired
state.  Whereas declarative defines the ultimate state of the system and composes the steps required to achieve the final
state based on the current state.
