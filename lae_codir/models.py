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

author = 'Nicolas & Flovic'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'lae_codir'
    players_per_group = None
    num_rounds = 1

    c_entity = ['FMM-SanteSocial', 'FT', 'FGES', 'FLSH', 'FD', 'Espol', 'Anthropo-Lab']
    c_participantlabel_entity = {'PC_1': c_entity[0],
                                 'PC_2': c_entity[1],
                                 'PC_3': c_entity[2],
                                 'PC_4': c_entity[3],
                                 'PC_7': c_entity[4],
                                 'PC_8': c_entity[5],
                                 'PC_9': c_entity[6],
                                 'PC_14': c_entity[0],
                                 'PC_15': c_entity[1],
                                 'PC_16': c_entity[2],
                                 'PC_12': c_entity[3],
                                 'PC_13': c_entity[4],
                                 'PC_11': c_entity[5],
                                 'PC_6': c_entity[6]}
    c_salairemoyen_nbmcf = [[46800,10], [52000,9], [58500,8], [66857,7], [78000,6],
                           [93600,5], [117000,4], [156000,3], [234000,2], [468000,1]]
    c_hff_cout = [[240,0], [200,30000], [160,60000], [120,90000], [80,120000],
                           [40,150000], [0,180000]]


class Subsession(BaseSubsession):
    def before_session_starts(self):
        #---------------------
        #  Initialise variables
        for g in self.get_groups():
            # Data pour phase 1
            g.nb_mcf_fmm = 0
            g.nb_mcf_ft = 0
            g.nb_mcf_fges = 0
            g.nb_mcf_flsh = 0
            g.nb_mcf_fd = 0
            g.nb_mcf_espol = 0
            g.nb_mcf_santesocial = 0
            g.nb_mcf_commonhome = 0
            g.nb_mcf_anthropolab = 0
            g.nb_mcf_total = 0
            # Data pour phase 2
            g.salaire_moyen_icl = 0
            g.nb_mcf_avec_salaire_moyen_icl = 0
            g.salaire_moyen_fmm = 0
            g.salaire_moyen_ft = 0
            g.salaire_moyen_fges = 0
            g.salaire_moyen_flsh = 0
            g.salaire_moyen_fd = 0
            g.salaire_moyen_espol = 0
            g.salaire_moyen_santesocial = 0
            g.salaire_moyen_commonhome = 0
            g.salaire_moyen_anthropolab = 0
            g.nb_mcf_avec_salaire_moyen_fmm = 0
            g.nb_mcf_avec_salaire_moyen_ft = 0
            g.nb_mcf_avec_salaire_moyen_fges = 0
            g.nb_mcf_avec_salaire_moyen_flsh = 0
            g.nb_mcf_avec_salaire_moyen_fd = 0
            g.nb_mcf_avec_salaire_moyen_espol = 0
            g.nb_mcf_avec_salaire_moyen_santesocial = 0
            g.nb_mcf_avec_salaire_moyen_commonhome = 0
            g.nb_mcf_avec_salaire_moyen_anthropolab = 0
            g.salaire_moyen_icl = 0
            g.nb_mcf_avec_salaire_moyen_icl = 0
            # Data pour phase 3
            g.hff_fmm = 0
            g.hff_ft = 0
            g.hff_fges = 0
            g.hff_flsh = 0
            g.hff_fd = 0
            g.hff_espol = 0
            g.hff_santesocial = 0
            g.hff_commonhome = 0
            g.hff_anthropolab = 0
            g.cout_vacation_avec_hff_fmm = 0
            g.cout_vacation_avec_hff_ft = 0
            g.cout_vacation_avec_hff_fges = 0
            g.cout_vacation_avec_hff_flsh = 0
            g.cout_vacation_avec_hff_fd = 0
            g.cout_vacation_avec_hff_espol = 0
            g.cout_vacation_avec_hff_santesocial = 0
            g.cout_vacation_avec_hff_commonhome = 0
            g.cout_vacation_avec_hff_anthropolab = 0
            g.hff_moyen_icl = 0
            g.cout_vacation_avec_hff_moyen_icl = 0
            g.recettes_icl = ''
            g.commentaires_icl = ''
        for p in self.get_players():
            p.participant.label = "initialValue"
            p.my_entity = ''
            p.nb_mcf1 = 0
            p.nb_mcf2 = 0
            p.nb_mcf3 = 0
            p.nb_mcffinal = 0
            p.salaire_moyen = 0
            p.nb_mcf_avec_salaire_moyen = 0
            p.hff = 240
            p.cout_vacation_avec_hff = 0
            p.cout_total = 0
            p.recettes = ''
            p.commentaires = ''


