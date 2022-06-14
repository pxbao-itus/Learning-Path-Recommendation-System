from py2neo import Graph

from algorithm_implementation import build_learning_path_step4, evaluate_set_courses_step3, \
    optimize_candidate_courses_step1
from models.user import User
from utilities.query_for_services import *
from services import igraph_service

graph = Graph()


def create_user(user):
    return graph.run(query_create_user(user.get('name'), user.get('email'), user.get('cost'), user.get('time'))).data()


def get_user_info(user_id):
    result = graph.run(query_get_user_info(user_id)).data()
    if result.__len__() > 0:
        career = graph.run(query_get_objective(user_id)).data()
        if career.__len__() > 0:
            print(career)
            result[0]['career'] = career[0].get('id')
        else:
            result[0]['career'] = 0
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


def delete_user_need_lo(user_id):
    graph.run(query_delete_relationship_user_need_lo(user_id))


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
        igraph_service.visualize_learning_path(path, counter)
        element["visualization"] = f'/static/learning-path-{counter}.png'
        result.append(element.copy())
        counter += 1
    delete_user_need_lo(user_id)

    return result
