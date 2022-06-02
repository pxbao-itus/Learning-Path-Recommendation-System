import functools
from concurrent.futures.thread import ThreadPoolExecutor
from py2neo import Graph
from operator import itemgetter

from utilities.query_for_algorithm import *
from constants.algorithm_constants import *
from algorithm_implementation import finding_set_courses_step2

graph = Graph()


# count amount course in final set course
def count_amount_course_in_a_set_course(set_course):
    return list(set(get_list_id(set_course))).__len__()


# convert list dict to list id
def get_list_id(list_dict):
    return list(map(finding_set_courses_step2.map_list_dict_to_list, list_dict))


# count amount lo redundant
def count_amount_lo_redundant(set_course, user_lo_need):
    lo_provided = graph.run(query_to_get_list_lo_provided_by_set_course(get_list_id(set_course))).data()
    set_lo = list(set(get_list_id(lo_provided)))
    return set_lo.__len__() - user_lo_need.__len__()


def count_amount_level_redundant(set_course, user_lo_need):
    counter = 0
    lo_provided = graph.run(query_to_get_list_lo_provided_by_set_course(get_list_id(set_course))).data()

    for lo in user_lo_need:
        for lo_provided_element in lo_provided:
            if lo.get('id') == lo_provided_element.get('id'):
                counter += lo_provided_element.get('level') - lo.get('level')
                break
    return counter


def count_avg_evaluation_for_set_course(set_course):
    set_course_id = list(set(get_list_id(set_course)))
    avg_rating = graph.run(query_get_rating_set_course(set_course_id)).data()

    return avg_rating[0].get('avgRating') or 0


def count_sum_tuition_of_set_course(set_course):
    set_course_id = list(set(get_list_id(set_course)))
    sumFee = graph.run(query_get_sum_tuition_set_course(set_course_id)).data()

    return sumFee[0].get('sumFee') or 0


def count_sum_time_of_set_course(set_course):
    set_course_id = list(set(get_list_id(set_course)))
    list_time = graph.run(query_get_list_time_of_set_course(set_course_id)).data()
    total_time = 0

    for time in list_time:
        try:
            total_time += float(time.get('time')[0: time.get('time').find(" ")])
        except:
            total_time+= 0

    return total_time


def evaluate_a_set_course(set_course, user_lo_need):
    return {
        'set_course': set_course,
        'point': AlgorithmConstant.F1 * count_amount_course_in_a_set_course(set_course)
                 + AlgorithmConstant.F2 * count_amount_lo_redundant(set_course, user_lo_need)
                 + AlgorithmConstant.F3 * count_amount_level_redundant(set_course, user_lo_need)
                 + AlgorithmConstant.F4 * count_avg_evaluation_for_set_course(set_course)
                 + AlgorithmConstant.F5 * count_sum_tuition_of_set_course(set_course)
                 + AlgorithmConstant.F6 * count_sum_time_of_set_course(set_course)
    }


def for_evaluating(e):
    return e.get('point')


def get_top_course_to_step_4(user_id):
    user_lo_need = graph.run(query_get_user_need_lo(user_id)).data()
    set_course_complete = finding_set_courses_step2.parse_for_step3_input(user_id)
    set_course_evaluation = []
    for set_course in set_course_complete:
        set_course_evaluation.append(evaluate_a_set_course(set_course, user_lo_need))
    set_course_evaluation.sort(key=for_evaluating, reverse=False)

    set_unique_course = []
    set_course_returned = []
    counter = 0
    for course in set_course_evaluation:
        tem = list(set(get_list_id(course.get('set_course'))))
        if tem not in set_unique_course:
            set_unique_course.append(tem.copy())
        else:
            continue
    for course in set_unique_course:
        counter += 1
        set_course_returned.append(course)
        if counter >= AlgorithmConstant.OMEGA:
            break
        else:
            continue
    return set_course_returned

# print(get_top_course_to_step_4(4248))
