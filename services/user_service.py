from py2neo import Graph
from bcrypt import *
from utilities.query_for_services import *

graph = Graph()


def create_user(user):
    password_hashed = hashpw(user.get('password').encode(), gensalt(10))

    return \
        graph.run(query_create_user(user.get('username'), password_hashed.decode(), user.get('name'))).data()[
            0].get('id')


def get_user_info(user_id):
    return graph.run(query_get_user_info(user_id)).data()[0]


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

# print(create_objective_career(4263, 214))

# create_user_has_lo(4261, [{'id': 116, 'type': 'tool', 'level': 1}])
# create_user_need_lo(4262)
