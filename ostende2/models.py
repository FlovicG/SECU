#################################################
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
#################################################
from otree.db.models import Model, ForeignKey, ManyToManyField
from django.db.models import Q

author = 'Flovic'

doc = """
Your app description
"""


##################################
##################################
class Constants(BaseConstants):
    name_in_url = 'ostende2'
    players_per_group = None
    num_rounds = 2

    c_entites = [
        'ICL - Hors Facultés',
        'Observation - Entreprises et innovation',
        'ESPOL-Lab',
        'ETHICS',
        'C3RD',
        'FGES-Recherche',
        'FLSH-Recherche',
        'FT-Recherche',
        'Laboratoire-2S',
    ]
    c_nb_propositions_per_player = 6
    c_proposition_types = [
        'Vision entité',
        'Quick-Wins entité',
        'Bifurcation entité',
        'Vision ICL',
        'Quick-Wins ICL',
        'Bifurcation ICL',
    ]
    c_min_note = -5
    c_max_note = 5
    c_initial_proposition_text = "Entrez ici votre proposition"
    c_initial_reaction_text = "Entrez ici votre réaction"


class Subsession(BaseSubsession):
    def before_session_starts(self):   # called each round
        if self.round_number == 1:
            # Empty the tables
            Proposition.objects.all().delete()
            Appreciation.objects.all().delete()
            # """For each player, create a fixed number of "proposition stubs""""
            for p in self.get_players():
                p.participant.vars["entite"] = "entite"
                p.generate_proposition_stubs()
            # """For each player, create a fixed number of "appreciation stubs""""
            for p in self.get_players():
                p.generate_appreciation_stubs()

    def compute_average_notes(self):
        for p in self.get_players():
            # Get all propositions for this player
            proposition_qs = Proposition.objects.filter(prop_player_ID_ingroup=p.id_in_group)\
                .filter(Q(type=Constants.c_proposition_types[0])
                        |Q(type=Constants.c_proposition_types[1])
                        |Q(type=Constants.c_proposition_types[2]))\
                .prefetch_related('appreciation_set')
            assert len(proposition_qs) == Constants.c_nb_propositions_per_player / 2
            # Compute the average note for each proposition
            for prop in proposition_qs:
                all_app_notes_list = [app.note for app in prop.appreciation_set.all()]
                prop.average_note = sum(all_app_notes_list)/len(all_app_notes_list)
                prop.save()
            # Compute the average note for the player
            all_prop_notes_list = [prop.average_note for prop in proposition_qs]
            p.participant.vars['average_note'] = sum(all_prop_notes_list)/len(all_prop_notes_list)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    entite = models.CharField(initial=Constants.c_entites[0],
                              choices=Constants.c_entites,
                              widget=widgets.RadioSelect())
    average_note = models.FloatField(min=Constants.c_min_note, max=Constants.c_max_note, initial=0)

    def generate_proposition_stubs(self):
        # Create a fixed number of "proposition stubs"
        for i in range(Constants.c_nb_propositions_per_player):
            proposition = self.proposition_set.create()    # create a new Proposition object as part of the player's decision set
            proposition.prop_player_ID_ingroup = self.id_in_group
            proposition.type = Constants.c_proposition_types[i]
            proposition.text = "Prop-" + proposition.type + "-" + str(self.id_in_group)
            proposition.save()     # important: save to DB!

    def generate_appreciation_stubs(self):
        # Get all propositions that don't belong to that player
        proposition_qs = Proposition.objects.exclude(player=self.pk)
        for prop in proposition_qs:
            appreciation = self.appreciation_set.create()
            appreciation.player = self
            appreciation.app_player_ID_ingroup = self.id_in_group
            appreciation.proposition = prop
            appreciation.note = 0
            appreciation.reaction = " "
            appreciation.related_version = 999
            appreciation.up_to_date = False
            appreciation.save()     # important: save to DB!


#################################################
# Additional classes for specific data
#################################################
class Proposition(Model):   # our custom model inherits from Django's base class "Model"
    player = ForeignKey(Player, null=True, blank=True)         # creates 1:m relation -> this proposition was made by a certain player
    prop_player_ID_ingroup = models.IntegerField()

    text = models.CharField(verbose_name="")
    type = models.CharField(choices=Constants.c_proposition_types)
    version = models.PositiveIntegerField(initial=0)
    average_note = models.FloatField(min=Constants.c_min_note, max=Constants.c_max_note, initial=0)

    def __str__(self):
        return "Proposition {type}: {text}".format(
            type=self.type, text=self.text)


class Appreciation(Model):   # our custom model inherits from Django's base class "Model"
    player = ForeignKey(Player, null=True, blank=True)  # creates 1:m relation -> this appreciation was made by a certain player
    proposition = ForeignKey(Proposition, null=True, blank=True)  # creates 1:m relation -> this appreciation is related to a certain proposition
    app_player_ID_ingroup = models.IntegerField()

    note = models.IntegerField(min=Constants.c_min_note, max=Constants.c_max_note)
    reaction = models.CharField()
    related_version = models.PositiveIntegerField(initial=999)
    up_to_date = models.BooleanField(initial=False)

    def __str__(self):
        return "Appreciation n°{id}: {reaction}".format(
            id=self.pk, reaction=self.reaction)
