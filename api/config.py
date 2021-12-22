"""
Serves the get_api_key function which returns the current api_url for the environment we are in.
"""
import configparser


def get_api_key():
    """
    Get the api_key from the config file.
    Returns:
        [type]: The api url for the environment we are in.
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
