#coding=utf-8
from django.http import HttpResponse
from django.template.context import RequestContext
from django.shortcuts import render_to_response,redirect
from django import forms
import ipmsg


class IpMsgForm(forms.Form):
    src=forms.IPAddressField(label="发送者IP")
    dst=forms.IPAddressField(label="目的IP"),
    src_mac=forms.CharField(max_length=17,label="源Mac地址")
    dst_mac=forms.CharField(max_length=17,label="目的Mac地址")
    user=forms.CharField(max_length=50,label="发送者姓名",required=True)
    host=forms.CharField(max_length=50,label="发送者主机名",required=True)
    msg=forms.CharField(widget=forms.Textarea)


def index(request):
    return render_to_response("index.html",context_instance=RequestContext(request))
    

#发送数据
def send_message(request):
    if request.method=='POST':
        form=IpMsgForm(request.POST)
        if form.is_valid():
            data=form.data
            ipmsg.send_msg(data)
            return HttpResponse("发送成功")
        else:
            return redirect('/')
    else:
        return redirect('/')
            
        
        

#更新表信息
def update_user(request,ip):
    pass


#增加一条记录
def add_user(request):
    pass