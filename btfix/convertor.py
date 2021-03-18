from typing import Tuple


def _convert_key(win_key: str) -> str:
    # Copy LTK to LongTermKey with capital characters and no comma
    win_key = win_key.replace(',', '')
    return win_key.upper()


def _convert_rand(win_rand: str) -> str:
    # Reverse ERand and convert the hexadecimal to the decimal
    erand_bytes = win_rand.split(',')
    erand_bytes.reverse()
    rand = ''.join(erand_bytes)
    return str(int(rand, 16))


def _convert_ediv(win_ediv: str) -> str:
    # Convert the hexadecimal of EDIV to the decimal
    return str(int(win_ediv, 16))


def _convert_device_mac(device_mac: str) -> str:
    # Convert to uppercase and separate bytes in hexadecimal by colon character
    device_mac = device_mac.upper()
    device_mac = ':'.join([device_mac[i:i + 2] for i in range(0, len(device_mac), 2)])
    return device_mac


def convert_configs(win_config: dict, linux_config: dict) -> Tuple[dict, str]:
    linux_config['LongTermKey']['Key'] = _convert_key(win_config['LTK'])
    linux_config['LongTermKey']['Rand'] = _convert_rand(win_config['ERand'])
    linux_config['LongTermKey']['EDiv'] = _convert_ediv(win_config['EDIV'])
    device_mac = _convert_device_mac(win_config['device_mac'])
    return linux_config, device_mac
