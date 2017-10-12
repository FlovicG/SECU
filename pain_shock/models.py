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
    name_in_url = 'pain_shock'
    players_per_group = None
    num_rounds = 30  # Maximum number of rounds, but the experiment will be stopped before

    c_games = ['1ball', '2balls', 'Minus5Shocks', 'Minus10Shocks']
    c_enjeux = {'1ball': "Echanger 1 boule rouge",
                '2balls': "Echanger 2 boules rouges",
                'Minus5Shocks': "Diminuer de 5 décharges",
                'Minus10Shocks': "Diminuer de 10 décharges",
                }
    c_number_of_balls = 10
    c_ball_colors = ['blanche', 'rouge']
    c_groups = ['L', 'M', 'H']
    c_inputfile = "./pain_file_phase2_input.csv"


class Subsession(BaseSubsession):
    grouping_done = models.BooleanField(initial=False)

    def before_session_starts(self):
        pass

    def vars_for_admin_report(self):
        payoffs = sorted([p.payoff for p in self.get_players()])
        return {'payoffs': payoffs}

    def make_grouping(self):
        # Grouping
        allplayers = self.get_players()
        print(allplayers)  # ???
        experimenters = [p for p in allplayers if p.participant.label == self.session.config['experimenter_pc']]
        players = [p for p in allplayers if p.participant.label != self.session.config['experimenter_pc']]
        print("Experimenters: ", experimenters)  # ???
        print("Players: ", players)  # ???
        group_matrix = []
        if not experimenters:
            print("Inside not experimenters")  # ???
            # Demo: Choose arbitrarely the first player to be the experimenter
            experimenter = players.pop()
            # Create the "playing" group
            playing_group = [experimenter, players.pop(self.round_number)]
            # Put all the other players in a "waiting group"
            waiting_group = [players.pop()]
            for p in players:
                waiting_group.append(p)
            group_matrix.append(playing_group)
            group_matrix.append(waiting_group)
        else:
            print("Inside Experimenters")  # ???
            # Real XP
            # Save the experimenter
            experimenter = experimenters.pop()
            # Create the "playing" group
            playing_group = [experimenter, players.pop(int(self.round_number/len(Constants.c_games)))]
            # Put all the other players in a "waiting group"
            waiting_group = [players.pop()]
            for p in players:
                waiting_group.append(p)
            group_matrix.append(playing_group)
            group_matrix.append(waiting_group)
        print(group_matrix)  # ???
        self.set_group_matrix(group_matrix)
        self.grouping_done = True
        # Assign the group variables
        done = False
        for g in self.get_groups():
            if not done:
                g.role = 'Playing'
                done = True
            else:
                g.role = 'Waiting'
        # Initialize the player variables
        self.initialize_variables_forallgames()

    def initialize_variables_forallgames(self):
        # Inside the playing group, initialize the variables
        for g in self.get_groups():
            if g.role == 'Playing':
                # Set the player variables (the experimenter has no variable to be set)
                theplayer = g.get_player_by_role('Player')
                # Set the participants variables that will be constants for all 4 games
                theplayer.participant.vars['game_counter'] = 0
                theplayer.participant.vars['games_order'] = Constants.c_games
                shuffle(theplayer.participant.vars['games_order'])
                theplayer.participant.vars['intensity_group'] = random.choice(Constants.c_groups)  # ??? Get from file
                theplayer.intensity_group = theplayer.participant.vars['intensity_group']
                if theplayer.participant.vars['intensity_group'] == 'H':
                    theplayer.participant.vars['balls_before_draw'] = ['rouge', 'rouge', 'rouge', 'rouge',
                                                                       'rouge', 'rouge', 'rouge', 'blanche',
                                                                       'blanche', 'blanche']
                elif theplayer.participant.vars['intensity_group'] == 'M':
                    theplayer.participant.vars['balls_before_draw'] = ['rouge', 'rouge', 'rouge', 'rouge',
                                                                       'rouge', 'blanche', 'blanche', 'blanche',
                                                                       'blanche', 'blanche']
                elif theplayer.participant.vars['intensity_group'] == 'L':
                    theplayer.participant.vars['balls_before_draw'] = ['rouge', 'rouge', 'rouge', 'blanche',
                                                                       'blanche', 'blanche', 'blanche', 'blanche',
                                                                       'blanche', 'blanche']
                else:
                    raise Exception('Unknown intensity_group')

    def initialize_variables_foreachgame(self, theplayer, gamenumber):
        # Set the participants variables that are specific to each game
        theplayer.game_played = theplayer.participant.vars['games_order'][gamenumber]
        temp = theplayer.participant.vars['balls_before_draw']
        shuffle(temp)
        theplayer.set_ballsbeforedraw(temp)
        theplayer.set_ballsafterdraw(temp)
        theplayer.offer_0 = c(0)
        theplayer.won_offer_price = False


class Group(BaseGroup):
    role = models.CharField(choices=['Playing', 'Waiting'])


class Player(BasePlayer):
    test = models.CharField(choices=["test1", "test2", "test3"])
    intensity_group = models.CharField(choices=Constants.c_groups)
    balls_before_draw = models.CharField()
    balls_after_draw = models.CharField()
    ball_position_drawn = models.IntegerField()
    game_played = models.CharField(choices=Constants.c_games)
    offer_0 = models.FloatField()
    price_0 = models.FloatField()
    won_offer_price = models.BooleanField()
    give_shock = models.IntegerField(choices=[0, 1])

    def set_ballsbeforedraw(self, x):
        self.balls_before_draw = json.dumps(x)

    def get_ballsbeforedraw(self):
        return json.loads(self.balls_before_draw)

    def set_ballsafterdraw(self, x):
        self.balls_after_draw = json.dumps(x)

    def get_ballsafterdraw(self):
        return json.loads(self.balls_after_draw)

    def determine_and_apply_drawing_result(self):
        if self.price_0 > self.offer_0:
            self.won_offer_price = False
        else:
            self.won_offer_price = True
        if self.won_offer_price:
            if self.game_played == '1ball':
                # '1ball': Exchange 1 red ball
                temp = self.get_ballsafterdraw()
                temp[temp.index(Constants.c_ball_colors[1])] = Constants.c_ball_colors[0]
                self.set_ballsafterdraw(temp)
            elif self.game_played == '2balls':
                # '2balls': Exchange 2 red balls
                temp = self.get_ballsafterdraw()
                temp[temp.index(Constants.c_ball_colors[1])] = Constants.c_ball_colors[0]
                temp[temp.index(Constants.c_ball_colors[1])] = Constants.c_ball_colors[0]
                self.set_ballsafterdraw(temp)

    def draw_ball(self):
        self.ball_position_drawn = random.randint(1, Constants.c_number_of_balls)
        temp = self.get_ballsafterdraw()
        print("temp:", temp)
        print("temp[self.ball_position_drawn - 1]:", temp[2])
        print("self.ball_position_drawn:", self.ball_position_drawn)
        print("Constants.c_ball_colors[1]", Constants.c_ball_colors[1])
        if temp[self.ball_position_drawn] == Constants.c_ball_colors[1]:
            self.give_shock = 1
        else:
            self.give_shock = 0
        print("self.give_shock:", self.give_shock)

    def role(self):
        if self.id_in_group == 1:
            return 'Experimenter'
        else:
            return 'Player'
