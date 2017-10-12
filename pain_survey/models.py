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

from random import shuffle
import json

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'pain_survey'
    players_per_group = 2
    num_rounds = 1


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
    firstname = models.CharField(initial=None,
                                 verbose_name='Prénom')
    surname = models.CharField(initial=None,
                               verbose_name='Nom')
    sex = models.CharField(initial=None,
                           choices=[('Masculin'), ('Féminin')],
                           verbose_name='Sexe',
                           widget=widgets.RadioSelectHorizontal())
    school = models.CharField(initial=None,
                              verbose_name='Etablissement')


    def save_data_in_dictionary(self):
        self.participant.vars['firstname'] = self.firstname
        self.participant.vars['surname'] = self.surname
        self.participant.vars['sex'] = self.sex
        self.participant.vars['school'] = self.school


    def role(self):
        return {1: 'Experimenter', 2: 'Player'}[self.id_in_group]