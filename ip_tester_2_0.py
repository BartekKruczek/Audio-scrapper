import requests


class ip_validator:
    def __init__(self, valid_path, raw_path, overwrite):
        self.valid_path = valid_path
        self.raw_path = raw_path
        self.overwrite = overwrite

        with open(
                self.raw_path, "r") as item:
            self.raw_list = item.read().split("\n")

        if self.overwrite is True:
            self.valid_list = []
        else:
            with open(
                    self.valid_path, "r") as item:
                self.valid_list = item.read().split("\n")

    def ip_check(self, current_ip):
        res = requests.get(
            "https://ipinfo.io/json",
            proxies={"http": current_ip, "https": current_ip},
            timeout=10,
        )
        print(res.status_code)
        if res.status_code == 200:
            self.valid_list.append(current_ip)

    def ip_validate(self):

        print("List to verify : ")
        print(self.raw_list)

        for current_ip in self.raw_list:
            print(current_ip)
            if self.overwrite is False:
                if current_ip in self.valid_list:
                    print("IP exists")
                else:
                    try:
                        self.ip_check(current_ip)
                    except:
                        continue
            elif self.overwrite is True:
                try:
                    self.ip_check(current_ip)
                except:
                    continue

        with open(
                self.valid_path, "w"
        ) as item:
            for ip in self.valid_list:
                if ip is self.valid_list[-1]:
                    item.write(str(ip))
                else:
                    item.write(str(ip) + "\n")

        print("IP saved")

        return self.valid_list
