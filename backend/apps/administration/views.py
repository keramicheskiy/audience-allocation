from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models

# TODO ТУТ короче должен быть контроллер для супер-пупер админов, которые будут крудить эти модельки:

# class Organization(models.Model):

@api_view(["GET"])

def index_organizations(request):
    organizations = models.Organization.objects.all().order_by('name')
    return Response({"organizations": organizations})










