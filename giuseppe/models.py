from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'giuseppe'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    test1 = models.IntegerField()
    test2 = models.IntegerField()
    test3 = models.IntegerField()
    test4 = models.IntegerField()
    test5 = models.IntegerField()
    test6 = models.IntegerField()
