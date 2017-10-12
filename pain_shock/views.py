# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants

import csv


#################################
class TestPage(Page):
    form_model = models.Player
    form_fields = ['test']

#################################
class GroupingPage(Page):
    timeout_seconds = 1

    def is_displayed(self):
        return (self.player.participant.label == self.session.config['experimenter_pc'])\
               & ((self.subsession.round_number % len(Constants.c_games)) == 1)

    def before_next_page(self):
        self.subsession.make_grouping()


class GroupingBlockPage(Page):
    def is_displayed(self):
        return (self.player.participant.label != self.session.config['experimenter_pc'])\
               & ((self.subsession.round_number % len(Constants.c_games)) == 1)

    def vars_for_template(self):
        return {
            'this_round_grouping_done': {True: 1, False: 0}[self.subsession.grouping_done]
        }


#################################
class ChoosePlayerPage(Page):
    def is_displayed(self):
        return (self.group.role == 'Playing')\
               & (self.player.role() == 'Experimenter')\
               & ((self.subsession.round_number % len(Constants.c_games)) == 1)

    def vars_for_template(self):
        # Read the possible players from the file
        csv_file = csv.DictReader(open(Constants.c_inputfile, 'r+'), delimiter=',',
                                  fieldnames=['id', 'prenom', 'nom', 'lmh_group', 'int_play'])
        players_matrix = []
        for line in csv_file:
            players_matrix.append([line['id'], line['prenom'], line['nom']])
        return{
            'csv_file': players_matrix
        }


class WaitForChoiceWaitPage(WaitPage):
    def is_displayed(self):
        return (self.group.role == 'Playing')\
               & ((self.subsession.round_number % len(Constants.c_games)) == 1)


#################################
class SetOffer0Page(Page):
    form_model = models.Player
    form_fields = ['offer_0']

    def is_displayed(self):
        return (self.group.role == 'Playing') & (self.player.role() == 'Player')

    def vars_for_template(self):
        # Set the participants variables that are specific to each game
        self.subsession.initialize_variables_foreachgame(theplayer=self.player,
                                                         gamenumber=self.player.participant.vars['game_counter'])
        self.player.participant.vars['game_counter'] += 1
        # Prepare the variables for this page
        ballsbeforedraw = self.player.get_ballsbeforedraw()
        return{
            'ball1colour': ballsbeforedraw[0],
            'ball2colour': ballsbeforedraw[1],
            'ball3colour': ballsbeforedraw[2],
            'ball4colour': ballsbeforedraw[3],
            'ball5colour': ballsbeforedraw[4],
            'ball6colour': ballsbeforedraw[5],
            'ball7colour': ballsbeforedraw[6],
            'ball8colour': ballsbeforedraw[7],
            'ball9colour': ballsbeforedraw[8],
            'ball10colour': ballsbeforedraw[9],
            'enjeu': Constants.c_enjeux[self.player.game_played],
            'offer_0_float_times100': int(100 * self.player.offer_0),
        }


class DrawPrice0Page(Page):
    form_model = models.Player
    form_fields = ['price_0']

    def is_displayed(self):
        return (self.group.role == 'Playing') & (self.player.role() == 'Player')

    def vars_for_template(self):
        ballsbeforedraw = self.player.get_ballsbeforedraw()
        return{
            'ball1colour': ballsbeforedraw[0],
            'ball2colour': ballsbeforedraw[1],
            'ball3colour': ballsbeforedraw[2],
            'ball4colour': ballsbeforedraw[3],
            'ball5colour': ballsbeforedraw[4],
            'ball6colour': ballsbeforedraw[5],
            'ball7colour': ballsbeforedraw[6],
            'ball8colour': ballsbeforedraw[7],
            'ball9colour': ballsbeforedraw[8],
            'ball10colour': ballsbeforedraw[9],
            'enjeu': Constants.c_enjeux[self.player.game_played],
            'offer_0_float_times100': int(100 * self.player.offer_0),
        }

    def before_next_page(self):
        self.player.determine_and_apply_drawing_result()


class DrawBallsPage(Page):
    def is_displayed(self):
        return (self.group.role == 'Playing') & (self.player.role() == 'Player')

    def vars_for_template(self):
        self.player.draw_ball()
        ballsbeforedraw = self.player.get_ballsbeforedraw()
        ballsafterdraw = self.player.get_ballsafterdraw()
        return{
            'ball1colour': ballsbeforedraw[0],
            'ball2colour': ballsbeforedraw[1],
            'ball3colour': ballsbeforedraw[2],
            'ball4colour': ballsbeforedraw[3],
            'ball5colour': ballsbeforedraw[4],
            'ball6colour': ballsbeforedraw[5],
            'ball7colour': ballsbeforedraw[6],
            'ball8colour': ballsbeforedraw[7],
            'ball9colour': ballsbeforedraw[8],
            'ball10colour': ballsbeforedraw[9],
            'ball1aftercolour': ballsafterdraw[0],
            'ball2aftercolour': ballsafterdraw[1],
            'ball3aftercolour': ballsafterdraw[2],
            'ball4aftercolour': ballsafterdraw[3],
            'ball5aftercolour': ballsafterdraw[4],
            'ball6aftercolour': ballsafterdraw[5],
            'ball7aftercolour': ballsafterdraw[6],
            'ball8aftercolour': ballsafterdraw[7],
            'ball9aftercolour': ballsafterdraw[8],
            'ball10aftercolour': ballsafterdraw[9],
            'enjeu': Constants.c_enjeux[self.player.game_played],
            'offer_0_float_times100': int(100 * self.player.offer_0),
            'price_0': self.player.price_0,
            'give_shock': 'yes',  # ???
        }


class EndShockWaitPage(WaitPage):
    def is_displayed(self):
        return self.group.role == 'Playing'


class ShockExperimenterPage(Page):
    def is_displayed(self):
        return (self.group.role == 'Playing') & (self.player.role() == 'Experimenter')

    def vars_for_template(self):
        return{
            'game_played': self.group.get_player_by_role('Player').game_played,
            'offer_0': self.group.get_player_by_role('Player').offer_0,
            'price_0': self.group.get_player_by_role('Player').price_0,
            'balls_before_draw': self.group.get_player_by_role('Player').balls_before_draw,
            'balls_after_draw': self.group.get_player_by_role('Player').balls_after_draw,
            'ball_position_drawn': self.group.get_player_by_role('Player').ball_position_drawn,
            'give_shock': self.group.get_player_by_role('Player').give_shock,
        }


################################
class FinishedWithThisPlayerPage(Page):
    def is_displayed(self):
        return (self.group.role == 'Playing')\
               & (self.player.role() == 'Experimenter') \
               & ((self.subsession.round_number % len(Constants.c_games)) == 0)


################################
class FinishedWithAllPlayers(Page):
    def is_displayed(self):
        nbofplayers = len(self.subsession.get_players()) - 1
        return self.subsession.round_number == nbofplayers * len(Constants.c_games)


#################################
page_sequence = [
    TestPage,
    GroupingPage,
    GroupingBlockPage,
    ChoosePlayerPage,
    WaitForChoiceWaitPage,
    SetOffer0Page,
    DrawPrice0Page,
    DrawBallsPage,
    ShockExperimenterPage,
    EndShockWaitPage,
    FinishedWithThisPlayerPage,
    FinishedWithAllPlayers,
]
