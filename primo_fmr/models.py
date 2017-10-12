from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from otree.db.models import Model, ForeignKey, ManyToManyField
import random

from channels import Group as channelsGroup
import json
import threading
from datetime import timedelta, datetime
from django.utils import timezone
from collections import OrderedDict

author = 'Your name here'

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
        yield start_date + timedelta(seconds=n*Constants.refresh_period_insec)


def sendUpdatedData(**kwargs):
    def create_odict_from_object(obj, fieldnames):
        data = OrderedDict()
        for f in fieldnames:
            data[f] = getattr(obj, f)
        return data

    groups_qs = Group.objects.filter(session_id = kwargs["session_id"],
                                     subsession_id = kwargs["subsession_id"],
                                     round_number = kwargs["round_number"])
    # Update all groups
    qs_players = Player.objects.select_related('subsession', 'group') \
        .prefetch_related('transitivedecision_set__argument') \
        .all()

    starting_datetime = timezone.make_aware(kwargs["starting_time"], timezone.get_default_timezone())
    current_datetime = timezone.make_aware(datetime.now(), timezone.get_default_timezone())

    data_dec1 = []
    data_dec2 = []
    data_dec_notyet = []
    i = 0
    for single_date in date_range(starting_datetime, current_datetime):
        data_dec1.append(0)
        data_dec2.append(0)
        data_dec_notyet.append(0)
        for p in qs_players:
            transitivedecisions = list(p.transitivedecision_set.order_by('timestamp'))
            while True:
                if len(transitivedecisions) == 0:
                    data_dec_notyet[i] += 1
                    break
                last_trans_dec = transitivedecisions.pop()
                if last_trans_dec.timestamp < single_date:
                    if last_trans_dec.player_decision == Choices.choices_q123[1]:
                        data_dec1[i] += 1
                    elif last_trans_dec.player_decision == Choices.choices_q123[2]:
                        data_dec2[i] += 1
                    break
        i += 1
    for group in groups_qs:
        # Build the data
        # Send the data
        group_name = "group" + str(group.id)
        textforgroup = json.dumps({
            "datanotyet": data_dec_notyet,
            "data1": data_dec1,
            "data2": data_dec2,
        })
        channelsGroup(group_name).send({
            "text": textforgroup,
        })


#########################################
#########################################
class Choices(Model):
    questions = [
        "uninitialised",
        "pop1_nb1",
        "pop1_nb2",
        "pop1_nb3",
    ]
    choices_q123 = [0, 1, 2]
    initial_arguments_q123 = [
        "Age",
        "Valeur sociétale",
        "Respecte la loi",
        "Parce que c'est comme ça",
    ]


#########################################
# Traditional oTree classes
#########################################
class Constants(BaseConstants):
    name_in_url = 'primo_fmr'
    players_per_group = None
    num_rounds = 1

    num_decisions_per_round = 3     # Equal to the number of pages in that experience.
    refresh_period_insec = 1

    c_arguments_status = [
        "en cours de validation",
        "validé"
    ]


class Subsession(BaseSubsession):
    def before_session_starts(self):   # called each round
        # At the very beginning, initialise the possible arguments
        if self.round_number == 1:
            # Empty the table
            Argument.objects.all().delete()
            # Fill the table with initial arguments
            for a in Choices.initial_arguments_q123:
                argument = Argument(argument_explanation = a,
                                    nb_votes = random.randint(20,70), #???
                                    arg_status = Constants.c_arguments_status[1])
                argument.save()     # important: save to DB!
            #??? Fill the table with fake questions
            players = self.get_players()
            question1 = players[0].questiontoexpert_set.create()
            question1.question_text = "Première question"
            question1.related_question = Choices.questions[2]
            question1.save()  # important: save to DB!
            question2 = players[1].questiontoexpert_set.create()
            question2.question_text = "Deuxième question"
            question2.related_question = Choices.questions[1]
            question2.save()  # important: save to DB!
            answer1 = AnswerFromExpert(answer_text = "Voilà la réponse",
                                       related_question = question2)
            answer1.save()  # important: save to DB!
            #???/

        # """For each player, create a fixed number of "decision stubs" with random values to be decided upon later."""
        for p in self.get_players():
            p.generate_decision_stubs()


