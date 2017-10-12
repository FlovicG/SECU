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


class Constants(BaseConstants):
    name_in_url = 'pain_calib'
    players_per_group = 2
    num_rounds = 2


class Subsession(BaseSubsession):
    def before_session_starts(self):
        pass

    def make_grouping(self):
        # Grouping
        if self.round_number == 1:
            players = self.get_players()
            experimenter = [p for p in players if p.participant.label == self.session.config['experimenter_pc']]
            player = [p for p in players if p.participant.label != self.session.config['experimenter_pc']]
            group_matrix = []
            if not experimenter:
                # Demo
                new_group = [player.pop(), player.pop()]
            else:
                new_group = [experimenter.pop(), player.pop()]
            group_matrix.append(new_group)
            self.set_group_matrix(group_matrix)
        else:
            self.group_like_round(1)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pain_1 = models.PositiveIntegerField()
    pain_2 = models.PositiveIntegerField()
    pain_3 = models.PositiveIntegerField()
    pain_4 = models.PositiveIntegerField()
    pain_5 = models.PositiveIntegerField()
    pain_6 = models.PositiveIntegerField()
    pain_7 = models.PositiveIntegerField()
    pain_8 = models.PositiveIntegerField()
    int_sens = models.FloatField()
    int_pain = models.FloatField()

    def compute_pain_levels(self):
        self.int_sens = 2
        self.int_pain = 7
        with open('pain_file_phase1_out.csv', 'a') as f:
            f.write("{},{},{},{},{},{},{}".format(self.participant.vars['firstname'],
                                                  self.participant.vars['surname'],
                                                  self.participant.vars['sex'],
                                                  self.participant.vars['school'],
                                                  self.int_sens,
                                                  self.int_pain))

    def role(self):
        return {1: 'Experimenter', 2: 'Player'}[self.id_in_group]
