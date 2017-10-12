from channels import Group as channelsGroup
from channels.sessions import channel_session
import random
from .models import QuestionToExpert, TransitiveDecision, Argument, Choices, Player as OtreePlayer, Group as OtreeGroup, Constants
import json


#############################################
#############################################
# Connected to websocket.connect
def ws_connect(message, group_name, question):
    print("*********CONNECT************")
    channelsGroup(group_name).add(message.reply_channel)

# Connected to websocket.receive
def ws_message(message, group_name, question):
    print("*********RECEIVE************")
    print("group_name: ", group_name)
    # Decrypt the url
    group_id = group_name[5:]
    question_nb = int(question[8:])
    # Decrypt the received message
    jsonmessage = json.loads(message.content['text'])
    player_id = jsonmessage['id']
    myplayer = OtreePlayer.objects.get(id=player_id)
    if 'decision' in jsonmessage:
        # Treat the decision
        argument = jsonmessage['argument']
        # Save the current decision
        currentdecision = myplayer.transitivedecision_set.create()
        currentdecision.related_question = Choices.questions[question_nb]
        currentdecision.player_decision = jsonmessage['decision']
        for a in argument:
            currentdecision.argument.add(Argument.objects.get(pk=a))
        currentdecision.save()  # important: save to DB!
    if 'question2expert' in jsonmessage:
        # Treat the question
        question = myplayer.questiontoexpert_set.create()
        question.question_text = jsonmessage['question2expert']
        question.related_question = Choices.questions[question_nb]
        question.save()
        # Update the experts with this new question
        textforgroup = json.dumps({
                    "whatsnew": "newquestion",
                })
        channelsGroup("EXPERTS").send({
            "text": textforgroup,
        })

# Connected to websocket.disconnect
def ws_disconnect(message, group_name, question):
    print("*********DISCONNECT************")
    channelsGroup(group_name).discard(message.reply_channel)


#############################################
#############################################
# Connected to websocket.connect
def ws_experts_connect(message):
    print("*********CONNECT************")
    channelsGroup("EXPERTS").add(message.reply_channel)

# Connected to websocket.receive
def ws_experts_message(message):
    print("*********RECEIVE************")
    # Decrypt the received message
    jsonmessage = json.loads(message.content['text'])
    if 'answer2question' in jsonmessage:
        # Get the corresponding question
        related_question = QuestionToExpert.objects.get(pk=jsonmessage['questionid'])
        # Treat the answer
        new_answer = related_question.answerfromexpert_set.create(answer_text = jsonmessage['answer2question'])
        new_answer.save()   # important: save to DB!
    if 'argument_explanation' in jsonmessage:
        # Treat the argument
        new_argument = Argument.objects.create(argument_explanation = jsonmessage['argument_explanation'],
                                               nb_votes = 0,
                                               arg_status = Constants.c_arguments_status[1])
        new_argument.save()   # important: save to DB!

# Connected to websocket.disconnect
def ws_experts_disconnect(message):
    print("*********DISCONNECT************")
    channelsGroup("EXPERTS").discard(message.reply_channel)
