【使い方例】

hostname:~/ipaddress_checker_by_macaddress_whiltelist$ python3 ./check_ip_is_white.py  10.1.2.32
false
hostname:~/ipaddress_checker_by_macaddress_whiltelist$ python3 ./check_ip_is_white.py  10.1.2.101
true

【注意点】
このスクリプトは arp -an <ipaddress> が arpテーブルを表示し該当するmacアドレスを応答することを利用して
作成しています。

【参考】
このスクリプトを生成してくれた ChatGPTとのやり取り
https://chat.openai.com/share/82a3346b-5dc3-45c8-9415-826843f66964
リスクを加味してセキュリティ強化の一助にしていただければありがたいです。



