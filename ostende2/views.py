from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, Proposition, Appreciation
from django import forms
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from collections import OrderedDict
from .utils import get_field_names_for_csv
from django.http import JsonResponse


##################################
##################################
class LabellingPage(Page):
    form_model = models.Player
    form_fields = ['entite']

    def is_displayed(self):
        return self.subsession.round_number == 1

    def before_next_page(self):
        self.player.participant.vars["entite"] = self.player.entite


##################################
##################################
#??? Keep it?
PropositionFormSet = forms.modelformset_factory(
    Proposition,
    fields=("text", ),
    widgets={"text": forms.Textarea(), },
    extra=0,
)
PropositionFormSetHidden = forms.modelformset_factory(
    Proposition,
    fields=("text", ),
    widgets={"text": forms.HiddenInput(), },
    extra=0,
)


##################################
class EnteringPage(Page):
    def is_displayed(self):
        return ((self.subsession.round_number == 1)
                & (self.player.participant.vars["entite"] != Constants.c_entites[0])
                & (self.player.participant.vars["entite"] != Constants.c_entites[1]))

    def vars_for_template(self):
        # get propositions for this player
        proposition_qs = Proposition.objects.filter(prop_player_ID_ingroup=self.player.id_in_group).order_by('id')
        assert len(proposition_qs) == Constants.c_nb_propositions_per_player
        proposition_formset = PropositionFormSetHidden(queryset=proposition_qs)
        return {
            'entite': self.player.participant.vars['entite'],
            'proposition_formset': proposition_formset,
            'proposition_types_and_forms': zip([prop.type for prop in proposition_qs], proposition_formset.forms),
        }

    def before_next_page(self):
        # get the raw submitted data as dict
        submitted_data = self.form.data
        # get decisions on this page belonging to this player and save as dict with decision ID lookup
        proposition_objs_by_id = {prop.pk: prop
                                  for prop in self.player.proposition_set.all()}
        assert len(proposition_objs_by_id) == Constants.c_nb_propositions_per_player
        for i in range(len(proposition_objs_by_id)):
            input_prefix = 'form-%d-' % i
            # get the id of the original object
            prop_id = int(submitted_data.get(input_prefix + 'id'))
            # get the data that the user has typed in
            proposition_text = submitted_data.get(input_prefix + 'text')
            # lookup by ID and save submitted data
            prop = proposition_objs_by_id[prop_id]
            if proposition_text != Constants.c_initial_proposition_text:
                prop.text = proposition_text
            else:
                prop.text = ""
            # Initialise the version:
            prop.version = 0
            # important: save to DB!
            prop.save()


class EnteringWaitPage(WaitPage):
    def is_displayed(self):
        return ((self.subsession.round_number == 1)
                & (self.player.participant.vars["entite"] != Constants.c_entites[0]))

    def after_all_players_arrive(self):
        pass


