import itertools

from py2neo import Graph
from utilities import query_for_algorithm, query_algorithm_v2
from constants.algorithm_constants import AlgorithmConstant
from models.candidate import Candidate

graph = Graph()


# get list id from list dictionary
def get_list_id(list_dictionary):
    list_id = []
    for dict_element in list_dictionary:
        list_id.append(dict_element.get('id'))
    return list_id


# get list course without similarity score
def get_courses_without_similarity(courses_with_similarity):
    courses_without_similarity = []
    for courses in courses_with_similarity:
        courses_without_similarity.append({'id': courses.get('id')})
    return courses_without_similarity


# find list lo that user need
def get_user_lo_need(user_id):
    return graph.run(query_algorithm_v2.query_get_user_need_lo(user_id)).data()


# find all candidate course for a lo
def find_candidate_for_lo(lo):
    return graph.run(query_algorithm_v2.query_get_courses_provided_a_lo(lo.get('id'), lo.get('level'))).data()


# get similarity score of all courses
def get_top_n_candidate(user_id, courses):
    return get_list_id(
        graph.run(query_algorithm_v2.query_get_top_courses_with_overlap_similarity(user_id, get_list_id(courses),
                                                                                   AlgorithmConstant.V2_MUY)).data())


# get los required by courses
def get_los_required_by_course(courses):
    los_required = []
    for course in courses:
        los_required.extend(graph.run(query_algorithm_v2.query_get_input_lo_of_a_course(course)).data())
    return los_required


# get candidate courses for all los required
def get_candidate_courses_all_los_required(user_id, los_required):
    candidate_courses = []
    for lo in los_required:
        candidate_courses.append(get_top_n_candidate(user_id, find_candidate_for_lo(lo)))
    return candidate_courses


# descartes candidate courses for sub los_required
def make_descartes_set_courses_by_descartes(candidate_courses):
    sets_courses = []
    candidate_top_n = []
    for candidate in candidate_courses:
        candidate_top_n.append(candidate[0:round(AlgorithmConstant.V2_MUY / 3)])
    for courses in itertools.product(*candidate_top_n):
        sets_courses.append(courses)
    sets_courses_as_list = []
    for i in sets_courses:
        sets_courses_as_list.append(list(i))
    return sets_courses_as_list


def map_list_dict_to_list(dictionary):
    return dictionary.get('id')


def create_temporary_relationship(user_id, user_lo_current_require):
    list_lo = get_list_id(user_lo_current_require)
    graph.run(query_for_algorithm.query_to_create_temporary_relationship_user_lo(user_id, list_lo))


def delete_temporary_relationship_created(user_id):
    graph.run(query_for_algorithm.query_to_remove_temporary_relationship_created(user_id))


# get complete candidate for a lo
def get_complete_candidate_for_a_lo(complete_candidates_courses, courses_extra, los_required, courses, user_id,
                                    user_lo_need):
    for course in courses:
        courses_extra.append(course.copy())
        delete_temporary_relationship_created(user_id)
        los_required.clear()
        los_required = get_los_required_by_course(course)
        if los_required.__len__() == 0:
            complete_candidates_courses.append(courses_extra.copy())
            courses_extra.pop()
            continue
        else:
            create_temporary_relationship(user_id, los_required)
            get_complete_candidate_for_a_lo(complete_candidates_courses, courses_extra, los_required,
                                            make_descartes_set_courses_by_descartes(
                                                get_candidate_courses_all_los_required(user_id, los_required)),
                                            user_id, user_lo_need)
    if courses_extra.__len__() > 0:
        courses_extra.pop()
    return


# make list to list of list
def list_to_list_of_list(list_single):
    list_of_list = []
    for single in list_single:
        list_of_list.append([single])
    return list_of_list


# get candidate courses for each lo
def get_candidate_for_all_lo(los, user_id):
    list_candidate_all_los = []
    for lo in los:
        complete_candidate_courses = []
        get_complete_candidate_for_a_lo(complete_candidate_courses, [], [],
                                        list_to_list_of_list(get_top_n_candidate(user_id, find_candidate_for_lo(lo))),
                                        user_id, get_user_lo_need(user_id))
        candidate_with_object = []
        for outer_course in complete_candidate_courses:
            content = []
            for inner_course in outer_course:
                content.extend(inner_course)
            candidate_with_object.append(Candidate(content, lo.get('id')))
        list_candidate_all_los.append(candidate_with_object)
    return list_candidate_all_los


def get_input_for_step2(user_id):
    return get_candidate_for_all_lo(get_user_lo_need(5), 5)

# structure of input for step 2
# [[obj, obj, obj], [obj, obj], [obj], [obj, obj, obj, obj, obj], ...]

# structure of object view in Candidate class in models package


# x = get_candidate_for_all_lo(get_user_lo_need(5), 5)
# for candidate_list in x:
#     for obj in candidate_list:
#         print(obj.get_value())
