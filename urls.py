from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^describe_instances$', 'appscale_monitor.appscale.views.describe_instances'),
    (r'^$', 'appscale_monitor.appscale.views.home'),
    (r'^home$', 'appscale_monitor.appscale.views.home'),
    (r'^homepost$', 'appscale_monitor.appscale.views.homepost'),
    (r'^editpost$', 'appscale_monitor.appscale.views.editpost'),
    (r'^addkeypair$', 'appscale_monitor.appscale.views.addkeypair'),
    (r'^addkeypairpost$', 'appscale_monitor.appscale.views.addkeypairpost'),
    (r'^terminate_instances$', 'appscale_monitor.appscale.views.terminate_instances'),
    (r'^run_instances$', 'appscale_monitor.appscale.views.run_instances'),
    (r'^run_instances_post$', 'appscale_monitor.appscale.views.run_instances_post'),
    (r'^upload_app$', 'appscale_monitor.appscale.views.upload_app'),
    (r'^upload_app_post$', 'appscale_monitor.appscale.views.upload_app_post'),
    (r'^remove_app$', 'appscale_monitor.appscale.views.remove_app'),
    (r'^remove_app_post$', 'appscale_monitor.appscale.views.remove_app_post'),
    (r'^reset_pwd$', 'appscale_monitor.appscale.views.reset_pwd'),
    (r'^reset_pwd_post$', 'appscale_monitor.appscale.views.reset_pwd_post'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT})
    # Example:
    # (r'^appscale_monitor/', include('appscale_monitor.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
