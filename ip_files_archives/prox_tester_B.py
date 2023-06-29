import requests

prox_list = []

with open(
    "Python_scripts/raw_prox_list.txt", "r"
) as item:
    prox_list = item.read().split("\n")

print(prox_list)


def adding_valid():
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
    return valid


valid = adding_valid()

print(valid)

with open(
    "Python_scripts/valid_prox.txt", "w"
) as item:
    for prox in valid:
        item.write(str(prox) + "\n")
    print("Zapisano IP")
