import configparser


def get_api_key():
    filename = "../config.ini"
    config = configparser.ConfigParser()
    config.read(filename)
    if config["general"]["environment"] == "1":
        return config["local"]["api_url"]

    if config["general"]["environment"] == "2":
        return config["home"]["api_url"]

    if config["general"]["environment"] == "3":
        return config["online"]["api_url"]
