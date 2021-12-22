"""
Serves config functions
"""
import configparser


def get_api_key():
    """
    Get the api url from the config file
    Returns:
        [type]: The api url
    """
    filename = "../config.ini"
    config = configparser.ConfigParser()
    config.read(filename)
    if config["general"]["environment"] == "1":
        return config["local"]["api_url"]

    if config["general"]["environment"] == "2":
        return config["home"]["api_url"]

    if config["general"]["environment"] == "3":
        return config["online"]["api_url"]
    return None