##################################
class TuningPage(Page):
    def is_displayed(self):
        if self.subsession.round_number==1:
            return False
        elif self.subsession.round_number==2:
            return ((self.player.participant.vars["entite"]!=Constants.c_entites[0])
                    & (self.player.participant.vars["entite"] != Constants.c_entites[1]))
        else:
            return (self.player.participant.vars["entite"] != Constants.c_entites[1])

    def vars_for_template(self):
        # get the "entity" propositions for this player
        proposition_qs = Proposition.objects.filter(prop_player_ID_ingroup=self.player.id_in_group)\
            .filter(Q(type=Constants.c_proposition_types[0])
                    |Q(type=Constants.c_proposition_types[1])
                    |Q(type=Constants.c_proposition_types[2])).order_by('-id')
        assert len(proposition_qs) == Constants.c_nb_propositions_per_player / 2
        proposition_formset = PropositionFormSetHidden(queryset=proposition_qs)
        propositions_values = [
            {
                "entite": prop.player.participant.vars["entite"],
                "type": prop.type,
                "text": prop.text,
                "version": prop.version,
                "note": prop.average_note,
                "prop_pk": prop.pk,
                "player_pk": prop.player.pk,
            } for prop in proposition_qs]
        # get appreciations for the propositions of this player
        if ((self.subsession.round_number == 1)
                | (self.subsession.round_number == 2)):
            appreciation_values = [
                {
                    "note": app.note,
                    "reaction": app.reaction,
                    "related_version": app.related_version,
                    "up_to_date": app.up_to_date,
                    "app_pk": app.pk,
                    "prop_pk": app.proposition.pk,
                    "player_pk": app.player.pk,
                } for prop in proposition_qs for app in prop.appreciation_set
                    .exclude(player__entite__exact=Constants.c_entites[0])
                    .order_by('id')]
        else:
            appreciation_values = [
                {
                    "note": app.note,
                    "reaction": app.reaction,
                    "related_version": app.related_version,
                    "up_to_date": app.up_to_date,
                    "app_pk": app.pk,
                    "prop_pk": app.proposition.pk,
                    "player_pk": app.player.pk,
                } for prop in proposition_qs for app in prop.appreciation_set
                    .order_by('id')]
        return {
            'entite': self.player.participant.vars['entite'],
            'all_propositions': propositions_values,
            'all_appreciations': appreciation_values,
            'propositions_pk_formsid': [(proposition_qs[i].pk, i) for i in range(len(proposition_qs))],
            'proposition_formset': proposition_formset,
            'proposition_types_and_forms': zip([prop.type for prop in proposition_qs], proposition_formset.forms),
        }

    def before_next_page(self):
        # get the raw submitted data as dict
        submitted_data = self.form.data
        # get decisions on this page belonging to this player and save as dict with decision ID lookup
        proposition_objs_by_id = {prop.pk: prop
                                  for prop in Proposition.objects.filter(prop_player_ID_ingroup=self.player.id_in_group)
                                      .filter(Q(type=Constants.c_proposition_types[0])
                                              |Q(type=Constants.c_proposition_types[1])
                                              |Q(type=Constants.c_proposition_types[2]))}
        assert len(proposition_objs_by_id) == Constants.c_nb_propositions_per_player / 2

        for i in range(len(proposition_objs_by_id)):
            input_prefix = 'form-%d-' % i
            # get the id of the original object
            prop_id = int(submitted_data.get(input_prefix + 'id'))
            # get the data that the user has typed in
            proposition_text = submitted_data.get(input_prefix + 'text')
            # lookup by ID and save submitted data
            prop = proposition_objs_by_id[prop_id]
            if proposition_text != prop.text:
                prop.text = proposition_text
                prop.version += 1
                for app in prop.appreciation_set.all():
                    app.up_to_date = False
            elif proposition_text == Constants.c_initial_proposition_text:
                prop.text = ""
            # important: save to DB!
            prop.save()