class Group(BaseGroup):
    timerDict_Q1Pop1 = {"starting_time": 0, "session_id": 0, "round_number": 0, "subsession_id": 0}
    updateTimer_Q1Pop1 = UpdateData(Constants.refresh_period_insec, sendUpdatedData, kwargs = timerDict_Q1Pop1)
    timer_Q1Pop1_started = models.BooleanField(initial=False)
    timer_Q1Pop1_startingTime = models.DateTimeField()

    def startTimer_Q1Pop1(self):
        # Start the timer
        if self.timer_Q1Pop1_started == False:
            self.timerDict_Q1Pop1["starting_time"] = datetime.now()
            self.timerDict_Q1Pop1["session_id"] = self.session.id
            self.timerDict_Q1Pop1["round_number"] = self.subsession.round_number
            self.timerDict_Q1Pop1["subsession_id"] = self.subsession.id
            self.updateTimer_Q1Pop1.start()
            self.timer_Q1Pop1_startingTime = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
            self.timer_Q1Pop1_started = True

    def stopTimer_Q1Pop1(self):
        self.updateTimer_Q1Pop1.stop() #??? Wait that the last player has left before stopping


class Player(BasePlayer):

    def generate_decision_stubs(self):
        """
        Create a fixed number of "decision stubs", i.e. decision objects that only have a random "value" field on
        which the player will base her or his decision later in the game.
        """
        for i in range(Constants.num_decisions_per_round):
            decision = self.decision_set.create()    # create a new Decision object as part of the player's decision set
            decision.related_question = Choices.questions[i+1]
            decision.save()     # important: save to DB!


#########################################
# Additional classes for specific data
#########################################
class Argument(Model):   # our custom model inherits from Django's base class "Model"
    argument_explanation = models.CharField()
    nb_votes = models.PositiveIntegerField(initial=0)
    arg_status = models.CharField(choices=Constants.c_arguments_status,
                                  initial = Constants.c_arguments_status[0])

    class Meta:
        ordering = ['-nb_votes']

    def __str__(self):
        return "Argument n°{id}: {explanation}, choisi {nb_votes} fois.".format(
            id=self.pk, explanation=self.argument_explanation, nb_votes=self.nb_votes)


class Decision(Model):   # our custom model inherits from Django's base class "Model"
    player_decision = models.IntegerField(choices=Choices.choices_q123, initial=Choices.choices_q123[0])
    related_question = models.CharField(choices=Choices.questions, initial=Choices.questions[0])

    player = ForeignKey(Player)         # creates 1:m relation -> this decision was made by a certain player
    argument = ManyToManyField(Argument)    # creates m:m relation


#########################################
# Additional classes to track evolution of transitive decisions
#########################################
class TransitiveDecision(Model):   # our custom model inherits from Django's base class "Model"
    player_decision = models.IntegerField(choices=Choices.choices_q123, initial=Choices.choices_q123[0])
    related_question = models.CharField(choices=Choices.questions, initial=Choices.questions[0])
    timestamp = models.DateTimeField()

    player = ForeignKey(Player)         # creates 1:m relation -> this decision was made by a certain player
    argument = ManyToManyField(Argument)    # creates m:m relation

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.timestamp = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
        return super(TransitiveDecision, self).save(*args, **kwargs)


#########################################
# Additional classes for questions and answers with experts
#########################################
class QuestionToExpert(Model):
    question_text = models.TextField()
    related_question = models.CharField(choices=Choices.questions, initial=Choices.questions[0])
    player = ForeignKey(Player)  # creates 1:m relation -> this question was asked by a certain player


class AnswerFromExpert(Model):
    answer_text = models.TextField()
    related_question = ForeignKey(QuestionToExpert)  # creates 1:m relation -> this answers a particular question
