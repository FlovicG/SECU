# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants

import random

#--------------------------------------
class InformationsGenerales(Page):
    timeout_seconds = random.randint(5,15)  #???DEBUG


#--------------------------------------
class Entite(Page):
    timeout_seconds = random.randint(5,15)  #???DEBUG
    timeout_submission = {'my_entity': Constants.c_entity[random.randint(0,8)]} #???DEBUG
    form_model = models.Player
    form_fields = ['my_entity']

    def vars_for_template(self):
        try:
            self.player.my_entity = Constants.c_participantlabel_entity[self.player.participant.label]
        except KeyError:
            pass
        return {
        'entity': self.player.my_entity,
        }


#--------------------------------------
class GrandesMasses1(Page):
    timeout_seconds = random.randint(5,15)  #???DEBUG
    timeout_submission = {'nb_mcf1': random.randint(0,10)} #???DEBUG
    form_model = models.Player
    form_fields = ['nb_mcf1']

class GrandesMasses1ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.compute_group_grandes_masses_results1()

class GrandesMasses2(Page):
    timeout_seconds = random.randint(5,15)  #???DEBUG
    timeout_submission = {'nb_mcf2': random.randint(0,10)} #???DEBUG
    form_model = models.Player
    form_fields = ['nb_mcf2']
    def is_displayed(self):
        return self.group.nb_mcf_total>10

class GrandesMasses2ResultsWaitPage(WaitPage):
    def is_displayed(self):
        return self.group.nb_mcf_total>10
    def after_all_players_arrive(self):
        self.group.compute_group_grandes_masses_results2()

class GrandesMasses3(Page):
    timeout_seconds = random.randint(5,15)  #???DEBUG
    timeout_submission = {'nb_mcf3': random.randint(0,10)} #???DEBUG
    form_model = models.Player
    form_fields = ['nb_mcf3']
    def is_displayed(self):
        return self.group.nb_mcf_total>10

class GrandesMasses3ResultsWaitPage(WaitPage):
    def is_displayed(self):
        return self.group.nb_mcf_total>10
    def after_all_players_arrive(self):
        self.group.compute_group_grandes_masses_results3()

class GrandesMassesResults(Page):
    timeout_seconds = random.randint(5,15)  #???DEBUG


#--------------------------------------
class MasseSalariale(Page):
    timeout_seconds = random.randint(5,15)  #???DEBUG
    timeout_submission = {'salaire_moyen': Constants.c_salairemoyen_nbmcf[random.randint(0,8)][0],
                          'nb_mcf_avec_salaire_moyen': Constants.c_salairemoyen_nbmcf[random.randint(0,8)][1]} #???DEBUG
    form_model = models.Player
    form_fields = ['salaire_moyen', 'nb_mcf_avec_salaire_moyen']

    def vars_for_template(self):
        data_to_be_plotted = Constants.c_salairemoyen_nbmcf
        return {
        'dataToBePlotted': data_to_be_plotted,
        }

class MasseSalarialeResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.compute_group_masse_salariale_results()

class MasseSalarialeResults(Page):
    timeout_seconds = random.randint(5,15)  #???DEBUG


#--------------------------------------
class CroissanceIntExt(Page):
    timeout_seconds = random.randint(5,15)  #???DEBUG
    timeout_submission = {'hff': Constants.c_hff_cout[random.randint(0,6)][0],
                          'cout_vacation_avec_hff': Constants.c_hff_cout[random.randint(0,6)][1]} #???DEBUG
    form_model = models.Player
    form_fields = ['hff', 'cout_vacation_avec_hff']

    def vars_for_template(self):
        data_to_be_plotted = Constants.c_hff_cout
        return {
        'dataToBePlotted': data_to_be_plotted,
        }#

class CroissanceIntExtResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.compute_group_croissance_intext_results()

class CroissanceIntExtResults(Page):
    timeout_seconds = random.randint(5,15)  #???DEBUG


#-------------------------------------
class GlobalResultsPerEntity(Page):
    timeout_seconds = random.randint(5,15)  #???DEBUG
    timeout_submission = {'recettes': '1|2|3|4',
                          'commentaires': 'mes commentaires'} #???DEBUG
    form_model = models.Player
    form_fields = ['recettes', 'commentaires']

    def vars_for_template(self):
        self.player.cout_total = self.player.nb_mcffinal * (self.player.salaire_moyen + self.player.cout_vacation_avec_hff)


class GlobalResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.compute_group_masse_salariale_results()
        self.group.compute_group_croissance_intext_results()


class GlobalResults(Page):
    pass


#-------------------------------------
class MerciPage(Page):
    pass


#--------------------------------------
page_sequence = [
    InformationsGenerales,
    Entite,
    GrandesMasses1,
    GrandesMasses1ResultsWaitPage,
    GrandesMasses2,
    GrandesMasses2ResultsWaitPage,
    GrandesMasses3,
    GrandesMasses3ResultsWaitPage,
    GrandesMassesResults,
    MasseSalariale,
    CroissanceIntExt,
    GlobalResultsPerEntity,
    GlobalResultsWaitPage,
    GlobalResults,
    MerciPage
]