class Group(BaseGroup):
    # Data pour phase 1
    nb_mcf_fmm = models.IntegerField(min=0, max=10)
    nb_mcf_ft = models.IntegerField(min=0, max=10)
    nb_mcf_fges = models.IntegerField(min=0, max=10)
    nb_mcf_flsh = models.IntegerField(min=0, max=10)
    nb_mcf_fd = models.IntegerField(min=0, max=10)
    nb_mcf_espol = models.IntegerField(min=0, max=10)
    nb_mcf_santesocial = models.IntegerField(min=0, max=10)
    nb_mcf_commonhome = models.IntegerField(min=0, max=10)
    nb_mcf_anthropolab = models.IntegerField(min=0, max=10)
    # Data agrégées
    nb_mcf_total = models.IntegerField(min=0)

    # Data pour phase 2
    salaire_moyen_fmm = models.IntegerField(min=0)
    salaire_moyen_ft = models.IntegerField(min=0)
    salaire_moyen_fges = models.IntegerField(min=0)
    salaire_moyen_flsh = models.IntegerField(min=0)
    salaire_moyen_fd = models.IntegerField(min=0)
    salaire_moyen_espol = models.IntegerField(min=0)
    salaire_moyen_santesocial = models.IntegerField(min=0)
    salaire_moyen_commonhome = models.IntegerField(min=0)
    salaire_moyen_anthropolab = models.IntegerField(min=0)
    nb_mcf_avec_salaire_moyen_fmm = models.IntegerField(min=0)
    nb_mcf_avec_salaire_moyen_ft = models.IntegerField(min=0)
    nb_mcf_avec_salaire_moyen_fges = models.IntegerField(min=0)
    nb_mcf_avec_salaire_moyen_flsh = models.IntegerField(min=0)
    nb_mcf_avec_salaire_moyen_fd = models.IntegerField(min=0)
    nb_mcf_avec_salaire_moyen_espol = models.IntegerField(min=0)
    nb_mcf_avec_salaire_moyen_santesocial = models.IntegerField(min=0)
    nb_mcf_avec_salaire_moyen_commonhome = models.IntegerField(min=0)
    nb_mcf_avec_salaire_moyen_anthropolab = models.IntegerField(min=0)
    # Data agrégées
    salaire_moyen_icl = models.IntegerField(min=0)
    nb_mcf_avec_salaire_moyen_icl = models.IntegerField(min=0)

    # Data pour phase 3
    hff_fmm = models.IntegerField(min=0, max=240)
    hff_ft = models.IntegerField(min=0, max=240)
    hff_fges = models.IntegerField(min=0, max=240)
    hff_flsh = models.IntegerField(min=0, max=240)
    hff_fd = models.IntegerField(min=0, max=240)
    hff_espol = models.IntegerField(min=0, max=240)
    hff_santesocial = models.IntegerField(min=0, max=240)
    hff_commonhome = models.IntegerField(min=0, max=240)
    hff_anthropolab = models.IntegerField(min=0, max=240)
    cout_vacation_avec_hff_fmm = models.IntegerField(min=0, max=180000)
    cout_vacation_avec_hff_ft = models.IntegerField(min=0, max=180000)
    cout_vacation_avec_hff_fges = models.IntegerField(min=0, max=180000)
    cout_vacation_avec_hff_flsh = models.IntegerField(min=0, max=180000)
    cout_vacation_avec_hff_fd = models.IntegerField(min=0, max=180000)
    cout_vacation_avec_hff_espol = models.IntegerField(min=0, max=180000)
    cout_vacation_avec_hff_santesocial = models.IntegerField(min=0, max=180000)
    cout_vacation_avec_hff_commonhome = models.IntegerField(min=0, max=180000)
    cout_vacation_avec_hff_anthropolab = models.IntegerField(min=0, max=180000)
    # Data agrégées
    hff_moyen_icl = models.IntegerField(min=0, max=240)
    cout_vacation_avec_hff_moyen_icl = models.IntegerField(min=0, max=180000)

    # Data recettes
    recettes_icl = models.TextField()
    commentaires_icl = models.TextField()

    def compute_group_grandes_masses_results1(self):
        self.nb_mcf_total = 0
        for p in self.get_players():
            p.nb_mcffinal = p.nb_mcf1
            self.nb_mcf_total += p.nb_mcf1
            if p.my_entity == 'FMM-SanteSocial': self.nb_mcf_fmm = p.nb_mcf1
            elif p.my_entity == 'FT': self.nb_mcf_ft = p.nb_mcf1
            elif p.my_entity == 'FGES': self.nb_mcf_fges = p.nb_mcf1
            elif p.my_entity == 'FLSH': self.nb_mcf_flsh = p.nb_mcf1
            elif p.my_entity == 'FD': self.nb_mcf_fd = p.nb_mcf1
            elif p.my_entity == 'Espol': self.nb_mcf_espol = p.nb_mcf1
            elif p.my_entity == 'Sante-Social': self.nb_mcf_santesocial = p.nb_mcf1
            elif p.my_entity == 'Common-Home': self.nb_mcf_commonhome = p.nb_mcf1
            elif p.my_entity == 'Anthropo-Lab': self.nb_mcf_anthropolab = p.nb_mcf1

    def compute_group_grandes_masses_results2(self):
        self.nb_mcf_total = 0
        for p in self.get_players():
            p.nb_mcffinal = p.nb_mcf2
            self.nb_mcf_total += p.nb_mcf2
            if p.my_entity == 'FMM-SanteSocial': self.nb_mcf_fmm = p.nb_mcf2
            elif p.my_entity == 'FT': self.nb_mcf_ft = p.nb_mcf2
            elif p.my_entity == 'FGES': self.nb_mcf_fges = p.nb_mcf2
            elif p.my_entity == 'FLSH': self.nb_mcf_flsh = p.nb_mcf2
            elif p.my_entity == 'FD': self.nb_mcf_fd = p.nb_mcf2
            elif p.my_entity == 'Espol': self.nb_mcf_espol = p.nb_mcf2
            elif p.my_entity == 'Sante-Social': self.nb_mcf_santesocial = p.nb_mcf2
            elif p.my_entity == 'Common-Home': self.nb_mcf_commonhome = p.nb_mcf2
            elif p.my_entity == 'Anthropo-Lab': self.nb_mcf_anthropolab = p.nb_mcf2

    def compute_group_grandes_masses_results3(self):
        self.nb_mcf_total = 0
        for p in self.get_players():
            p.nb_mcffinal = p.nb_mcf3
            self.nb_mcf_total += p.nb_mcf3
            if p.my_entity == 'FMM-SanteSocial': self.nb_mcf_fmm = p.nb_mcf3
            elif p.my_entity == 'FT': self.nb_mcf_ft = p.nb_mcf3
            elif p.my_entity == 'FGES': self.nb_mcf_fges = p.nb_mcf3
            elif p.my_entity == 'FLSH': self.nb_mcf_flsh = p.nb_mcf3
            elif p.my_entity == 'FD': self.nb_mcf_fd = p.nb_mcf3
            elif p.my_entity == 'Espol': self.nb_mcf_espol = p.nb_mcf3
            elif p.my_entity == 'Sante-Social': self.nb_mcf_santesocial = p.nb_mcf3
            elif p.my_entity == 'Common-Home': self.nb_mcf_commonhome = p.nb_mcf3
            elif p.my_entity == 'Anthropo-Lab': self.nb_mcf_anthropolab = p.nb_mcf3

    def compute_group_masse_salariale_results(self):
        # Compute le salaire moyen
        self.salaire_moyen_icl = 0
        self.nb_mcf_avec_salaire_moyen_icl = 0
        for p in self.get_players():
            self.salaire_moyen_icl += p.salaire_moyen
            self.nb_mcf_avec_salaire_moyen_icl += p.nb_mcf_avec_salaire_moyen
            if p.my_entity == 'FMM-SanteSocial':
                self.salaire_moyen_fmm = p.salaire_moyen
                self.nb_mcf_avec_salaire_moyen_fmm = p.nb_mcf_avec_salaire_moyen
            elif p.my_entity == 'FT':
                self.salaire_moyen_ft = p.salaire_moyen
                self.nb_mcf_avec_salaire_moyen_ft = p.nb_mcf_avec_salaire_moyen
            elif p.my_entity == 'FGES':
                self.salaire_moyen_fges = p.salaire_moyen
                self.nb_mcf_avec_salaire_moyen_fges = p.nb_mcf_avec_salaire_moyen
            elif p.my_entity == 'FLSH':
                self.salaire_moyen_flsh = p.salaire_moyen
                self.nb_mcf_avec_salaire_moyen_flsh = p.nb_mcf_avec_salaire_moyen
            elif p.my_entity == 'FD':
                self.salaire_moyen_fd = p.salaire_moyen
                self.nb_mcf_avec_salaire_moyen_fd = p.nb_mcf_avec_salaire_moyen
            elif p.my_entity == 'Espol':
                self.salaire_moyen_espol = p.salaire_moyen
                self.nb_mcf_avec_salaire_moyen_espol = p.nb_mcf_avec_salaire_moyen
            elif p.my_entity == 'Sante-Social':
                self.salaire_moyen_santesocial = p.salaire_moyen
                self.nb_mcf_avec_salaire_moyen_santesocial = p.nb_mcf_avec_salaire_moyen
            elif p.my_entity == 'Common-Home':
                self.salaire_moyen_commonhome = p.salaire_moyen
                self.nb_mcf_avec_salaire_moyen_commonhome = p.nb_mcf_avec_salaire_moyen
            elif p.my_entity == 'Anthropo-Lab':
                self.salaire_moyen_anthropolab = p.salaire_moyen
                self.nb_mcf_avec_salaire_moyen_anthropolab = p.nb_mcf_avec_salaire_moyen
        # Terminer les moyennes
        self.salaire_moyen_icl /= len(self.get_players())
        self.nb_mcf_avec_salaire_moyen_icl /= len(self.get_players())

    def compute_group_croissance_intext_results(self):
        # Compute la décharge moyenne
        self.hff_moyen_icl = 0
        self.cout_vacation_avec_hff_moyen_icl = 0
        for p in self.get_players():
            self.hff_moyen_icl += p.hff
            self.cout_vacation_avec_hff_moyen_icl += p.cout_vacation_avec_hff
            if p.my_entity == 'FMM-SanteSocial':
                self.hff_fmm = p.hff
                self.cout_vacation_avec_hff_fmm = p.cout_vacation_avec_hff
            elif p.my_entity == 'FT':
                self.hff_ft = p.hff
                self.cout_vacation_avec_hff_ft = p.cout_vacation_avec_hff
            elif p.my_entity == 'FGES':
                self.hff_fges = p.hff
                self.cout_vacation_avec_hff_fges = p.cout_vacation_avec_hff
            elif p.my_entity == 'FLSH':
                self.hff_flsh = p.hff
                self.cout_vacation_avec_hff_flsh = p.cout_vacation_avec_hff
            elif p.my_entity == 'FD':
                self.hff_fd = p.hff
                self.cout_vacation_avec_hff_fd = p.cout_vacation_avec_hff
            elif p.my_entity == 'Espol':
                self.hff_espol = p.hff
                self.cout_vacation_avec_hff_espol = p.cout_vacation_avec_hff
            elif p.my_entity == 'Sante-Social':
                self.hff_santesocial = p.hff
                self.cout_vacation_avec_hff_santesocial = p.cout_vacation_avec_hff
            elif p.my_entity == 'Common-Home':
                self.hff_commonhome = p.hff
                self.cout_vacation_avec_hff_commonhome = p.cout_vacation_avec_hff
            elif p.my_entity == 'Anthropo-Lab':
                self.hff_anthropolab = p.hff
                self.cout_vacation_avec_hff_anthropolab = p.cout_vacation_avec_hff
        # Terminer les moyennes
        self.hff_moyen_icl /= len(self.get_players())
        self.cout_vacation_avec_hff_moyen_icl /= len(self.get_players())

    def compute_group_recettes_results(self):
        self.recettes_icl = ''
        self.commentaires_icl = ''
        for p in self.get_players():
            self.recettes_icl += "\n**********************\n" + p.my_entity + "\n**********************\n" + p.recettes + "\n"
            self.commentaires_icl += "\n**********************\n" + p.my_entity + "\n**********************\n" + p.commentaires + "\n"


class Player(BasePlayer):
    my_entity = models.CharField(
        choices=Constants.c_entity,
        verbose_name="De quelle entité avez-vous la responsabilité?",
        widget=widgets.RadioSelect()
    )
    # Phase 1
    nb_mcf1 = models.IntegerField(min=0, max=10)
    nb_mcf2 = models.IntegerField(min=0, max=10)
    nb_mcf3 = models.IntegerField(min=0, max=10)
    nb_mcffinal = models.IntegerField(min=0, max=10)
    # Phase 2
    salaire_moyen = models.IntegerField(min=0)
    nb_mcf_avec_salaire_moyen = models.IntegerField(min=0)
    # Phase 3
    hff = models.IntegerField(min=0, max=240)
    cout_vacation_avec_hff = models.IntegerField(min=0, max=180000)
    # GlobalResults
    cout_total = models.IntegerField(min=0)
    recettes = models.TextField(verbose_name="Quelle(s) source(s) de financement imaginez-vous?")
    commentaires = models.TextField(blank=True, verbose_name="Commentaires libres:")