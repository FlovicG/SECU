# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants

from django.http import HttpResponse, HttpResponseRedirect
import random


#################################
def get_redir(request):
    if request.session.get("otree"):
        ofi = open('./wf2016/sessionState.txt', 'r')
        sessionState = ofi.read()
        ofi.close()
        if sessionState=="running":
            cookie_val = request.session["otree"]
            return HttpResponseRedirect(cookie_val)
        else:
            return HttpResponseRedirect(Constants.url_aulamaxima)
    else:
        return HttpResponseRedirect(Constants.url_aulamaxima)


#################################
# -------------------------------
class InformationPage(Page):
    timeout_seconds = 60

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        parti = self.request.build_absolute_uri(self.player.participant._start_url())
        self.request.session["otree"] = parti
        self.request.session.set_expiry(18000)


# -------------------------------
class MessagePage(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        messageFromExperts = "2 euros"
        if self.group.group_advice == Constants.c_advice[0]:
            # partenaires_non_cooperatifs
            messageFromExperts = "0 euros"
        elif self.group.group_advice == Constants.c_advice[1]:
            # partenaires_cooperatifs
            messageFromExperts = "5 euros"
        return {
            'messageFromExperts': messageFromExperts,
        }


# -------------------------------
class PlayPage(Page):
    form_model = models.Player
    form_fields = ['contribution']
    timeout_seconds = 30
    timeout_submission = {'contribution': int(Constants.endowment/2)}

    def is_displayed(self):
        ofi = open('./wf2016/sessionState.txt', 'r')
        sessionState = ofi.read()
        ofi.close()
        return sessionState == 'running'

    def vars_for_template(self):
        if self.subsession.round_number != 1:
            previous_group = self.group.in_round(self.subsession.round_number - 1)
            previous_player = self.player.in_round(self.subsession.round_number - 1)
            lastcontribution_average = float(previous_group.total_contribution)/Constants.players_per_group
            previous_contribution = float(previous_player.contribution)
            previous_payoff = float(previous_player.payoff)
            previous_individualshare = float(previous_group.individual_share)
            return {
                'my_lastcontribution': previous_contribution,
                'lastcontribution_average': lastcontribution_average,
                'individual_share': c(previous_individualshare),
                'individual_payoff': c(previous_payoff),
                'individual_kept': c(previous_payoff - previous_individualshare),
            }

    def before_next_page(self):
        self.player.timed_out = self.timeout_happened


# -------------------------------
class ResultsWaitPage(WaitPage):

    def is_displayed(self):
        ofi = open('./wf2016/sessionState.txt', 'r')
        sessionState = ofi.read()
        ofi.close()
        return sessionState == 'running'

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class FinalResults(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds


#################################
page_sequence = [
    InformationPage,
    MessagePage,
    PlayPage,
    ResultsWaitPage,
    FinalResults
]
