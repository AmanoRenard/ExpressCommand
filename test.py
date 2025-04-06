# from config_accessor.core import ConfigAccessor

# config = ConfigAccessor()

# print(config.get_selection_value("is_open"))

# import sys
# print([sys.executable] + sys.argv)

import requests
response = requests.get("https://version.chamiko.com/ExpressCommand", timeout=5, proxies={"http": None, "https": None})
data = response.json()
print(data["msg"])