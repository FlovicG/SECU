from django.conf.urls import url
from otree.default_urls import urlpatterns

from . import views

urlpatterns.append(url(r'^primo_fmr/export/$', 'primo_fmr.views.export_view_json', name="primo_fmr.export_view_json", ))
