#!/usr/bin/python3

import subprocess

with open("configs/urls.txt") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            shelter, url = line.split(" ")
            subprocess.check_output(["firefox", "-new-tab", "-url", url])