class TuningICLPage(Page):
    def is_displayed(self):
        return((self.player.participant.vars["entite"] == Constants.c_entites[0])
               & (self.subsession.round_number == 2))

    def vars_for_template(self):
        # get the "entity" propositions for this player to build the form
        proposition_qs = Proposition.objects.filter(prop_player_ID_ingroup=self.player.id_in_group)\
            .filter(Q(type=Constants.c_proposition_types[0])
                    |Q(type=Constants.c_proposition_types[1])
                    |Q(type=Constants.c_proposition_types[2])).order_by('id')
        assert len(proposition_qs) == Constants.c_nb_propositions_per_player / 2
        proposition_formset = PropositionFormSet(queryset=proposition_qs)
        # get the "ICL" propositions from all other players to display them
        alliclproposition_qs = Proposition.objects.exclude(prop_player_ID_ingroup=self.player.id_in_group)\
            .filter(Q(type=Constants.c_proposition_types[3])
                    |Q(type=Constants.c_proposition_types[4])
                    |Q(type=Constants.c_proposition_types[5])).order_by('-id')
        alliclpropositions_values = [
            {
                "entite": prop.player.participant.vars["entite"],
                "type": prop.type,
                "text": prop.text,
                "version": prop.version,
                "note": prop.average_note,
                "prop_pk": prop.pk,
                "player_pk": prop.player.pk,
            } for prop in alliclproposition_qs]
        # get appreciations for these alliclpropositions to pop-up them
        alliclappreciation_values = [
            {
                "note": app.note,
                "reaction": app.reaction,
                "related_version": app.related_version,
                "up_to_date": app.up_to_date,
                "app_pk": app.pk,
                "prop_pk": app.proposition.pk,
                "player_pk": app.player.pk,
            } for prop in alliclproposition_qs for app in prop.appreciation_set
                .exclude(player__entite__exact=Constants.c_entites[0])
                .order_by('id')]
        # send everything
        return {
            'entite': self.player.participant.vars['entite'],
            'allicl_propositions': alliclpropositions_values,
            'allicl_appreciations': alliclappreciation_values,
            'propositions_pk_formsid': [(proposition_qs[i].pk, i) for i in range(len(proposition_qs))],
            'proposition_formset': proposition_formset,
            'proposition_types_and_forms': zip([prop.type for prop in proposition_qs], proposition_formset.forms),
        }

    def before_next_page(self):
        # get the raw submitted data as dict
        submitted_data = self.form.data
        # get decisions on this page belonging to this player and save as dict with decision ID lookup
        proposition_objs_by_id = {prop.pk: prop
                                  for prop in Proposition.objects.filter(prop_player_ID_ingroup=self.player.id_in_group)
                                      .filter(Q(type=Constants.c_proposition_types[0])
                                              |Q(type=Constants.c_proposition_types[1])
                                              |Q(type=Constants.c_proposition_types[2]))}
        assert len(proposition_objs_by_id) == Constants.c_nb_propositions_per_player / 2
        for i in range(len(proposition_objs_by_id)):
            input_prefix = 'form-%d-' % i
            # get the id of the original object
            prop_id = int(submitted_data.get(input_prefix + 'id'))
            # get the data that the user has typed in
            proposition_text = submitted_data.get(input_prefix + 'text')
            # lookup by ID and save submitted data
            prop = proposition_objs_by_id[prop_id]
            if proposition_text != prop.text:
                prop.text = proposition_text
                prop.version += 1
                for app in prop.appreciation_set.all():
                    app.up_to_date = False
            elif proposition_text == Constants.c_initial_proposition_text:
                prop.text = ""
            # important: save to DB!
            prop.save()


class TuningWaitPage(WaitPage):
    def is_displayed(self):
        return self.subsession.round_number != 1

    def after_all_players_arrive(self):
        pass


##################################
AppreciationFormSet = forms.modelformset_factory(
    Appreciation,
    fields=("reaction",),
    widgets={"reaction": forms.HiddenInput(), },
    extra=0,
)



