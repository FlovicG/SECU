# -*- coding: utf-8 -*-
from __future__ import division

from . import models
from .models import Constants
from ._builtin import Page, WaitPage


#################################
class GroupingWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.subsession.make_grouping()


#################################
class QuestionsPage(Page):
    form_model = models.Player
    form_fields = ['firstname', 'surname', 'sex', 'school']


    def is_displayed(self):
        return self.player.role() == 'Player'

    def before_next_page(self):
        # Save the data in the dictionary for use in subsequent apps
        self.player.save_data_in_dictionary()


# -------------------------------
class ExperimenterWaitPage(WaitPage):
    pass


#################################
page_sequence = [
    GroupingWaitPage,
    QuestionsPage,
    ExperimenterWaitPage,
]
