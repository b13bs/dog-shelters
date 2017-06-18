# dog-shelters

Description
======
The script parses the webpages of different shelters and for each, it extracts the number of dogs available for adoption. The execution should be iterative, like every hour with a cronjob. The number found with the webpage parsing if compared to the previous number of each specific shelter and an alert is generated if the number is higher, i.e. new dogs are available for adoptions.


Motivation
======
I am in the process of adopting a dog and I want to do it through a shelter. I noticed that depending on the search criteria of the animal, new ones can be adopter pretty quickly. It got me tot he idea to create a script that parse various specified shelters and notifiy me if there are new dogs.

Usage
======
The script is in Python3 and needs a few Python modules pretty standards for Webpage scraping.
\$ pip3 install -r requirements.txt

A config file must be created by the user to allow notifying and API keys. This configuration file is a Python file named "secrets.py" like this one:
pushbullet_key = "foo"
key = "bar"
secret = "baz"

The function "util.notify_me()" could be overwrite to the prefered notification method. I implemented mine with [PushBullet](https://www.pushbullet.com/) as I use it for my notification center.

TODO
======
Shelters to add:
none
