

from django import template
from django.contrib.auth.decorators import login_required

register = template.Library()

@register.simple_tag
def suggest_friends(request):
    user = request.user
    sg = {}
    for i in user.user_profile.follow.all():
        if sg.get(i,None)==None:
            sg[i] = 0
            for j in i.user_profile.follow.all():
                if sg.get(j,None)==None:
                    sg[j] = 0
                sg[j]+=1
        sg[i]+=1
    sglist = sorted(list(sg.keys()),key=lambda x:sg[x], reverse=True)[:10]
    return sglist
