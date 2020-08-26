from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.


def list_users(request):
    userObject = request.user
    users = User.objects.all().exclude(username=userObject.username)
    context = {
        "users":users,
    }
    return render(request, "users/list.html", context=context)

