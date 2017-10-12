from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage

from .models import Decision, Argument, QuestionToExpert

from django.forms import modelformset_factory
from django import forms
from collections import OrderedDict
from .utils import get_field_names_for_csv
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.shortcuts import render


##################################
##################################
DecisionFormSet = modelformset_factory(
    Decision,
    fields=("player_decision", "argument",),
    widgets={"player_decision":forms.HiddenInput(), "argument":forms.CheckboxSelectMultiple(),},
    extra=0,
)
QuestionToExpertFormSet = modelformset_factory(
    QuestionToExpert,
    fields=("question_text",),
    widgets={"question_text":forms.Textarea(),},
    extra=0,
)


##################################
##################################
class ExpertsView(TemplateView):
    template_name = "primo_fmr/Experts.html"

    def get(self, request, *args, **kwargs):
        existing_questions_qs = QuestionToExpert.objects.prefetch_related('answerfromexpert_set')
        context = {'existing_questions': existing_questions_qs}
        return render(request=request, template_name = self.template_name, context=context)


##################################
##################################
class Pop1Nb1Page(Page):
    def vars_for_template(self):
        # get decisions for this player
        decision_qs = Decision.objects.filter(player__exact=self.player)\
            .filter(related_question__exact=models.Choices.questions[1])
        assert len(decision_qs) == 1    # As we have 1 decision per page
        decision_formset = DecisionFormSet(queryset=decision_qs)
        existing_questions_qs = QuestionToExpert.objects.filter(related_question__exact=models.Choices.questions[1])\
            .prefetch_related('answerfromexpert_set')
        # Start the timer
        self.group.startTimer_Q1Pop1()

        return {
            'decision_formset': decision_formset,
            'decision_arguments': decision_formset.forms,
            'nb_players_group': len(self.group.get_players()),
            'existing_questions': existing_questions_qs,
        }

    def before_next_page(self):
        # Stop the timer
        self.group.stopTimer_Q1Pop1()
        # get the raw submitted data as dict
        submitted_data = self.form.data

        # get decisions on this page belonging to this player and save as dict with decision ID lookup
        decision_objs_by_id = {dec.pk: dec
                               for dec in self.player.decision_set.all()
                                   .filter(related_question__exact=models.Choices.questions[1])}
        assert len(decision_objs_by_id) == 1    # As we have 1 decision per page...

        for i in range(len(decision_objs_by_id)):
            input_prefix = 'form-%d-' % i

            # get the inputs
            dec_id = int(submitted_data.get(input_prefix + 'id'))
            player_decision = submitted_data.get(input_prefix + 'player_decision')
            argument = submitted_data.getlist(input_prefix + 'argument')

            # lookup by ID and save submitted data
            dec = decision_objs_by_id[dec_id]
            if player_decision != '':
                dec.player_decision = player_decision
            else:
                dec.player_decision = 0
            # save the different arguments the player has checked
            for a in argument:
                # Add a vote to this argument
                Argument.objects.get(pk=a).nb_votes += 1
                Argument.objects.get(pk=a).save()
                # Attach this argument to my decision
                dec.argument.add(Argument.objects.get(pk=a))

            # important: save to DB!
            dec.save()


class Pop1Nb2Page(Page):
    def vars_for_template(self):
        # get decisions for this player
        decision_qs = Decision.objects.filter(player__exact=self.player) \
            .filter(related_question__exact=models.Choices.questions[2])
        assert len(decision_qs) == 1  # As we have 1 decision per page
        decisions_formset = DecisionFormSet(queryset=decision_qs)

        return {
            'decision_formset': decisions_formset,
            'decision_arguments': decisions_formset.forms,
        }

    def before_next_page(self):
        # get the raw submitted data as dict
        submitted_data = self.form.data

        # get decisions on this page belonging to this player and save as dict with decision ID lookup
        decision_objs_by_id = {dec.pk: dec
                               for dec in self.player.decision_set.all()
                                   .filter(related_question__exact=models.Choices.questions[2])}
        assert len(decision_objs_by_id) == 1  # As we have 1 decision per page...

        for i in range(len(decision_objs_by_id)):
            input_prefix = 'form-%d-' % i

            # get the inputs
            dec_id = int(submitted_data.get(input_prefix + 'id'))
            player_decision = submitted_data.get(input_prefix + 'player_decision')
            argument = submitted_data.getlist(input_prefix + 'argument')

            # lookup by ID and save submitted data
            dec = decision_objs_by_id[dec_id]
            if player_decision != '':
                dec.player_decision = player_decision
            else:
                dec.player_decision = 0
            # save the different arguments the player has checked
            for a in argument:
                # Add a vote to this argument
                Argument.objects.get(pk=a).nb_votes += 1
                Argument.objects.get(pk=a).save()
                # Attach this argument to my decision
                dec.argument.add(Argument.objects.get(pk=a))

            # important: save to DB!
            dec.save()


