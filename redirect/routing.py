from channels.routing import include
from channels.routing import route
from ebay.consumers import ws_message as ebay_ws_message,\
    ws_connect as ebay_ws_connect,\
    ws_disconnect as ebay_ws_disconnect
from ostende.consumers import ws_experts_message as ostende_ws_experts_message,\
    ws_experts_connect as ostende_ws_experts_connect,\
    ws_experts_disconnect as ostende_ws_experts_disconnect
from ostende.consumers import ws_message as ostende_ws_message,\
    ws_connect as ostende_ws_connect, \
    ws_disconnect as ostende_ws_disconnect
from otree.channels.routing import channel_routing
from primo_fmr.consumers import ws_experts_message as primo_fmr_ws_experts_message,\
    ws_experts_connect as primo_fmr_ws_experts_connect,\
    ws_experts_disconnect as primo_fmr_ws_experts_disconnect
from primo_fmr.consumers import ws_message as primo_fmr_ws_message,\
    ws_connect as primo_fmr_ws_connect, \
    ws_disconnect as primo_fmr_ws_disconnect
from vote_1_tour.consumers import ws_message as vote_1_tour_ws_message,\
    ws_connect as vote_1_tour_ws_connect, \
    ws_disconnect as vote_1_tour_ws_disconnect
from vote_2_tours.consumers import ws_message as vote_2_tours_ws_message,\
    ws_connect as vote_2_tours_ws_connect, \
    ws_disconnect as vote_2_tours_ws_disconnect
from vote_approbation.consumers import ws_message as vote_approbation_ws_message,\
    ws_connect as vote_approbation_ws_connect, \
    ws_disconnect as vote_approbation_ws_disconnect

#################################################
# Sockets for ebay application
ebay_routing = [route("websocket.connect",
                      ebay_ws_connect,  path=r'^/(?P<group_name>\w+)$'),
                route("websocket.receive",
                      ebay_ws_message,  path=r'^/(?P<group_name>\w+)$'),
                route("websocket.disconnect",
                      ebay_ws_disconnect,  path=r'^/(?P<group_name>\w+)$'), ]


#################################################
# Sockets for primo_fmr application
primo_fmr_routing = [route("websocket.connect",
                           primo_fmr_ws_connect,  path=r'^/(?P<group_name>\w+)/(?P<question>\w+)$'),
                     route("websocket.receive",
                           primo_fmr_ws_message,  path=r'^/(?P<group_name>\w+)/(?P<question>\w+)$'),
                     route("websocket.disconnect",
                           primo_fmr_ws_disconnect,  path=r'^/(?P<group_name>\w+)/(?P<question>\w+)$'), ]
primo_fmr_routing_experts = [route("websocket.connect",
                                   primo_fmr_ws_experts_connect),
                             route("websocket.receive",
                                   primo_fmr_ws_experts_message),
                             route("websocket.disconnect",
                                   primo_fmr_ws_experts_disconnect), ]


#################################################
# Sockets for ostende application
ostende_routing = [route("websocket.connect",
                         ostende_ws_connect,  path=r'^/(?P<group_name>\w+)$'),
                   route("websocket.receive",
                         ostende_ws_message,  path=r'^/(?P<group_name>\w+)$'),
                   route("websocket.disconnect",
                         ostende_ws_disconnect,  path=r'^/(?P<group_name>\w+)$'), ]
ostende_routing_experts = [route("websocket.connect",
                                 ostende_ws_experts_connect),
                           route("websocket.receive",
                                 ostende_ws_experts_message),
                           route("websocket.disconnect",
                                 ostende_ws_experts_disconnect), ]


#################################################
# Sockets for vote_1_tour application
vote_1_tour_routing = [route("websocket.connect", vote_1_tour_ws_connect),
                       route("websocket.receive", vote_1_tour_ws_message),
                       route("websocket.disconnect", vote_1_tour_ws_disconnect), ]


#################################################
# Sockets for vote_1_tour application
vote_2_tours_routing = [route("websocket.connect", vote_2_tours_ws_connect),
                        route("websocket.receive", vote_2_tours_ws_message),
                        route("websocket.disconnect", vote_2_tours_ws_disconnect), ]


#################################################
# Sockets for vote_approbation application
vote_approbation_routing = [route("websocket.connect", vote_approbation_ws_connect),
                        route("websocket.receive", vote_approbation_ws_message),
                        route("websocket.disconnect", vote_approbation_ws_disconnect), ]


#################################################
#################################################
channel_routing += [
    include(ebay_routing, path=r"^/ebay"),
    include(primo_fmr_routing, path=r"^/primo_fmr"),
    include(primo_fmr_routing_experts, path=r"^/primo_fmr/expertchannel"),
    include(ostende_routing, path=r"^/ostende"),
    include(ostende_routing_experts, path=r"^/ostende/expertchannel"),
    include(vote_1_tour_routing, path=r"^/vote_1_tour/director"),
    include(vote_2_tours_routing, path=r"^/vote_2_tours/director"),
    include(vote_approbation_routing, path=r"^/vote_approbation/director"),
]
