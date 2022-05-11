from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from neomodel import db, StructuredNode, StringProperty, IntegerProperty

from Neo4j_Connection.models import Career

db.set_connection('bolt://neo4j:fit@hcmus@localhost:7687')


def allCareer(request):
    all_nodes = Career.nodes.all()
    return HttpResponse(all_nodes)
