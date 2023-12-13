import subprocess
import sys
import socket
import json
import re

def is_valid_ipv4(address):
    """ IPv4アドレスとしての形式を検証 """
    try:
        socket.inet_aton(address)
        return address.count('.') == 3
    except socket.error:
        return False

def get_mac_address(ip_address):
    """ 指定したIPアドレスに対応するMACアドレスをARPテーブルから取得 """
    result = subprocess.run(["arp", "-an", ip_address], capture_output=True, text=True)
    mac_pattern = r"[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}"
    for line in result.stdout.split('\n'):
        if ip_address in line:
            match = re.search(mac_pattern, line)
            if match:
                return match.group(0)
    return None

def is_mac_in_whitelist(mac_address, whitelist_file):
    """ ホワイトリストにMACアドレスがあるかどうかをチェック """
    with open(whitelist_file, 'r') as file:
        data = json.load(file)
        whitelist = data.get("whitelist", [])
    return mac_address.lower() in (mac.lower() for mac in whitelist)

# ホワイトリストファイルのパス (JSONファイル)
whitelist_file = "./whitelist.json"

# コマンドライン引数からIPアドレスを取得
if len(sys.argv) > 1:
    ip_address = sys.argv[1]
else:
    print("IPアドレスが指定されていません。")
    sys.exit(1)

# IPv4アドレスの形式を検証
if not is_valid_ipv4(ip_address):
    print("false")
else:
    # ARPテーブルからMACアドレスを取得
    mac_address = get_mac_address(ip_address)
    if mac_address and is_mac_in_whitelist(mac_address, whitelist_file):
        print("true")
    else:
        print("false")