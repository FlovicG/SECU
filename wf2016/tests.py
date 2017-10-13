# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants
from otree.api import Bot, SubmissionMustFail

class PlayerBot(Bot):
    """Bot that plays one round"""

    def play_round(self):
        if self.subsession.round_number == 1:
            assert "Instructions générales" in self.html
            yield (views.InformationPage)
        # if self.subsession.round_number == 6:
        #     yield (views.MessagePage)
        # yield SubmissionMustFail(views.PlayPage, {'contribution': Constants.endowment + 1})
        yield (views.PlayPage, {'contribution': random.randint(0, Constants.endowment)})
        # Don't submit waitpages: yield (views.ResultsWaitPage)
        # Don't put any button in the results page: yield (views.Results)


    def validate_play(self):
        pass
