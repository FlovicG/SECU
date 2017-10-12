#################################################
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
#################################################
from otree.db.models import Model, ForeignKey, ManyToManyField
from datetime import datetime, timedelta
from django.utils import timezone
import threading
from collections import OrderedDict
from channels import Group as channelsGroup
import json

author = 'Flovic'

doc = """
Your app description
"""


##################################
##################################
class UpdateData:
    def __init__(self, tempo, target, args=[], kwargs={}):
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._tempo = tempo

    def _run(self):
        self._timer = threading.Timer(self._tempo, self._run)
        self._timer.start()
        self._target(*self._args, **self._kwargs)

    def start(self):
        self._timer = threading.Timer(self._tempo, self._run)
        self._timer.start()

    def stop(self):
        self._timer.cancel()


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).seconds)):
        yield start_date + timedelta(seconds=n*Constants.c_refresh_to_clients_insec)


def sendUpdatedData(**kwargs):
    def create_odict_from_object(obj, fieldnames):
        data = OrderedDict()
        for f in fieldnames:
            data[f] = getattr(obj, f)
        return data

    groups_qs = Group.objects.filter(session_id = kwargs["session_id"],
                                     subsession_id = kwargs["subsession_id"],
                                     round_number = kwargs["round_number"])

    starting_datetime = timezone.make_aware(kwargs["starting_time"], timezone.get_default_timezone())
    current_datetime = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
    for single_date in date_range(starting_datetime, current_datetime):
        print("single_date: ", single_date)

    for group in groups_qs:
        # Build the data
        dict_for_group = {}
        for p in group.get_players():
            new_key = "data_player_" + str(p.id_in_group)
            dict_for_group[new_key] = []
            transitivedecisions_for_thisplayer = list(p.transitivedecision_set.order_by('-timestamp'))
            if len(transitivedecisions_for_thisplayer) == 0:
                for _ in date_range(starting_datetime, current_datetime):
                    dict_for_group[new_key].append(Constants.c_initial_nbETP)
            elif len(transitivedecisions_for_thisplayer) == 1:
                only_trans_dec = transitivedecisions_for_thisplayer.pop()
                for single_date in date_range(starting_datetime, current_datetime):
                    if single_date < only_trans_dec.timestamp :
                        dict_for_group[new_key].append(Constants.c_initial_nbETP)
                    else:
                        dict_for_group[new_key].append(only_trans_dec.nb_ETP)
            else:
                previous_trans_dec = transitivedecisions_for_thisplayer.pop()
                next_trans_dec = transitivedecisions_for_thisplayer.pop()
                for single_date in date_range(starting_datetime, current_datetime):
                    if single_date < previous_trans_dec.timestamp :
                        dict_for_group[new_key].append(Constants.c_initial_nbETP)
                    elif single_date < next_trans_dec.timestamp:
                        dict_for_group[new_key].append(previous_trans_dec.nb_ETP)
                    else:
                        while (next_trans_dec.timestamp < single_date) \
                                & (len(transitivedecisions_for_thisplayer) != 0):
                            previous_trans_dec = next_trans_dec
                            next_trans_dec = transitivedecisions_for_thisplayer.pop()
                        dict_for_group[new_key].append(previous_trans_dec.nb_ETP)
        # Send the data
        group_name = "group" + str(group.id)
        #??? print("dict_for_group: ", dict_for_group)
        textforgroup = json.dumps(dict_for_group)
        channelsGroup(group_name).send({
            "text": textforgroup,
        })


#################################################
#################################################
class Constants(BaseConstants):
    name_in_url = 'ostende'
    players_per_group = None
    num_rounds = 1

    c_arguments_status = [
        "en cours de validation",
        "validé"
    ]
    c_likes_dislikes_choices = [
        "j'aime",
        "je n'aime pas"
    ]
    c_max_nb_ETP = 50
    c_initial_nbETP = 0
    c_num_decisions_per_round = 1       # Equal to the number of pages in that experience
    c_refresh_to_clients_insec = 3
    c_refresh_from_clients_insec = 3


