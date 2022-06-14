from models.models import Career
from py2neo import Graph
from utilities.query_for_services import *

all_career = Career.nodes.all()

graph = Graph()

def get_all_career():
    list_career = []
    for i in all_career:
        list_career.append(i.to_json_1())
    return list_career


def get_career_by_id(career_id):
    return Career.get_one(career_id).to_json_1()


def get_lo_career_need(career_id):
    return graph.run(query_get_lo_need_by_career(career_id)).data()
