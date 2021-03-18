import os
import argparse

from btfix.exceptions import ArgumentException
from btfix.parser import parse_regfile, parse_linux_conf, write_config
from btfix.convertor import convert_configs


def _file_path(path: str, must_exist: bool) -> str:
    path = os.path.abspath(path)
    if must_exist and not os.path.exists(path):
        raise argparse.ArgumentTypeError(f'Path {path} does not exist')
    return path


def parse_argv():
    parser = argparse.ArgumentParser(description='Script for fixing bluetooth peripheral in dual boot')
    parser.add_argument(
        '-r',
        '--reg',
        required=True,
        type=lambda x: _file_path(x, must_exist=True),
        help='Path to Windows reg file'
    )
    parser.add_argument(
        '-l',
        '--linux',
        required=True,
        type=lambda x: _file_path(x, must_exist=True),
        help='Path to Linux config file'
    )
    parser.add_argument(
        '-o',
        '--output',
        type=lambda x: _file_path(x, must_exist=False),
        help='Path to file where result config will be stored - required when --inplace is not used'
    )
    parser.add_argument(
        '--inplace',
        action='store_true',
        dest='inplace',
        help='Make changes inplace in linux config file - backup will be created in /tmp'
    )
    options = parser.parse_args()
    if not options.inplace and not options.output:
        raise ArgumentException(f'--inplace or --ourput must be set')
    return options


def main():
    options = parse_argv()
    win_config = parse_regfile(options.reg)
    linux_config = parse_linux_conf(options.linux)
    linux_config, device_mac = convert_configs(win_config, linux_config)
    write_config(
        linux_config,
        options.linux if options.inplace else options.output,
        device_mac,
        options.inplace
    )