class Subsession(BaseSubsession):
    def before_session_starts(self):   # called each round
        #??? For tests
        argument1 = Argument(argument_text="text1",
                             arg_status=Constants.c_arguments_status[1])
        argument1.save()  # important: save to DB!
        argument2 = Argument(argument_text="text2",
                             arg_status=Constants.c_arguments_status[0])
        argument2.save()  # important: save to DB!
        argument3 = Argument(argument_text="text3",
                             arg_status=Constants.c_arguments_status[1])
        argument3.save()  # important: save to DB!
        #/???

        # """For each player, create a fixed number of "decision stubs" with random values to be decided upon later."""
        for p in self.get_players():
            p.generate_decision_stubs()


class Group(BaseGroup):
    timerDict_DecisionPage = {"starting_time": 0, "session_id": 0, "round_number": 0, "subsession_id": 0}
    updateTimer_DecisionPage = UpdateData(Constants.c_refresh_to_clients_insec, sendUpdatedData, kwargs = timerDict_DecisionPage)
    timer_DecisionPage_started = models.BooleanField(initial=False)
    timer_DecisionPage_startingTime = models.DateTimeField()

    def startTimer_DecisionPage(self):
        # Start the timer
        if self.timer_DecisionPage_started == False:
            self.timerDict_DecisionPage["starting_time"] = datetime.now()
            self.timerDict_DecisionPage["session_id"] = self.session.id
            self.timerDict_DecisionPage["round_number"] = self.subsession.round_number
            self.timerDict_DecisionPage["subsession_id"] = self.subsession.id
            self.updateTimer_DecisionPage.start()
            self.timer_DecisionPage_startingTime = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
            self.timer_DecisionPage_started = True

    def stopTimer_DecisionPage(self):
        self.updateTimer_DecisionPage.stop() # Called from the next "waitpage"



class Player(BasePlayer):
    def generate_decision_stubs(self):
        # Create a fixed number of "decision stubs"
        for i in range(Constants.c_num_decisions_per_round):
            decision = self.decision_set.create()    # create a new Decision object as part of the player's decision set
            decision.round_number = self.subsession.round_number
            decision.save()     # important: save to DB!


#################################################
# Additional classes for specific data
#################################################
class Argument(Model):   # our custom model inherits from Django's base class "Model"
    argument_text = models.CharField()
    arg_status = models.CharField(choices=Constants.c_arguments_status,
                                  initial=Constants.c_arguments_status[0])

    def __str__(self):
        return "Argument n°{id}: {text}".format(
            id=self.pk, text=self.argument_text)


class Decision(Model):   # our custom model inherits from Django's base class "Model"
    player = ForeignKey(Player)         # creates 1:m relation -> this decision was made by a certain player
    argument = ManyToManyField(Argument,
                               limit_choices_to={'arg_status': Constants.c_arguments_status[1]})    # creates m:m relation
    round_number = models.PositiveIntegerField()
    nb_ETP = models.FloatField(min=0, max=Constants.c_max_nb_ETP, initial=Constants.c_initial_nbETP)


#################################################
# Additional classes to track evolution of transitive decisions
#################################################
class TransitiveDecision(Model):   # our custom model inherits from Django's base class "Model"
    player = ForeignKey(Player)         # creates 1:m relation -> this decision was made by a certain player
    argument = ManyToManyField(Argument,
                               limit_choices_to={'arg_status': Constants.c_arguments_status[1]})    # creates m:m relation
    timestamp = models.DateTimeField()
    round_number = models.PositiveIntegerField()
    nb_ETP = models.FloatField(min=0, max=Constants.c_max_nb_ETP, initial=0)

    def save(self, *args, **kwargs):
        self.timestamp = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
        return super(TransitiveDecision, self).save(*args, **kwargs)


#################################################
# Additional classes to vote for arguments
#################################################
class LikeDislike(Model):
    player = ForeignKey(Player)
    argument = ForeignKey(Argument)

    like_choice = models.CharField(choices=Constants.c_likes_dislikes_choices)


#################################################
# Additional classes for comments
#################################################
class Commentaire(Model):
    player = ForeignKey(Player, blank=True, null=True)# creates 0:m relation -> this comment was made by a certain player, or by an expert
    parent_comment = ForeignKey('self', blank=True, null=True, related_name='children')# creates 0:m relation -> this comment is related to a parent comment or not
    argument = ForeignKey(Argument, blank=True, null=True)# creates 0:m relation -> this comment is related to an argument or not
