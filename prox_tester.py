# NOTE !
# This script verifies prox with status codes and chooses functional one with good response dependent on timeout
# Simply copy n paste list of prox to raw_prox_list.txt and run this script
# It will verify the list and create output "valid_prox.txt" with good prox

import threading
import queue

import requests

with open("raw_prox_list.txt", "r") as item:
    prox_list = item.read().split("\n")

print(prox_list)


def prox_validator():
    valid = []
    for current_prox in prox_list:
        print(current_prox)
        try:
            res = requests.get(
                "https://ipinfo.io/json",
                proxies={"http": current_prox, "https": current_prox},
                timeout=10,
            )
            print(res.status_code)
            if res.status_code == 200:
                valid.append(current_prox)
        except:
            continue

    with open(
        "C:/Users/krucz/Documents/GitHub/Anonimowi-Akustycy/valid_prox.txt", "w"
    ) as item:
        for prox in valid:
            item.write(str(prox) + "\n")


prox_validator()
