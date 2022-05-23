from concurrent.futures.thread import ThreadPoolExecutor

from py2neo import Graph

from utilities.query_for_algorithm import *
from constants.algorithm_constants import *

graph = Graph()


# print(graph.run(
#     'match (u:User{name:"Bob"})-[r]->(lo) where type(r) =~"NE.*"return r.Level as level, lo.value as value').data())


# get list LO that user need
def get_user_lo_need(user_id):
    return graph.run(query_get_user_need_lo(user_id)).data()


# checking lo belong or not a set lo
def is_lo_belong_set_lo(set_lo, lo_dict):
    for lo in set_lo:
        if lo.get('id') == lo_dict.get('id') and lo.get('level') >= lo_dict.get('level'):
            return True
        else:
            continue
    return False


def is_inside_set_lo(set_lo, lo_dict):
    for lo in set_lo:
        if lo.get('id') == lo_dict.get('id'):
            return True
        else:
            continue
    return False


# checking for a course that is or not satisfy first criteria
def is_course_provided_more_than_one_lo(list_lo, lo_dict, user_lo_need):
    result = False
    if list_lo.__len__() < 2:
        return False
    for lo in list_lo:
        if lo_dict.get('id') != lo.get('id') and is_lo_belong_set_lo(user_lo_need, lo):
            result = True
    return result


# checking for a course that is or not satisfy second criteria
def is_require_lo_of_course_belonged(course_id, user_lo_need):
    counter = 0
    list_require_lo = graph.run(query_get_input_lo_of_a_course(course_id)).data()
    for lo in list_require_lo:
        if is_lo_belong_set_lo(user_lo_need, lo):
            counter += 1
    if counter == list_require_lo.__len__():
        return True
    else:
        return False


# checking for a course that is or not satisfy third criteria
def is_output_lo_of_course_less_or_equal_than_delta(user_lo_need, list_lo_provided_by_course):
    counter = 0
    for lo in list_lo_provided_by_course:
        if is_inside_set_lo(user_lo_need, lo):
            continue
        else:
            counter += 1
    if counter <= AlgorithmConstant.DELTA:
        return True
    else:
        return False


# checking for a course that is or not satisfy fourth criteria
def is_input_lo_of_course_outside_less_or_equal_than_alpha(course_id, user_lo_need):
    counter = 0
    list_require_lo = graph.run(query_get_input_lo_of_a_course(course_id)).data()
    for lo in list_require_lo:
        if is_lo_belong_set_lo(user_lo_need, lo):
            continue
        else:
            counter += 1
    if counter <= AlgorithmConstant.ALPHA:
        return True
    else:
        return False


# checking for a course that is or not satisfy fifth criteria
def is_amount_level_redundancy_less_than_beta(lo_dict, list_lo_provided_by_course):
    amount = 0
    for lo in list_lo_provided_by_course:
        if lo.get('id') == lo_dict.get('id'):
            amount = lo.get('level') - lo_dict.get('level')
            break;
    if amount <= AlgorithmConstant.BETA:
        return True
    else:
        return False


# checking for a course that is or not satisfy sixth criteria
def is_rating_for_course_greater_than_lambda(course_id):
    course = graph.run(query_get_rating_course(course_id)).data()
    for lo in course:
        if lo.get('rating') is not None and lo.get('rating') >= AlgorithmConstant.LAMBDA:
            return True
        else:
            return False


# checking for a course that satisfy criteria provide by user
def is_candidate_courses_a_LO(course_id, lo_dict, user_lo_need, criteria):
    list_lo_provided_by_course = graph.run(query_get_lo_provided_by_course(course_id)).data()

    switcher = {
        1: is_course_provided_more_than_one_lo(list_lo_provided_by_course, lo_dict, user_lo_need),
        2: is_require_lo_of_course_belonged(course_id, user_lo_need),
        3: is_output_lo_of_course_less_or_equal_than_delta(user_lo_need, list_lo_provided_by_course),
        4: is_input_lo_of_course_outside_less_or_equal_than_alpha(course_id, user_lo_need),
        5: is_amount_level_redundancy_less_than_beta(lo_dict, list_lo_provided_by_course),
        6: is_rating_for_course_greater_than_lambda(course_id)
    }
    return switcher.get(criteria, True)


# get candidate courses for a lo
def get_list_candidate_courses_for_a_lo(lo_dict, user_lo_need):
    course_lo = graph.run(query_get_courses_provided_a_lo(lo_dict.get('id'))).data()
    list_course_lo = []
    for i in range(7):
        for course in course_lo:
            if is_candidate_courses_a_LO(course.get('id'), lo_dict, user_lo_need, i + 1):
                list_course_lo.append(course)
        if list_course_lo.__len__() > 0:
            return list_course_lo
        else:
            continue


# get all candidate courses for all lo
def get_set_candidate_for_all_lo(user_id):
    user_lo_need = get_user_lo_need(user_id)
    list_courses_all_lo = []
    list_future_for_thread = []
    executor = ThreadPoolExecutor(user_lo_need.__len__())
    for lo in user_lo_need:
        list_future_for_thread.append(executor.submit(get_list_candidate_courses_for_a_lo, lo, user_lo_need))
    executor.shutdown()
    for future in list_future_for_thread:
        list_courses_all_lo.append(future.result())
    return list_courses_all_lo


print(get_set_candidate_for_all_lo(4248))
