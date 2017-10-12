from channels import Group as channelsGroup
from channels.sessions import channel_session
from .models import Argument, Player as OtreePlayer
import json


#############################################
#############################################
# Connected to websocket.connect for players
def ws_connect(message, group_name):
    print("*********CONNECT************")
    channelsGroup(group_name).add(message.reply_channel)

# Connected to websocket.receive for players
def ws_message(message, group_name):
    print("*********RECEIVE************")
    print("group_name: ", group_name)
    # Decrypt the received message
    jsonmessage = json.loads(message.content['text'])
    player_id = jsonmessage['player_id']
    myplayer = OtreePlayer.objects.get(id=player_id)
    if 'nb_ETP' in jsonmessage:
        # Treat the decision
        argument = jsonmessage['argument']
        # Save the current decision
        currentdecision = myplayer.transitivedecision_set.create()
        currentdecision.round_number = jsonmessage['round_number']
        currentdecision.nb_ETP = jsonmessage['nb_ETP']
        for a in argument:
            currentdecision.argument.add(Argument.objects.get(pk=a))
        currentdecision.save()  # important: save to DB! The timestamp is automatically set when saving


# Connected to websocket.disconnect for players
def ws_disconnect(message, group_name):
    print("*********DISCONNECT************")
    channelsGroup(group_name).discard(message.reply_channel)


#############################################
#############################################
# Connected to websocket.connect for experts
def ws_experts_connect(message):
    print("*********CONNECT************")
    channelsGroup("EXPERTS").add(message.reply_channel)

# Connected to websocket.receive for experts
def ws_experts_message(message):
    print("*********RECEIVE************")
    # Decrypt the received message
    jsonmessage = json.loads(message.content['text'])

# Connected to websocket.disconnect for experts
def ws_experts_disconnect(message):
    print("*********DISCONNECT************")
    channelsGroup("EXPERTS").discard(message.reply_channel)

