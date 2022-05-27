from concurrent.futures.thread import ThreadPoolExecutor
from py2neo import Graph
from operator import itemgetter

from utilities.query_for_algorithm import *
from constants.algorithm_constants import *
import finding_set_courses_step2

graph = Graph()


def count_amount_course_in_a_set_course(set_course):
    return set_course.__len__()


def get_list_id(list):
    list_id = []
    for item in list:
        list_id.append(item.get('id'))
    return list_id.copy()


def count_amount_level_redundant(set_course, user_lo_need, lo_need_just_an_id):
    counter = 0
    course_lo_provide = []
    lo_need_just_an_id = []
    # for lo in user_lo_need:
    #     lo_need_just_an_id.append(lo.get('id'))
    course_lo_provide = graph.run(query_to_get_list_lo_provided_by_set_course(set_course_id))
    # for course_lo in course_lo_provide:

# def find_lo_provide_by_set_course(set_course, user_id):


# abc = [{'id': 1}, {'id': 2}, {'id': 3}]
# print(list(map(itemgetter(0), abc.__getitem__('id'))))
