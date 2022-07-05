from py2neo import Graph
from utilities.query_for_services import *
from utilities.query_for_algorithm import *

graph = Graph()


def get_lo_provided_by_course(course_id):
    return graph.run(query_get_lo_provided_by_course(course_id)).data()


def get_lo_required_by_course(course_id):
    return graph.run(query_lo_require_a_course(course_id)).data()


def get_info_course(course_id):
    return graph.run(query_get_info_a_course(course_id)).data()[0]
