from django.conf.urls.defaults import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('mine.views',
    url(r'^form/$', 'form'),
    url(r'^thanks/(?P<name>\w+)/$', 'thanks'),
    url(r'^ajax/$', 'ajax'),
    url(r'^json/$', 'json'),
    url(r'^tabs/(?P<tab>\w+)/$', 'tabs_ajax'),                       
    url(r'^tabs/$', 'tabs'),
#    url(r'^sensors/Presence/$', 'binary_sensors'),
    url(r'^sensors/(?P<type_name>\w+)/(?P<name>\w+)/json$', 'json_sensor'),
    url(r'^sensors/(?P<type_name>\w+)/(?P<name>\w+)/init$', 'json_sensor_init'),
    url(r'^sensors/(?P<type_name>\w+)/(?P<name>\w+)/$', 'sensor'),
    url(r'^sensors/$', 'sensors'),
    url(r'^commands/(?P<name>\w+)/$', 'command'),
    url(r'^commands/$', 'commands'),
    url(r'^home/$', 'home'),
    url(r'^editor/$', 'editor'),
    url(r'^editors/(?P<name>\w+)/$', 'editor'),
    url(r'^editors/(?P<name>\w+)/json$', 'json_editor'),
    url(r'^editors/$', 'editors'),
    url(r'^reset/$', 'reset'),
)
