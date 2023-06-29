with open("Python_scripts/Free_Proxy_List.txt", "r") as item:
    prox_list = item.read().split("\n")

pure_prox_list = []

for item in prox_list:
    pure_prox_list.append(item.split(",")[0][1:-2])

with open("Python_scripts/raw_prox_list.txt", "w") as item:
    for element in pure_prox_list:
        item.write(str(element) + "\n")