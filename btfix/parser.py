import re
import os
import time
import shutil
import configparser

from btfix.exceptions import RegFileParseException


def _convert_to_ini(reg: str) -> str:
    section_re = re.compile(r'^\[.+]$')
    variable_re = re.compile(r'^\"(.+)\"=[\w()]+:(.+)')
    ini_lines = []
    for line in reg.split('\n'):
        if not line:
            continue
        if section_re.match(line):
            ini_lines.append(line.strip())
            continue
        variable_match = variable_re.match(line)
        if variable_match:
            ini_lines.append(f'{variable_match.group(1)}={variable_match.group(2)}')
    return '\n'.join(ini_lines)


def parse_regfile(path: str) -> dict:
    with open(path, encoding='utf-16le') as file:
        reg = file.read()
    raw_ini = _convert_to_ini(reg)
    parser = configparser.ConfigParser()
    parser.optionxform = str
    parser.read_string(raw_ini)
    section_re = re.compile(
        r'HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\BTHPORT\\Parameters\\Keys\\[0-9a-f]+\\([0-9a-f]+)'
    )
    for section in parser.sections():
        result = section_re.match(section)
        if result:
            config = dict(parser.items(section))
            config['device_mac'] = result.group(1)
            return config
    raise RegFileParseException('Regfile device section not found')


def parse_linux_conf(path: str) -> dict:
    parser = configparser.ConfigParser()
    parser.optionxform = str
    parser.read(path)
    config = dict(parser)
    return config


def _rename_dir(path: str, device_mac: str):
    dir_path = os.path.dirname(path)
    dir_name = os.path.basename(dir_path)
    file_name = os.path.basename(path)
    if os.path.basename(dir_name) != device_mac:
        base_dir = os.path.dirname(dir_path)
        new_dir = os.path.join(base_dir, device_mac)
        path = os.path.join(new_dir, file_name)
        os.rename(dir_path, new_dir)
    return path


def write_config(linux_config: dict, path: str, device_mac, inplace: bool = False):
    if inplace:
        shutil.copyfile(path, f'/tmp/bluetooth_backup_{time.time()}')
        path = _rename_dir(path, device_mac)
    parser = configparser.ConfigParser()
    parser.optionxform = str
    parser.read_dict(linux_config)
    with open(path, 'w') as file:
        parser.write(file, space_around_delimiters=False)
