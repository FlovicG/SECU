from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from django.views.generic import TemplateView
from .models import Commentaire, Decision
from django import forms
from django.shortcuts import render


#################################################
#################################################
class ExpertsView(TemplateView):
    template_name = "ostende/Experts.html"

    def get(self, request, *args, **kwargs):
        existing_comments_qs = Commentaire.objects.select_related('player', 'parent_comment', 'argument').all()
        context = {'existing_questions': existing_comments_qs}
        return render(request=request, template_name = self.template_name, context=context)


#################################################
#################################################
DecisionFormSet = forms.modelformset_factory(
    Decision,
    fields=("nb_ETP", "argument",),
    widgets={"nb_ETP": forms.HiddenInput(), "argument": forms.CheckboxSelectMultiple(), },
    extra=0,
)


#################################################
class DecisionPage(Page):
    def vars_for_template(self):
        # get decisions for this player
        decision_qs = Decision.objects.filter(player__exact=self.player)\
            .filter(round_number__exact=self.subsession.round_number)
        assert len(decision_qs) == Constants.c_num_decisions_per_round
        decision_formset = DecisionFormSet(queryset=decision_qs)
        # Start the timer
        self.group.startTimer_DecisionPage()
        return {
            'decision_formset': decision_formset,
            'decision_arguments': decision_formset.forms,
            'current_decision': 0,
        }


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        # Stop the timer
        self.group.stopTimer_DecisionPage()


class Results(Page):
    pass


#################################################
#################################################
page_sequence = [
    DecisionPage,
    ResultsWaitPage,
    Results
]