class CommentingPage(Page):
    def is_displayed(self):
        if ((self.subsession.round_number == 1)
                & (self.player.participant.vars["entite"] == Constants.c_entites[0])):
            return False
        elif self.subsession.round_number == Constants.num_rounds:
            return False
        else:
            return True

    def vars_for_template(self):
        if self.subsession.round_number == 1:
            # get propositions for all players except this one and ICL at the first round
            proposition_qs = Proposition.objects \
                .exclude(prop_player_ID_ingroup=self.player.id_in_group) \
                .exclude(player__entite__exact=Constants.c_entites[0]) \
                .exclude(player__entite__exact=Constants.c_entites[1]) \
                .filter(Q(type=Constants.c_proposition_types[0])
                        |Q(type=Constants.c_proposition_types[1])
                        |Q(type=Constants.c_proposition_types[2])) \
                .select_related('player')\
                .order_by('-id')
        else:
            # get propositions for all players except this one and the observation group
            proposition_qs = Proposition.objects\
                .exclude(prop_player_ID_ingroup=self.player.id_in_group) \
                .exclude(player__entite__exact=Constants.c_entites[1]) \
                .filter(Q(type=Constants.c_proposition_types[0])
                        |Q(type=Constants.c_proposition_types[1])
                        |Q(type=Constants.c_proposition_types[2])) \
                .select_related('player')\
                .order_by('-id')
        propositions_values = [
            {
                "entite": prop.player.participant.vars["entite"],
                "type": prop.type,
                "text": prop.text,
                "version": prop.version,
                "note": prop.average_note,
                "prop_pk": prop.pk,
                "player_pk": prop.player.pk,
            } for prop in proposition_qs]
        print("-----------------------------------------------")
        print("propositions_values: ", propositions_values)
        # get appreciations for this player
        if self.subsession.round_number == 1:
            # get appreciations for my player except this one and ICL at the first round
            appreciation_qs = Appreciation.objects \
                .filter(app_player_ID_ingroup=self.player.id_in_group) \
                .exclude(proposition__player__entite__exact=Constants.c_entites[0]) \
                .exclude(proposition__player__entite__exact=Constants.c_entites[1]) \
                .filter(Q(proposition__type=Constants.c_proposition_types[0])
                        |Q(proposition__type=Constants.c_proposition_types[1])
                        |Q(proposition__type=Constants.c_proposition_types[2])) \
                .select_related('player')\
                .order_by('-id')
        else:
            # get appreciations for all players except this one
            appreciation_qs = Appreciation.objects\
                .filter(app_player_ID_ingroup=self.player.id_in_group) \
                .exclude(proposition__player__entite__exact=Constants.c_entites[1]) \
                .filter(Q(proposition__type=Constants.c_proposition_types[0])
                        |Q(proposition__type=Constants.c_proposition_types[1])
                        |Q(proposition__type=Constants.c_proposition_types[2])) \
                .select_related('player')\
                .order_by('-id')
        appreciation_values = [
            {
                "note": app.note,
                "reaction": app.reaction,
                "related_version": app.related_version,
                "up_to_date": app.up_to_date,
                "app_pk": app.pk,
                "prop_pk": app.proposition.pk,
                "player_pk": app.player.pk,
            } for app in appreciation_qs]
        print("-----------------------------------------------")
        print("appreciation_values: ", appreciation_values)
        appreciation_formset = AppreciationFormSet(queryset=appreciation_qs)
        return {
            'entite': self.player.participant.vars['entite'],
            'all_propositions': propositions_values,
            'all_appreciations': appreciation_values,
            'appreciation_pk_formsid': [(appreciation_qs[i].pk, i) for i in range(len(appreciation_qs))],
            'appreciation_formset': appreciation_formset,
            'appreciation_pk_forms': zip([app.pk for app in appreciation_qs], appreciation_formset.forms),
        }

    def before_next_page(self):
        # get the raw submitted data as dict
        submitted_data = self.form.data
        # get appreciations on this page belonging to this player and save as dict with decision ID lookup
        if self.subsession.round_number == 1:
            # get appreciations for all players except this one and ICL at the first round
            appreciation_objs_by_id = {app.pk: app
                                       for app in
                                       Appreciation.objects \
                                           .filter(app_player_ID_ingroup=self.player.id_in_group) \
                                           .exclude(proposition__player__entite__exact=Constants.c_entites[0])
                                           .exclude(proposition__player__entite__exact=Constants.c_entites[1])
                                           .filter(Q(proposition__type=Constants.c_proposition_types[0])
                                                   |Q(proposition__type=Constants.c_proposition_types[1])
                                                   |Q(proposition__type=Constants.c_proposition_types[2]))}
        else:
            # get appreciations for all players except this one
            appreciation_objs_by_id = {app.pk: app
                                       for app in
                                       Appreciation.objects \
                                           .filter(app_player_ID_ingroup=self.player.id_in_group)
                                           .exclude(proposition__player__entite__exact=Constants.c_entites[1])
                                           .filter(Q(proposition__type=Constants.c_proposition_types[0])
                                                   | Q(proposition__type=Constants.c_proposition_types[1])
                                                   | Q(proposition__type=Constants.c_proposition_types[2]))}

        for i in range(len(appreciation_objs_by_id)):
            input_prefix = 'form-%d-' % i
            # get the id of the original object
            app_id = int(submitted_data.get(input_prefix + 'id'))
            # get the data that the user has typed in
            appreciation_text = submitted_data.get(input_prefix + 'reaction')
            appreciation_note = submitted_data.get(input_prefix + 'note')
            # lookup by ID
            app = appreciation_objs_by_id[app_id]
            # Save the data
            app.note = appreciation_note
            if appreciation_text != app.reaction:
                # Save the newly update appreciation
                app.reaction = appreciation_text
                app.related_version = app.proposition.version
                app.up_to_date = True
            elif appreciation_text == Constants.c_initial_reaction_text:
                app.reaction = ""
            # important: save to DB!
            app.save()


