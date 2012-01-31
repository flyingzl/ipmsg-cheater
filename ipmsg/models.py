#coding=utf-8
from django.db import models
class IpMsg(models.Model):
    ip=models.IPAddressField(primary_key=True)
    mac=models.CharField(max_length=17)
    sender=models.CharField(max_length=50,verbose_name="发送者")
    sender_host=models.CharField(max_length=50,verbose_name="发送者主机名")
    sender_nick=models.CharField(max_length=50,verbose_name="发送者昵称",null=True)
    
    def __unicode__(self):
        return self.ip+"--->"+self.sender_nick
    
    class Meta:
        verbose_name_plural='飞鸽用户列表'
        db_table='ipmsg'
        ordering=['ip']