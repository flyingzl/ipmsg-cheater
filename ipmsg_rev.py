#coding=utf-8
import pcap,dpkt
import socket
import sqlite3
pc=pcap.pcap()
pc.setfilter("udp port 2425")


#??1234567890ab??????12-34-56-78-90-ab
def format_mac(mac):
    if len(mac)!=12:
        return ''
    return '-'.join([mac[(i-1)*2:2*i] for i in range(1,7)])

#????????mac????"\x08\x00'\xba\xf7\xe5"????"08-00-27-ba-f7-e5"
def decode_mac(mac):
    return '-'.join(['%02x'%ord(i)for i in mac])
    
for i,j in pc:
    ethernet=dpkt.ethernet.Ethernet(j)
    ip=ethernet.data
    udp=ip.data
    
    
    if socket.inet_ntoa(ip.dst)==socket.gethostbyname(socket.gethostname()):
        #data??????1_lbt4_10#128#002481627512#0#0#0:1276557510:Administrator:MICROSO-697TGLD:6291459:nick
        data=udp.data.decode('gbk').split(":")
        #??????????????
        if data[4]=='6291459' or data[4]=='259':
            mac_array=data[0].split('#')
            mac=format_mac(mac_array[2]) if len(mac_array)>=3 else decode_mac(ethernet.src)
            user=data[2]
            host=data[3]
            nickname=data[5].split("\x00")[0]
            
            cursor=sqlite3.connect("ipmsg.db")
            row=cursor.execute("select ip from ipmsg where ip='%s'"%(socket.inet_ntoa(ip.src)))
            if len(row.fetchall())==0:
                sql="insert into ipmsg values('%s','%s','%s','%s','%s')"\
                    %(socket.inet_ntoa(ip.src),mac,user,host,nickname)
                cursor.execute(sql)
                cursor.commit()
                cursor.close()
                print 'ok'