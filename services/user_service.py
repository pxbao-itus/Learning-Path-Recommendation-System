from py2neo import Graph

from algorithm_implementation import build_learning_path_step4, evaluate_set_courses_step3, \
    optimize_candidate_courses_step1
from models.user import User
from utilities.query_for_services import *
from services import igraph_service
from algorithm_v2.step3 import *
from algorithm_v2.step2 import *

graph = Graph()


def create_user(user, user_id):
    return graph.run(query_create_user(user_id, user.get('cost'), user.get('time'))).data()


def register(name, email):
    result = login(email)
    print(result)
    if result.get("id") == 0:
        return graph.run(query_register(name, email)).data()
    else:
        return {}


def update(user_id, career_id):
    graph.run(query_update_career(user_id, career_id))
    graph.run(query_create_objective_career(user_id, career_id))


def login(email):
    result = graph.run(query_get_id_by_email(email)).data()
    if result.__len__() > 0:
        return result[0]
    else:
        return {"id": 0}


def get_user_info(user_id):
    result = graph.run(query_get_user_info(user_id)).data()
    if result.__len__() > 0:
        career = graph.run(query_get_objective(user_id)).data()
        if career.__len__() > 0:
            result[0]['career'] = career[0]
        else:
            result[0]['career'] = {}
        return User(result[0])
    else:
        return False


def create_objective_career(user_id, career_id):
    try:
        return graph.run(query_create_objective_career(user_id, career_id)).data()[0].get('id')
    except:
        return 0


# structure of a lo like {'id':123, 'type':'knowledge', 'level': 1}
def create_user_has_lo(user_id, list_lo):
    for lo in list_lo:
        graph.run(query_create_has_lo(user_id, lo))


def create_user_need_lo(user_id):
    list_relationship_id = []
    for query in query_create_user_need_lo(user_id):
        result = graph.run(query).data()
        # if result.__len__() > 0:
        #     list_relationship_id.append(result[0].get('id'))
    # print(list_relationship_id)


# create_user_need_lo(5)
def delete_user_need_lo(user_id):
    graph.run(query_delete_relationship_user_need_lo(user_id))


# delete_user_need_lo(5)
def get_learning_path(user_id):
    user = User(graph.run(query_get_user_info(user_id)).data()[0])
    delete_user_need_lo(user_id)
    create_user_need_lo(user_id)
    lb = build_learning_path_step4.completing_step4(user)
    result = []
    counter = 1
    for path in lb:
        element = {}
        element["path"] = path
        igraph_service.visualize_learning_path_v1(get_course_name_by_id(path), counter)
        element["visualization"] = f'/static/learning-path-{counter}.png'
        result.append(element.copy())
        counter += 1
    delete_user_need_lo(user_id)

    return result


def map_list_dict_to_list(dict):
    return dict.get('name')


def get_list_name(list_dict):
    return list(map(map_list_dict_to_list, list_dict))


def get_course_name_by_id(set_course):
    list_name = graph.run(query_get_course_name_by_id(set_course)).data()
    list_name = get_list_name(list_name)
    return list_name


def get_lo_need_by_user(user_id):
    user_lo = graph.run(query_get_lo_user_has(user_id)).data()
    career_lo = graph.run(query_get_lo_need_by_career_by_user_id(user_id)).data()
    lo_user_need = []
    for lo_career in career_lo:
        check = True
        for lo_user in user_lo:
            if lo_user.get('id') == lo_career.get('id') and lo_user.get('level') >= lo_career.get('level'):
                check = False
        if check:
            lo_user_need.append(lo_career.copy())
    return lo_user_need


def get_learning_path_v2(user_id):
    # user = User(graph.run(query_get_user_info(user_id)).data()[0])
    delete_user_need_lo(user_id)
    create_user_need_lo(user_id)
    paths = get_final_result(user_id)
    result = []
    counter = 1
    for path in paths:
        element = {}
        element["path"] = path
        igraph_service.visualize_learning_path_v2(path, counter)
        element["visualization"] = f'/static/learning-path-{counter}.png'
        result.append(element.copy())
        counter = counter + 1
    delete_user_need_lo(user_id)
    return result


def get_info_lp(courses, user_id):
    delete_user_need_lo(user_id)
    create_user_need_lo(user_id)
    result = {'course': calculate_number_of_course(courses),
              'lor': calculate_number_of_redundant_LO(courses, get_lo_need_by_user(user_id)),
              'lod': calculate_number_of_overlap_LO(courses),
              'time': calculate_sum_time_of_individual(courses),
              'cost': calculate_sum_cost_of_individual(courses)}
    delete_user_need_lo(user_id)
    return result

