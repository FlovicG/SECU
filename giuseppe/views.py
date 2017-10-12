from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, Player
from django import forms


class MyPage(Page):
    form_model = models.Player

    def get_form_fields(self):
        if self.player.id_in_group % 2 == 0:
            return ['test1', 'test2', 'test3', 'test4', 'test5', 'test6']
        else:
            return ['test6', 'test5', 'test4', 'test3', 'test2', 'test1']


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    MyPage,
    ResultsWaitPage,
    Results
]
