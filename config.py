import configparser


def get_section_key(section, key):
    filename = r"config.ini"
    config = configparser.ConfigParser()
    config.read(filename)
    return config[section][key]

