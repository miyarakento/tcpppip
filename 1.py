TCP/IP１章
　コンピューターの通信に関する機能を階層構造で規定している
　　アプリケーション層
　　プレゼンテーション層
　　セッション層
　　トランスポート層
　　ネットワーク層
　　データリンク層
　　物理（フィジカル層）
　IPはネットワーク層に位置する
　TCPはトランスポート層に位置している

プロトコルとは
「決めごと」です

pingコマンドを用いてTCP/IPのネットワーク疎通を確認することができます。
返信がこれば正常で来なければ何かしらの問題があるのかもしれない
　　　　　　　　　　ping -c 4 8.8.8.8
コマンドがうまく実行できるとこのような返信が来る
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.

64 bytes from 8.8.8.8: icmp_seq=1 ttl=63 time=30.5 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=63 time=34.9 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=63 time=30.2 ms
この３行は8.8.8.8というIPアドレスを持った通信相手から３回応答があったことを示しています pingにつけた３は応答を要求するメッセージを３回送るという意味でした


--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2007ms
rtt min/avg/max/mdev = 30.217/31.872/34.865/2.120 ms
 
  3 received, 0% packet loss, time 2007msという表示は「３個要求を送って３個帰ってきました。失われた内容は０％です。」という意味になっています
  また後続の”ave”は応答するまでに３１mm秒かかったことを表しています


  IPアドレスとは
  IPアドレスというものは、IP（internet protocol:インターネット・プロトコル）というプロトコルで通信するのに必要な識別子の一つです
名前にインターネットと入ってるようにIPはインターネットの根幹をなす１つです

         ip addres show
         
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 02:31:13:65:d8:9d brd ff:ff:ff:ff:ff:ff
    inet 10.0.2.15/24 metric 100 brd 10.0.2.255 scope global dynamic enp0s3
       valid_lft 82240sec preferred_lft 82240sec
    inet6 fe80::31:13ff:fe65:d89d/64 scope link
       valid_lft forever preferred_lft forever
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:b7:bd:25 brd ff:ff:ff:ff:ff:ff
    inet 192.168.56.10/24 brd 192.168.56.255 scope global enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:feb7:bd25/64 scope link
       valid_lft forever preferred_lft forever

 inet 127.0.0.1/8 scope host lo　127.0.0.1は自分のコンピュータ

　　　　　 コンピュータの流れを覗き見る通信
sudo tcpdump -tn -i any icmp
これを他のターミナルで打ち込んだあとにpingをとばします
sudo tcpdump -tn -i any icmp
tcpdump: data link type LINUX_SLL2
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on any, link-type LINUX_SLL2 (Linux cooked v2), snapshot length 262144 bytes
enp0s3 Out IP 10.0.2.15 > 8.8.8.8: ICMP echo request, id 2, seq 1, length 64
enp0s3 In  IP 8.8.8.8 > 10.0.2.15: ICMP echo reply, id 2, seq 1, length 64
enp0s3 Out IP 10.0.2.15 > 8.8.8.8: ICMP echo request, id 2, seq 2, length 64
enp0s3 In  IP 8.8.8.8 > 10.0.2.15: ICMP echo reply, id 2, seq 2, length 64
enp0s3 Out IP 10.0.2.15 > 8.8.8.8: ICMP echo request, id 2, seq 3, length 64
enp0s3 In  IP 8.8.8.8 > 10.0.2.15: ICMP echo reply, id 2, seq 3, length 64

tcpdumpコマンドに指定したオプションの補足
ーｔ　
時間に関するものを表示させない
ーｎ
IPアドレスを逆引きせずそのまま表示するもの
ーi
パケットキャプチャする対象のネットワークインターネットフェイスを指定します


ip route show

default via 10.0.2.2 dev enp0s3 proto dhcp src 10.0.2.15 metric 100
10.0.2.0/24 dev enp0s3 proto kernel scope link src 10.0.2.15 metric 100
10.0.2.2 dev enp0s3 proto dhcp scope link src 10.0.2.15 metric 100
10.0.2.3 dev enp0s3 proto dhcp scope link src 10.0.2.15 metric 100
192.168.56.0/24 dev enp0s8 proto kernel scope link src 192.168.56.10



