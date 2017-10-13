# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
# </standard imports>

author = 'Your name here'

doc = """
Your app description
"""


# -------------------------------
class Constants(BaseConstants):
    name_in_url = 'wf2016'
    url_aulamaxima = 'http://otree.univ-catholille.fr/room/Aula_Maxima/'
    players_per_group = 3
    num_rounds = 10
    c_advice = ['partenaires_non_cooperatifs',
                'partenaires_cooperatifs']
    # """Amount allocated to each player"""
    endowment = 10
    efficiency_factor = 2


# -------------------------------
class Subsession(BaseSubsession):
    def before_session_starts(self):
        # Set the state of the session. Normal flow = "waiting", "running", "stopped"
        ofi = open("./wf2016/sessionState.txt", "w")
        ofi.write("running")
        ofi.close()
        # Start initialisation of variables
        for g in self.get_groups():
            if self.round_number == 1:
                g.group_advice = Constants.c_advice[random.randint(0, 1)]
            else:
                g.group_advice = g.in_round(self.round_number - 1).group_advice
            g.total_contribution = 0
            g.individual_share = 0
        for p in self.get_players():
            p.timed_out = False


# -------------------------------
class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()
    group_advice = models.CharField(
        choices=(Constants.c_advice[0], Constants.c_advice[1])
    )

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            p.payoff = (Constants.endowment - p.contribution) + self.individual_share


# -------------------------------
class Player(BasePlayer):
    timed_out = models.BooleanField()
    contribution = models.CurrencyField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player"""
    )
