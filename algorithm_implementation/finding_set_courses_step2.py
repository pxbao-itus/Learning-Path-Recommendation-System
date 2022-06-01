import itertools
from collections import Counter

from concurrent.futures.thread import ThreadPoolExecutor

import numpy as np
from py2neo import Graph

from utilities.query_for_algorithm import *
from constants.algorithm_constants import *
import optimize_candidate_courses_step1

graph = Graph()


# checking lo is inside in user_lo_require or user_lo_current_require
def is_inside_list_lo_existed(lo_dict, user_lo_require, user_lo_current_require):
    for set_lo in user_lo_require:
        for lo in set_lo:
            if lo.get('id') == lo_dict.get('id') \
                    and lo.get('level') is not None \
                    and lo_dict.get('level') is not None \
                    and lo.get('level') >= lo_dict.get('level'):
                return True
            else:
                continue
    for lo in user_lo_current_require:
        if lo.get('id') == lo_dict.get('id') \
                and lo.get('level') is not None \
                and lo_dict.get('level') is not None \
                and lo.get('level') >= lo_dict.get('level'):
            return True
        else:
            continue
    return False


# get lo require of a course with condition above
def get_lo_require_a_course(course_id, user_lo_require, user_lo_current_require):
    lo_require_per_course = graph.run(query_lo_require_a_course(course_id)).data()
    lo_require_per_course_returned = []
    for lo in lo_require_per_course:
        if is_inside_list_lo_existed(lo, user_lo_require, user_lo_current_require):
            continue
        else:
            lo_require_per_course_returned.append(lo)
    return lo_require_per_course_returned


# get set lo require of set course
def get_user_lo_current_require(set_course, user_lo_require, user_lo_current_require):
    for course in set_course:
        user_lo_current_require.extend(get_lo_require_a_course(course.get('id'),
                                                               user_lo_require,
                                                               user_lo_current_require))
    return user_lo_current_require.copy()


# create temporary relationship to calculate similarity
def map_list_dict_to_list(dict):
    return dict.get('id')


def create_temporary_relationship(user_id, user_lo_current_require):
    list_lo = list(map(map_list_dict_to_list, user_lo_current_require))
    graph.run(query_to_create_temporary_relationship_user_lo(user_id, list_lo))


def delete_temporary_relationship_created(user_id, user_lo_current_require):
    list_lo = list(map(map_list_dict_to_list, user_lo_current_require))
    graph.run(query_to_remove_temporary_relationship_created(user_id, list_lo))


# create descartes set courses
def make_descartes_set(user_id, user_lo_require, user_lo_current_require, user_course_extra):
    sets_courses = []
    list_course_per_lo = optimize_candidate_courses_step1.get_set_candidate_for_all_lo(user_lo_require,
                                                                                       user_lo_current_require, 0,
                                                                                       user_course_extra)

    list_course_per_lo = optimize_candidate_courses_step1.filter_list_not_none(list_course_per_lo)
    list_candidates_filtered = []

    for set_courses in list_course_per_lo:
        list_candidates_filtered.append(
            optimize_candidate_courses_step1.get_top_candidate_courses_of_a_lo(user_id, set_courses))

    for set_courses in itertools.product(*list_candidates_filtered):
        sets_courses.append(set_courses)

    sets_courses_as_list = []
    for i in sets_courses:
        sets_courses_as_list.append(list(i))
    return sets_courses_as_list


def complete_set_course(sets_courses, user_id, user_course_extra, user_lo_require, user_lo_current_require,
                        set_complete_course):
    for set_course in sets_courses:
        user_course_extra.append(set_course.copy())
        user_lo_require.append(user_lo_current_require.copy())
        delete_temporary_relationship_created(user_id, user_lo_current_require)
        user_lo_current_require.clear()
        user_lo_current_require = get_user_lo_current_require(set_course, user_lo_require, user_lo_current_require)
        if user_lo_current_require.__len__() == 0:
            set_complete_course.append(user_course_extra.copy())
            abc = user_course_extra.pop()
            cde = user_lo_require.pop()
            continue
        else:
            create_temporary_relationship(user_id, user_lo_current_require)
            complete_set_course(
                make_descartes_set(user_id, user_lo_require, user_lo_current_require, user_course_extra), user_id,
                user_course_extra, user_lo_require, user_lo_current_require, set_complete_course)
    if user_course_extra.__len__() > 0:
        user_course_extra.pop()


def parse_for_step3_input(user_id):
    total = []
    complete_set_course(optimize_candidate_courses_step1.get_input_for_step2(user_id, 1, []), user_id, [],
                        [optimize_candidate_courses_step1.get_user_lo(user_id)], [], total)
    parse_list = []
    for set_raw in total:
        element = []
        for e in set_raw:
            element.extend(e)
        if element not in parse_list:
            parse_list.append(element.copy())
        else:
            continue
    return parse_list

# lista = [[1, 2, 3], [1, 2, 4], [1, 2, 3]]
# set_list = []
# for element in lista:
#     if element not in set_list:
#         set_list.append(element.copy())
#     else:
#         continue
# print(set_list)

# print(parse_for_step3_input(4248).__len__())

# listb = [ 2, 3, 1, 2, 1, 5, 4, 4]
# print(set(listb))
