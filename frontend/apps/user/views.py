from django.shortcuts import render

from ..teachers.decorators import logged_in


# Create your views here.

@logged_in
def profile(request):
    return render(request, "", context={"user": request.user})