class Pop1Nb3Page(Page):

    def vars_for_template(self):
        # get decisions for this player
        decision_qs = Decision.objects.filter(player__exact=self.player) \
            .filter(related_question__exact=models.Choices.questions[3])
        assert len(decision_qs) == 1  # As we have 1 decision per page
        decisions_formset = DecisionFormSet(queryset=decision_qs)

        return {
            'decision_formset': decisions_formset,
            'decision_arguments': decisions_formset.forms,
        }

    def before_next_page(self):
        # get the raw submitted data as dict
        submitted_data = self.form.data

        # get decisions on this page belonging to this player and save as dict with decision ID lookup
        decision_objs_by_id = {dec.pk: dec
                               for dec in self.player.decision_set.all()
                                   .filter(related_question__exact=models.Choices.questions[3])}
        assert len(decision_objs_by_id) == 1  # As we have 1 decision per page...

        for i in range(len(decision_objs_by_id)):
            input_prefix = 'form-%d-' % i

            # get the inputs
            dec_id = int(submitted_data.get(input_prefix + 'id'))
            player_decision = submitted_data.get(input_prefix + 'player_decision')
            argument = submitted_data.getlist(input_prefix + 'argument')

            # lookup by ID and save submitted data
            dec = decision_objs_by_id[dec_id]
            if player_decision != '':
                dec.player_decision = player_decision
            else:
                dec.player_decision = 0
            # save the different arguments the player has checked
            for a in argument:
                # Add a vote to this argument
                Argument.objects.get(pk=a).nb_votes += 1
                Argument.objects.get(pk=a).save()
                # Attach this argument to my decision
                dec.argument.add(Argument.objects.get(pk=a))

            # important: save to DB!
            dec.save()


##################################
##################################
@login_required
def export_view_json(request):
    """
    Custom view function to export full results for this game as JSON file
    """

    def create_odict_from_object(obj, fieldnames):
        """
        Small helper function to create an OrderedDict from an object <obj> using <fieldnames>
        as attributes.
        """
        data = OrderedDict()
        for f in fieldnames:
            data[f] = getattr(obj, f)
        return data

    # get the complete result data from the database
    qs_results = models.Player.objects.select_related('subsession', 'subsession__session', 'group', 'participant') \
        .prefetch_related('decision_set__argument') \
        .prefetch_related('transitivedecision_set') \
        .all()

    session_fieldnames = []  # will be defined by get_field_names_for_csv
    subsess_fieldnames = []  # will be defined by get_field_names_for_csv
    group_fieldnames = []  # will be defined by get_field_names_for_csv
    player_fieldnames = []  # will be defined by get_field_names_for_csv
    decision_fieldnames = ['player_decision', 'related_question']
    transitivedecision_fieldnames = ['player_decision', 'related_question', 'timestamp']
    argument_fieldnames = ['argument_explanation', 'nb_votes']

    # get all sessions, order them by label
    sessions = sorted(set([p.subsession.session for p in qs_results]), key=lambda x: x.label)

    # this will be a list that contains data of all sessions
    output = []

    # loop through all sessions
    for sess in sessions:
        session_fieldnames = session_fieldnames or get_field_names_for_csv(sess.__class__)
        sess_output = create_odict_from_object(sess, session_fieldnames)
        sess_output['subsessions'] = []

        # loop through all subsessions (i.e. rounds) ordered by round number
        subsessions = sorted(sess.get_subsessions(), key=lambda x: x.round_number)
        for subsess in subsessions:
            subsess_fieldnames = subsess_fieldnames or get_field_names_for_csv(subsess.__class__)
            subsess_output = create_odict_from_object(subsess, subsess_fieldnames)
            subsess_output['groups'] = []

            # loop through all groups ordered by ID
            groups = sorted(subsess.get_groups(), key=lambda x: x.id_in_subsession)
            for g in groups:
                group_fieldnames = group_fieldnames or get_field_names_for_csv(g.__class__)
                g_output = create_odict_from_object(g, group_fieldnames)
                g_output['players'] = []

                # loop through all players ordered by ID
                players = sorted(g.get_players(), key=lambda x: x.participant.id_in_session)
                for p in players:
                    player_fieldnames = player_fieldnames or get_field_names_for_csv(p.__class__)
                    p_output = create_odict_from_object(p, player_fieldnames)

                    # add some additional player information
                    p_output['participant_id_in_session'] = p.participant.id_in_session
                    p_output['decisions'] = []
                    # loop through all decisions ordered by ID
                    decisions = p.decision_set.order_by('id')
                    for dec in decisions:
                        dec_output = create_odict_from_object(dec, decision_fieldnames)
                        # add some additional decision information
                        dec_output['arguments'] = []
                        # loop through all arguments ordered by ID
                        arguments = dec.argument.order_by('id')
                        for arg in arguments:
                            arg_output = create_odict_from_object(arg, argument_fieldnames)
                            dec_output['arguments'].append(arg_output)
                        p_output['decisions'].append(dec_output)

                    p_output['transitivedecisions'] = []
                    # loop through all transitivedecisions ordered by ID
                    transitivedecisions = p.transitivedecision_set.order_by('id')
                    for transdec in transitivedecisions:
                        transdec_output = create_odict_from_object(transdec, transitivedecision_fieldnames)
                        # add some additional transitivedecision information
                        transdec_output['arguments'] = []
                        # loop through all arguments ordered by ID
                        arguments = transdec.argument.order_by('id')
                        for arg in arguments:
                            arg_output = create_odict_from_object(arg, argument_fieldnames)
                            transdec_output['arguments'].append(arg_output)
                        p_output['transitivedecisions'].append(transdec_output)

                    g_output['players'].append(p_output)

                subsess_output['groups'].append(g_output)

            sess_output['subsessions'].append(subsess_output)

        output.append(sess_output)

    return JsonResponse(output, safe=False)


##################################
##################################
page_sequence = [
    Pop1Nb1Page,
    Pop1Nb2Page,
    Pop1Nb3Page,
]
