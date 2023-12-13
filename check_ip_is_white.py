import subprocess
import sys
import socket
import json

def is_valid_ipv4(address):
    """ IPv4アドレスとしての形式を検証 """
    try:
        socket.inet_aton(address)
        return address.count('.') == 3
    except socket.error:
        return False

def is_mac_in_whitelist(ip_address, whitelist_file):
    """ ARPテーブルからMACアドレスを取得し、ホワイトリストにあるかどうかをチェック """
    result = subprocess.run(["arp", "-an"], capture_output=True, text=True)
    mac_address = None
    for line in result.stdout.split('\n'):
        if ip_address in line:
            mac_address = line.split()[3]
            break

    if mac_address:
        with open(whitelist_file, 'r') as file:
            data = json.load(file)
            whitelist = data.get("whitelist", [])
        return mac_address.lower() in (mac.lower() for mac in whitelist)
    return False

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
    # MACアドレスがホワイトリストにあるかチェック
    if is_mac_in_whitelist(ip_address, whitelist_file):
        print("true")
    else:
        print("false")