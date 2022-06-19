from py2neo import Graph

from utilities import query_for_algorithm, query_algorithm_v2
from constants.algorithm_constants import AlgorithmConstant

graph = Graph()


def get_list_id(list_dictionary):
    list_id = []
    for dict_element in list_dictionary:
        list_id.append(dict_element.get('id'))
    return list_id


def add_new_label(courses):
    graph.run(query_algorithm_v2.add_new_label_for_courses_selected(courses))


def remove_label():
    graph.run(query_algorithm_v2.remove_label_selected())


def create_relationship_btw_courses(courses):
    graph.run(query_algorithm_v2.create_relationship_btw_courses_selected(courses))


def remote_relationship_btw_courses():
    graph.run(query_algorithm_v2.remove_relationship_btw_courses())


def create_sub_graph(user_id):
    graph.run(query_algorithm_v2.create_sub_graph_from_list_courses(user_id))


def remove_sub_graph(user_id):
    graph.run(query_algorithm_v2.remove_sub_graph(user_id))


def find_single_nodes():
    return graph.run(query_algorithm_v2.find_single_nodes_inside_sub_graph()).data()


def find_source_nodes():
    return graph.run(query_algorithm_v2.find_source_nodes_inside_sub_graph()).data()


def find_target_nodes():
    return graph.run(query_algorithm_v2.find_target_node_inside_sub_graph()).data()


def find_path_source_target(sources, targets, user_id):
    return graph.run(query_algorithm_v2.find_paths_from_sources_to_targets(sources, targets, user_id, 10)).data()


def check_existed_path_in_paths(paths, path_checked):
    for path in paths:
        if path.get('sourceNodeName') == path_checked.get('sourceNodeName') \
                and path.get('targetNodeName') == path_checked.get('targetNodeName') \
                and path.get('totalCost') == path_checked.get('totalCost'):
            return True
    return False


def find_distinct_path(paths):
    paths_distinct = []
    for path in paths:
        path_selected = path
        for path_compare in paths:
            if path.get('sourceNodeName') == path_compare.get('sourceNodeName') \
                    and path.get('targetNodeName') == path_compare.get('targetNodeName') \
                    and path.get('totalCost') < path_compare.get('totalCost'):
                path_selected = path_compare.copy()
        if check_existed_path_in_paths(paths_distinct, path_selected):
            continue
        else:
            paths_distinct.append(path_selected)
    path_returned = []
    for path in paths_distinct:
        path_returned.append(path.get('nodeNames'))
    return path_returned


# def check_same_element_in_two_list(list1, list2):
#     for element in list1:

def get_target_common_source_path_two_element(paths, source, targets):
    targets_return = []
    for path in paths:
        if source in path and path.__len__() == 2:
            targets_return.append(path[1])
    for target in targets_return:
        paths.remove([source, target])
        targets.remove(target)
    return targets_return


def add_list_to_list(native_list, added_list):
    for element in added_list:
        if element in native_list:
            continue
        else:
            native_list.append(element)


def is_common_node_in_two_paths(path1, path2):
    for i in path1:
        if i in path2:
            return True
    return False


def get_common_node(path1, path2):
    for i in path1:
        if i in path2:
            return i
    return 0


def is_two_list_different(list1, list2):
    if list1.__len__() != list2.__len__():
        return False
    for i in range(list2.__len__()):
        if list1[i] != list2[i]:
            return False
    return True


def handle_path(paths, path_check, hash_map, path_final, new_hash_map):
    paths_have_common_node = [path_check]
    common_node = 0
    for path in paths:
        if not is_two_list_different(path_check, path) and is_common_node_in_two_paths(path_check, path):
            if common_node == 0:
                common_node = get_common_node(path_check, path)
                paths_have_common_node.append(path.copy())
            elif get_common_node(path_check, path) == common_node:
                paths_have_common_node.append(path.copy())

    if paths_have_common_node.__len__() == 1:
        path_added = hash_map.get(path_check[0])
        path_added.append(path_check)
        path_final.extend(path_added)
        paths.remove(path_check)
        return
    sources = []
    # print(paths_have_common_node)
    for path_chosen in paths_have_common_node:
        sources.append(path_chosen[0])
    sources = list(set(sources))
    path_added = []
    for source in sources:
        path_added.extend(hash_map.get(source))
    for path in paths_have_common_node:
        add_list_to_list(path_added, path[0:path.index(common_node)])
    new_hash_map[common_node] = path_added


def create_path_final(path_final, sources, targets, hash_map, user_id):
    if sources.__len__() == 0:
        return
    paths = find_distinct_path(find_path_source_target(sources, targets, user_id))
    # paths = [[272, 282, 316, 323], [287, 262], [302, 311, 316, 323], [335, 350, 403], [335, 350, 427],
    #          [361, 340, 350, 403], [361, 340, 350, 427]]
    new_hash_map = {}
    for path in paths:
        if path.__len__() == 2:
            source = path[0]
            path_added = get_target_common_source_path_two_element(paths, source, targets)
            path_added.append(source)
            path_added.extend(hash_map.get(source))
            path_added.reverse()
            path_final.append(path_added)
    for path in paths:
        handle_path(paths, path, hash_map, path_final, new_hash_map)
    create_path_final(path_final, list(new_hash_map.keys()), targets, new_hash_map, user_id)


def get_final_result(user_id):
    path_final = [get_list_id(find_single_nodes())]
    source_nodes = get_list_id(find_source_nodes())
    target_nodes = get_list_id(find_target_nodes())
    hash_map = {}
    for node in source_nodes:
        hash_map[node] = []
    create_path_final(path_final, source_nodes, target_nodes, hash_map, user_id)
    return path_final


# print(get_final_result(5))
