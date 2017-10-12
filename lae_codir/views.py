# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


#--------------------------------------
class InformationsGenerales(Page):
    pass


#--------------------------------------
class Entite(Page):
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
    form_model = models.Player
    form_fields = ['nb_mcf1']

class GrandesMasses1ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.compute_group_grandes_masses_results1()

class GrandesMasses2(Page):
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
    pass


#--------------------------------------
class MasseSalariale(Page):
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
    pass


#--------------------------------------
class CroissanceIntExt(Page):
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
    pass


#-------------------------------------
class GlobalResultsPerEntity(Page):
    form_model = models.Player
    form_fields = ['recettes', 'commentaires']

    def vars_for_template(self):
        self.player.cout_total = self.player.nb_mcffinal * (self.player.salaire_moyen + self.player.cout_vacation_avec_hff)


class GlobalResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.compute_group_masse_salariale_results()
        self.group.compute_group_croissance_intext_results()
        self.group.compute_group_recettes_results()


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