class CommentingWaitPage(WaitPage):
    def is_displayed(self):
        return True

    def after_all_players_arrive(self):
        #??? self.subsession.compute_average_notes()
        pass



##################################
class ResultsPage(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        # get propositions for all players except this one
        proposition_qs = Proposition.objects\
            .exclude(player__entite__exact=Constants.c_entites[1])\
            .filter(Q(type=Constants.c_proposition_types[0])
                    | Q(type=Constants.c_proposition_types[1])
                    | Q(type=Constants.c_proposition_types[2]))\
            .select_related('player').order_by('player__average_note').order_by('-id')
        propositions_values = [
            {
                "entite": prop.player.participant.vars["entite"],
                "type": prop.type,
                "text": prop.text,
                "version": prop.version,
                #??? "player_note": prop.player.participant.vars['average_note'],
                "note": prop.average_note,
                "prop_pk": prop.pk,
                "player_pk": prop.player.pk,
            } for prop in proposition_qs]
        # get appreciations for this player
        appreciation_qs = Appreciation.objects.select_related('player')
        appreciation_values = [
            {
                "note": app.note,
                "reaction": app.reaction,
                "related_version": app.related_version,
                "up_to_date": app.up_to_date,
                "app_pk": app.pk,
                "prop_pk": app.proposition.pk,
                "player_pk": app.player.pk,

            } for app in appreciation_qs]
        appreciation_formset = AppreciationFormSet(queryset=appreciation_qs)
        return {
            'entite': self.player.participant.vars['entite'],
            'all_propositions': propositions_values,
            'all_appreciations': appreciation_values,
            'appreciation_pk_formsid': [(appreciation_qs[i].pk, i) for i in range(len(appreciation_qs))],
            'appreciation_formset': appreciation_formset,
            'appreciation_pk_forms': zip([app.pk for app in appreciation_qs], appreciation_formset.forms),
        }


##################################
##################################
page_sequence = [
    LabellingPage,
    EnteringPage,
    EnteringWaitPage,
    TuningPage,
    TuningICLPage,
    TuningWaitPage,
    CommentingPage,
    CommentingWaitPage,
    ResultsPage,
]


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
        .prefetch_related('proposition_set') \
        .prefetch_related('appreciation_set') \
        .all()

    session_fieldnames = []
    subsess_fieldnames = []  # will be defined by get_field_names_for_csv
    group_fieldnames = []  # will be defined by get_field_names_for_csv
    player_fieldnames = ['entite', 'average_note']  # will be defined by get_field_names_for_csv
    proposition_fieldnames = ['prop_player_ID_ingroup', 'type', 'text', 'version', 'average_note']
    appreciation_fieldnames = ['app_player_ID_ingroup', 'note', 'reaction', 'related_version', 'up_to_date']

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
                    p_output['propositions'] = []
                    # loop through all decisions ordered by ID
                    propositions = p.proposition_set.order_by('id')
                    for prop in propositions:
                        prop_output = create_odict_from_object(prop, proposition_fieldnames)
                        # add some additional decision information
                        prop_output['appreciations'] = []
                        # loop through all arguments ordered by ID
                        appreciations = prop.appreciation_set.order_by('id')
                        for app in appreciations:
                            app_output = create_odict_from_object(app, appreciation_fieldnames)
                            prop_output['appreciations'].append(app_output)
                        p_output['propositions'].append(prop_output)

                    g_output['players'].append(p_output)

                subsess_output['groups'].append(g_output)

            sess_output['subsessions'].append(subsess_output)

        output.append(sess_output)

    return JsonResponse(output, safe=False)
