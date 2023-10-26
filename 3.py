Network Namespace



sudo ip netns add helloworld
このコマンドで新しいネットワークスペースを作れる　addのあとがスペースの名前
正しくできて ip net list とうつと
helloworld　とスペース名が出てきます

sudo ip netns exec helloworld ip addres show
今作った環境でサブコマンドを実行します
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
明らかに　ip addres show のときと文章が変わっています
Network Spaceを使うとネットワーク的には独立した空間を生み出せます
もちろん独立しているのはネットワークインターフェースだけではありません
ルーティングテーブルも独立しています

なお不要になったスペースを消すコマンドはこれです
sudo ip netns delete helloworld

あるいはLinuxを再起動すると消えます

３．２　　つないで見る
  sudo ip netns add ns1
  sudo ip netns add ns2
これでns1 ns2のネットワークができます

sudo ip link add ns1-veth0 type veth peer name ns2-veth0
 
veth0と言う仮想的なネットワークインターフェイスでネットワークスペースをつなげます
vethを作るには ip link add サブコマンドを使います

 ip link show |grep veth
4: ns2-veth0@ns1-veth0: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
5: ns1-veth0@ns2-veth0: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
作成したvethは２つのネットワークスペースが対になってできています
sudo ip link set ns1-veth0 netns ns1
sudo ip link set ns2-veth0 netns ns2
これでvethがネットワークスペースで使えます
試しにネットワークスペースをつかわずにip link show を試してみる
ip link show |grep veth
vethインターフェイスが見えなくなった
変わりにそれぞれのネットワースペースにvethが移動している
sudo ip netns exec ns1 ip link show | grep veth
5: ns1-veth0@if4: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
仮想的なLAN同士でつながっている
IPを使って通信するためにはIPアドレスが必要になる
つまりvethにIPアドレスを付与しなければならない
sudo ip netns exec ns1 ip addres add 192.0.2.1/24 dev ns1-veth0
sudo ip netns exec ns2 ip addres add 192.0.2.2/24 dev ns2-veth0
これでns1.ns2にアドレスを付与できた

次にネットワークインターフェイスをアップさせます
sudo ip netns exec ns1 ip link show ns1-veth0 | grep state
5: ns1-veth0@if4: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
sudo ip netns exec ns2 ip link show ns2-veth0 | grep state
4: ns2-veth0@if5: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000

アップさせます
sudo ip netns exec ns1 ip link set ns1-veth0 up
sudo ip netns exec ns2 ip link set ns2-veth0 up
しました

用意できたのでpingをする
sudo ip netns exec ns1 ping -c 3 192.0.2.2
PING 192.0.2.2 (192.0.2.2) 56(84) bytes of data.
64 bytes from 192.0.2.2: icmp_seq=1 ttl=64 time=0.065 ms
64 bytes from 192.0.2.2: icmp_seq=2 ttl=64 time=0.117 ms
64 bytes from 192.0.2.2: icmp_seq=3 ttl=64 time=0.117 ms

--- 192.0.2.2 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2039ms
rtt min/avg/max/mdev = 0.065/0.099/0.117/0.024 ms

ロストしてないのでできてます

３．４
sudo ip netns add ns1
sudo ip netns add router
sudo ip netns add ns2
routerは橋渡しの役割を持ちます
sudo ip link add ns1-veth0 type veth peer name gw-veth0
sudo ip link add ns2-veth0 type veth peer name gw-veth1
vethを２つにします

ネットワークスペースに所属させます
sudo ip link set ns1-veth0 netns ns1
sudo ip link set gw-veth0 netns router
sudo ip link set gw-veth1 netns router
sudo ip link set ns2-veth0 netns ns2
 やったらupさせてください

 sudo ip netns exec ns1 ip addres add 192.0.2.1/24 dev ns1-veth0
sudo ip netns exec router ip addres add 192.0.2.254/24 dev gw-veth0


sudo ip netns exec router ip addres add 198.51.100.254/24 dev gw-veth1
sudo ip netns exec ns2 ip addres add 198.51.100.1/24 dev ns2-veth0







