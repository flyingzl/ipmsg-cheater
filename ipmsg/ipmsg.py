#coding=utf-8
import dpkt
import sendpkt
from socket import inet_aton
from time import strftime

#本地网关MAC地址,可以通过如下方式获取:
#C:\Users\Administrator>arp -a
#接口: 192.168.0.100 --- 0xb
#  Internet 地址         物理地址                                             类型
#  192.168.0.1    1c-af-f7-c0-65-a8     动态
MASK_MAC='00-0f-e2-7e-59-c6'


#获得本机Mac地址
def get_local_mac():
    import uuid
    mac=uuid.uuid1().hex[-12:]
    return '-'.join([mac[(i-1)*2:2*i] for i in range(1,7)])

def send_msg(kwargs):
    local_ip=inet_aton(kwargs['src'])
    remote_ip=inet_aton(kwargs['dst'])
    local_mac=pack_mac(kwargs['src_mac'])
    #判断remote_ip和local_ip是否在同一个网段
    remote_mac=pack_mac(kwargs['dst_mac'])\
            if trans(kwargs['src'])==trans(kwargs['dst']) else pack_mac(MASK_MAC)
    host=kwargs['host']
    user=kwargs['user']
    msg=kwargs['msg']
    
    device=sendpkt.findalldevs()[0]  
    #飞鸽监听本地的UDP 2425端口   
    udp=dpkt.udp.UDP(dport=2425,sport=2425)
    #向飞鸽发送消息命令字
    #6291458表示下线
    #6291457表示上线
    #288表示发送信息
    msg="1_lbt4_10#65664#%s#0#0#0:%s:%s:%s:288:%s" \
        %(kwargs['src_mac'].replace('-',''),int(strftime('%m%d%H%M%S'))+1000000000,user,host,msg)
    
    msg=msg.encode("gbk")
    udp.data+=msg
    udp.ulen=len(udp)
    
    ip=dpkt.ip.IP(src=local_ip,dst=remote_ip,data=udp,p=dpkt.ip.IP_PROTO_UDP)
    #重新计算ip的长度,不然消息发送不出去
    ip.len=len(ip)
    
    ether=dpkt.ethernet.Ethernet(
        dst=remote_mac,
        src=local_mac,
        type=0x0800,
        data=ip
    )
    sendpkt.sendpacket(str(ether),device)

#判断两个ip地址是否在同一个网段
def trans(ip,mask='255.255.255.0'):
    str=[]
    ip=ip.split(".")
    mask=mask.split(".")
    for index,item in enumerate(ip):
        str.append(int(item)&int(mask[index]))
    return str

#将网卡地址转为以太网Mac地址
#例如将"08-00-27-ba-f7-e5"转为"\x08\x00'\xba\xf7\xe5"
def pack_mac(mac,pattern='-'):
    mac=mac.split(pattern.lower())
    return "".join([chr(int('0x'+x,16)) for x in mac])

if __name__=="__main__":
    s={
       'src':'10.4.44.87',
       'dst':'10.4.45.90',
       'dst_mac':'00-1D-92-AA-8A-CA',
       'src_mac':'08-00-27-BA-F7-E5',
       'host':u'测试',
       'user':u'测试',
       'msg':u'测试信息'
    }
    send_msg(s)


