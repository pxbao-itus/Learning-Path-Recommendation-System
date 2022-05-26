import itertools

from concurrent.futures.thread import ThreadPoolExecutor
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


# create descartes set courses
def make_descartes_set(user_id, user_lo_require, user_lo_current_require):
    sets_courses = []
    list_course_per_lo = optimize_candidate_courses_step1.get_set_candidate_for_all_lo(user_lo_require,
                                                                                       user_lo_current_require)

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
        user_lo_current_require.clear()
        user_lo_current_require = get_user_lo_current_require(set_course, user_lo_require, user_lo_current_require)
        if user_lo_current_require.__len__() == 0:
            set_complete_course.append(user_course_extra.copy())
            abc = user_course_extra.pop()
            cde = user_lo_require.pop()
            continue
        else:
            complete_set_course(make_descartes_set(user_id, user_lo_require, user_lo_current_require), user_id,
                                user_course_extra, user_lo_require, user_lo_current_require, set_complete_course)
    if user_course_extra.__len__() > 0:
        user_course_extra.pop()

import time

start_time = time.time()
total = []
complete_set_course(optimize_candidate_courses_step1.get_input_for_step2(4248), 4248, [],
                             [optimize_candidate_courses_step1.get_user_lo(4248)], [], total)
deco_list = []
for set_raw in total:
    element = []
    for e in set_raw:
        element.extend(e)
    # print(element)
    deco_list.append(element.copy())
# for i in deco_list:
#     print(i)
print(deco_list.__len__())
print("--- %s seconds ---" % (time.time() - start_time))
