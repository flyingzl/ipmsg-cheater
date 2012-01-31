from django.conf.urls.defaults import patterns
from django.views.static import serve
import views
import os


#js_path=os.path.abspath(os.path.dirname(__file__),'js')
#patterns('',
#    (r'^send_message/',views.send_message),
#    (r'^js/(?P<path>.*)$', serve,{'document_root':js_path}),
#)
