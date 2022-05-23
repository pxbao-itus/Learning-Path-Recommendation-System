from py2neo import Graph

graph = Graph()
from utilities.query_for_algorithm import *


def check_criteria_one(list_lo, lo_id):
    result = False
    if list_lo.__len__() < 2:
        return False
    for lo in list_lo:
        if lo_id == lo.get('id'):
            result = True
    return result




def optimize_candidate_courses_a_LO(course_id, user_id, lo_id):
    query = get_lo_provided_by_course(course_id, user_id)
    list_lo = graph.run(query).data()
    print(list_lo)
    print(check_criteria_one(list_lo, lo_id))


optimize_candidate_courses_a_LO(3575, 4248, 98)
