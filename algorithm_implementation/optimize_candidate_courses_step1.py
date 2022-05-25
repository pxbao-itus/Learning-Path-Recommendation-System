import itertools

from concurrent.futures.thread import ThreadPoolExecutor
from py2neo import Graph

from utilities.query_for_algorithm import *
from constants.algorithm_constants import *

graph = Graph()


# get list LO that user need
def get_user_lo_need(user_id):
    return graph.run(query_get_user_need_lo(user_id)).data()


# get list LO that user has and need
def get_user_lo(user_id):
    return graph.run(query_get_user_lo(user_id)).data()


# checking lo belong or not a set lo
def is_lo_belong_set_lo(set_lo, lo_dict):
    for lo in set_lo:
        if lo.get('id') == lo_dict.get('id') \
                and lo.get('level') is not None \
                and lo_dict.get('level') is not None \
                and lo.get('level') >= lo_dict.get('level'):
            return True
        else:
            continue
    return False


def is_inside_set_lo(set_lo, lo_dict):
    for lo in set_lo:
        if lo.get('id') == lo_dict.get('id') \
                and lo.get('level') is not None \
                and lo_dict.get('level') is not None:
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
def is_candidate_courses_a_LO(course_id, lo_dict, user_lo_need, user_lo, criteria):
    list_lo_provided_by_course = graph.run(query_get_lo_provided_by_course(course_id)).data()

    switcher = {
        1: is_course_provided_more_than_one_lo(list_lo_provided_by_course, lo_dict, user_lo_need),
        2: is_require_lo_of_course_belonged(course_id, user_lo),
        3: is_output_lo_of_course_less_or_equal_than_delta(user_lo, list_lo_provided_by_course),
        4: is_input_lo_of_course_outside_less_or_equal_than_alpha(course_id, user_lo_need),
        5: is_amount_level_redundancy_less_than_beta(lo_dict, list_lo_provided_by_course),
        6: is_rating_for_course_greater_than_lambda(course_id)
    }
    return switcher.get(criteria, True)


# get candidate courses for a lo
def get_list_candidate_courses_for_a_lo(lo_dict, user_lo_need, user_lo):
    course_lo = graph.run(query_get_courses_provided_a_lo(lo_dict.get('id'))).data()
    list_course_lo = []
    for i in range(7):
        for course in course_lo:
            if is_candidate_courses_a_LO(course.get('id'), lo_dict, user_lo_need, user_lo, i + 1):
                list_course_lo.append(course)
        if list_course_lo.__len__() > 0:
            return list_course_lo
        else:
            continue


# get all candidate courses for all lo
def get_set_candidate_for_all_lo(user_id):
    user_lo_need = get_user_lo_need(user_id)
    user_lo = get_user_lo(user_id)
    list_courses_all_lo = []
    list_future_for_thread = []
    executor = ThreadPoolExecutor(user_lo_need.__len__())
    for lo in user_lo_need:
        list_future_for_thread.append(executor.submit(get_list_candidate_courses_for_a_lo, lo, user_lo_need, user_lo))
    executor.shutdown()
    for future in list_future_for_thread:
        list_courses_all_lo.append(future.result())
    return list_courses_all_lo


# calculate similarity between a user and a course
def calculate_similarity_per_node_jaccard(user_id, course_id):
    return graph.run(query_calculate_similarity_jaccard(user_id, course_id)).data()[0].get('similarity')


def calculate_similarity_per_node_overlap(user_id, course_id):
    return graph.run(query_calculate_similarity_overlap(user_id, course_id)).data()[0].get('similarity')


# function for determine attribute similarity for sort in list
def for_sort(e):
    return e['similarity']


# function for remove element None in list
def filter_list_not_none(list_need_filtering):
    return [e for e in list_need_filtering if e not in [None]]


# reduce set candidate courses by get top n element hava higher similarity
def get_top_candidate_courses_of_a_lo(user_id, course_lo):
    if course_lo.__len__() < 3:
        return course_lo

    for course in course_lo:
        course['similarity'] = calculate_similarity_per_node_jaccard(user_id, course.get('id'))
    course_lo.sort(key=for_sort, reverse=True)

    for course in course_lo:
        course.pop('similarity')
    top_2_course = [course_lo[0], course_lo[1], course_lo[2]]
    return top_2_course


# transfer raw list to list is filtered by similarity
def get_input_for_step2(user_id):
    sets_courses = []
    list_course_per_lo = get_set_candidate_for_all_lo(user_id)

    list_course_per_lo = filter_list_not_none(list_course_per_lo)
    list_candidates_filtered = []

    for set_courses in list_course_per_lo:
        list_candidates_filtered.append(get_top_candidate_courses_of_a_lo(user_id, set_courses))

    # for set_courses in itertools.product(*list_candidates_filtered):
    #     sets_courses.append(set_courses)
    #
    # print(sets_courses)
    # print(list_candidates_filtered)
    return list_candidates_filtered


import time

start_time = time.time()
# get_input_for_step2(4248)
#get_input_for_step2(4248)
abc = get_input_for_step2(4248)
string = "Match (u:User{name:'Bob'})-[r]->(k)<-[r2]-(c:Course) Where type(r) =~ 'NEED_.*' and" \
         " type(r2) =~'TEACH_.*' and ("
for i in abc:
    for j in i:
        string += f" id(c)={j.get('id')} OR "
string += f" id(c) = {abc[0][0].get('id')}) return u, k, c"
print(string)
print("--- %s seconds ---" % (time.time() - start_time))
