from django.conf.urls import url
from otree.default_urls import urlpatterns
from django.contrib.auth.decorators import login_required
import primo_fmr
import ostende2


urlpatterns.append(url(r'^livetree/$', 'redirect.views.get_livetree_redir', name="redirection", ))
urlpatterns.append(url(r'^eli/$', 'redirect.views.get_eli_redir', name="redirection", ))
urlpatterns.append(url(r'^eth/$', 'redirect.views.get_eth_redir', name="redirection", ))

urlpatterns.append(url(r'^ajax/sent/$', 'ajax.models.sent_ajax', name="ajax", ))
urlpatterns.append(url(r'^ajax/get/$', 'ajax.models.get_ajax', name="ajax", ))

urlpatterns.append(url(r'^primo_fmr/export/$', 'primo_fmr.views.export_view_json', name="primo_fmr.export_view_json", ))

urlpatterns.append(url(r'^test/$', 'redirect.views.get_test_redir', name="redirection", ))

# urlpatterns.append(url(r'^primo_fmr/experts/$', login_required(primo_fmr.views.ExpertsView.as_view()), name="experts", ))
# URL to dump the database
urlpatterns.append(url(r'^ostende2/export/$', 'ostende2.views.export_view_json', name="experts", ))

urlpatterns.append(url(r'^sensdutravail/vert/$', 'redirect.views.get_sensdutravail_vert_redir', name="bleus", ))
urlpatterns.append(url(r'^sensdutravail/rouge/$', 'redirect.views.get_sensdutravail_rouge_redir', name="rouges", ))

urlpatterns.append(url(r'^1509/$', 'redirect.views.get_room_redir', name="room", ))

# urlpatterns.append(url(r'^send_wordcloud/$', 'innov_sante_sociale.models.send_wordcloud', name="send_words", ))
# urlpatterns.append(url(r'^get_player_wordcloud/(?P<group_pk>[0-9]{1})/$', 'innov_sante_sociale.models.get_player_wordcloud', name="wordcloud", ))
# urlpatterns.append(url(r'^get_adminreport_wordcloud/(?P<subsession_pk>[0-9]{1})/$', 'innov_sante_sociale.models.get_adminreport_wordcloud', name="wordcloud", ))

urlpatterns.append(url(r'^avocats/compute/$', 'avocats.models.compute_results', name="avocats_compute", ))
