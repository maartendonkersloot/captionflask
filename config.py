import configparser


def get_section_key(section, key):
    filename = r"config.ini"
    config = configparser.ConfigParser()
    config.read(filename)
    return config[section][key]


def get_api_key():
    filename = r"config.ini"
    config = configparser.ConfigParser()
    config.read(filename)
    if config["general"]["environment"] == 1:
        return config["local"]["api_url"]

    if config["general"]["environment"] == 2:
        return config["home"]["api_url"]

    if config["general"]["environment"] == 3:
        return config["online"]["api_url"]

