from django.conf.urls.defaults import patterns,include

import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
js_path=os.path.abspath(os.path.join(os.path.dirname(__file__),'ipmsg/js'))
css_path=os.path.abspath(os.path.join(os.path.dirname(__file__),'ipmsg/css'))
urlpatterns = patterns('',
    (r'^$','ipmsg.views.index'),
    (r'^send_message/','ipmsg.views.send_message'),
    (r'^js/(?P<path>.*)$', 'django.views.static.serve',{'document_root':js_path,'show_indexes':True}),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve',{'document_root':css_path,'show_indexes':True}),
    (r'^admin/', include(admin.site.urls)),

)
