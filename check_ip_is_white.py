import subprocess
import sys
import socket
import json
import re

def is_valid_ipv4(address):
    """
    IPv4アドレスとしての形式を検証する関数。
    引数 'address' が正しいIPv4アドレスの形式であるかを確認し、
    結果をブール値（TrueまたはFalse）で返す。
    """
    try:
        socket.inet_aton(address)  # IPv4アドレスの形式をチェック
        return address.count('.') == 3  # 正しいアドレスには3つのドットが含まれる
    except socket.error:
        return False  # 不正な形式の場合はFalseを返す

def get_mac_address(ip_address):
    """
    指定したIPアドレスに対応するMACアドレスをARPテーブルから取得する関数。
    'arp -an' コマンドを実行し、出力から正規表現を使ってMACアドレスを抽出する。
    対応するMACアドレスが見つかれば、それを返す。見つからない場合はNoneを返す。
    """
    result = subprocess.run(["arp", "-an", ip_address], capture_output=True, text=True)
    mac_pattern = r"[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}"  # MACアドレスの正規表現パターン
    for line in result.stdout.split('\n'):
        if ip_address in line:
            match = re.search(mac_pattern, line)
            if match:
                return match.group(0)  # 正しいMACアドレスを返す
    return None  # MACアドレスが見つからなければNoneを返す

def is_mac_in_whitelist(mac_address, whitelist_file):
    """
    ホワイトリストに指定されたMACアドレスが含まれているかどうかをチェックする関数。
    JSONファイルからホワイトリストを読み込み、指定されたMACアドレスが
    リスト内に存在するかどうかを判定する。
    """
    with open(whitelist_file, 'r') as file:
        data = json.load(file)  # JSONファイルを読み込む
        whitelist = data.get("whitelist", [])  # ホワイトリストを取得
    return mac_address.lower() in (mac.lower() for mac in whitelist)  # 大文字小文字を無視してチェック

# ホワイトリストファイルのパス (JSONファイル)
whitelist_file = "./whitelist.json"

# コマンドライン引数からIPアドレスを取得
if len(sys.argv) > 1:
    ip_address = sys.argv[1]
else:
    print("IPアドレスが指定されていません。")
    sys.exit(1)  # 引数が不足している場合はプログラムを終了

# IPv4アドレスの形式を検証
if not is_valid_ipv4(ip_address):
    print("false")  # 不正なIPアドレスの場合はfalseを出力
else:
    # ARPテーブルからMACアドレスを取得
    mac_address = get_mac_address(ip_address)
    # MACアドレスがホワイトリストにあるかチェック
    if mac_address and is_mac_in_whitelist(mac_address, whitelist_file):
        print("true")  # ホワイトリストに含まれている場合はtrueを出力
    else:
        print("false")  # ホワイトリストに含まれていない場合はfalseを出力