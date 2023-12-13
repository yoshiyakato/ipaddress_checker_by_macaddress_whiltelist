【概要】

本スクリプトは maccaddress のホワイトリストを jsonファイルに保存しておき
WEBサーバーからみてアクセスされたIPアドレスがwhitelistにあるmacアドレスであるかどうか？
を確認しています。

arp -an コマンドが
? (172.31.108.16) at 00:ae:6b:0f:2f:3b [ether] on ens160
? (172.31.59.209) at 00:ae:3a:d0:d9:cd [ether] on ens160

みたいな出力を出してくれることを利用して　macaddress を拾い出し

whitelist.json　に保存されたホワイトリストのなかにあるば場合は True 
ない場合や おかしな入力の場合は false を返すようになっています。
{
    "whitelist": [
        "00:28:f8:ED:21:69",
        "04:d4:c4:91:fe:27"
    ]
}

【使い方例】

hostname:~/ipaddress_checker_by_macaddress_whiltelist$ python3 ./check_ip_is_white.py  10.1.2.32
false
hostname:~/ipaddress_checker_by_macaddress_whiltelist$ python3 ./check_ip_is_white.py  10.1.2.101
true

【注意点】
このスクリプトは arp -an <ipaddress> が arpテーブルを表示し該当するmacアドレスを応答することを利用して
作成しています。

【参考・注意】
このスクリプトを生成してくれた ChatGPTとのやり取り
https://chat.openai.com/share/82a3346b-5dc3-45c8-9415-826843f66964
リスクを加味してセキュリティ強化の一助にしていただければありがたいです。
