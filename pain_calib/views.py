# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


#################################
class GroupingWaitPage(WaitPage):
    def is_displayed(self):
        return self.subsession.round_number == 1

    def after_all_players_arrive(self):
        self.subsession.make_grouping()


#################################
class EnterPainPage(Page):
    form_model = models.Player
    form_fields = ['pain_1', 'pain_2', 'pain_3', 'pain_4',
                   'pain_5', 'pain_6', 'pain_7', 'pain_8']

    def is_displayed(self):
        return self.player.role() == 'Experimenter'


# -------------------------------
class EndPainDeterminationWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.get_player_by_role('Player').compute_pain_levels()


# -------------------------------
class ThankYouPage(Page):
    def is_displayed(self):
        return self.subsession.round_number == 2


#################################
page_sequence = [
    GroupingWaitPage,
    EnterPainPage,
    EndPainDeterminationWaitPage,
    ThankYouPage,
]
