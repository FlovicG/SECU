from django.http import HttpResponse, HttpResponseRedirect


#################################
def get_livetree_redir(request):
    if request.session.get("otree"):
        ofi = open('./redirect/sessionState.txt', 'r')
        session_state = ofi.read()
        ofi.close()
        if session_state=="running":
            cookie_val = request.session["otree"]
            return HttpResponseRedirect(cookie_val)
        else:
            return HttpResponseRedirect('http://otree.univ-catholille.fr/room/Anthropo_Field_Open/')
    else:
        return HttpResponseRedirect('http://otree.univ-catholille.fr/room/Anthropo_Field_Open/')


#################################
def get_eli_redir(request):
    if request.session.get("otree"):
        ofi = open('./redirect/sessionState.txt', 'r')
        session_state = ofi.read()
        ofi.close()
        if session_state=="running":
            cookie_val = request.session["otree"]
            return HttpResponseRedirect(cookie_val)
        else:
            return HttpResponseRedirect('http://otree.univ-catholille.fr/room/Anthropo_Lab/')
    else:
        return HttpResponseRedirect('http://otree.univ-catholille.fr/room/Anthropo_Lab/')


#################################
def get_eth_redir(request):
    if request.session.get("otree"):
        ofi = open('./redirect/sessionState.txt', 'r')
        session_state = ofi.read()
        ofi.close()
        if session_state=="running":
            cookie_val = request.session["otree"]
            return HttpResponseRedirect(cookie_val)
        else:
            return HttpResponseRedirect('http://otree.univ-catholille.fr/room/Anthropo_Field_Open/')
    else:
        return HttpResponseRedirect('http://otree.univ-catholille.fr/room/Anthropo_Field_Open/')


#################################
def get_test_redir(request):
    return HttpResponseRedirect('http://otree.univ-catholille.fr/room/Anthropo_Field_Open/')


#################################
def get_sensdutravail_vert_redir(request):
    if request.session.get("otree"):
        cookie_val = request.session["otree"]
        return HttpResponseRedirect(cookie_val)
    else:
        ofi = open('./redirect/url_vert.txt', 'r')
        url_vert = ofi.read()
        ofi.close()
        return HttpResponseRedirect(url_vert)


#################################
def get_sensdutravail_rouge_redir(request):
    if request.session.get("otree"):
        cookie_val = request.session["otree"]
        return HttpResponseRedirect(cookie_val)
    else:
        ofi = open('./redirect/url_rouge.txt', 'r')
        url_rouge = ofi.read()
        ofi.close()
        return HttpResponseRedirect(url_rouge)


c_rooms = [
    'http://otree.univ-catholille.fr/room/Anthropo_Field_Open/',
    'http://otree.univ-catholille.fr/room/Anthropo_Field_Open_2/',
    'http://otree.univ-catholille.fr/room/Anthropo_Field_Open_3/',
]
#################################
def get_room_redir(request):
    ofi = open('./redirect/rooms.txt', 'r')
    text = ofi.read()
    ofi.close()
    if text=="closed":
        return HttpResponse("Désolé, ce lien ne sera activé que lorsque l'expérience commencera")
    else:
        index = int(text)
        return HttpResponseRedirect(c_rooms[index])
