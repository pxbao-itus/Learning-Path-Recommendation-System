import sys
from py2neo import Graph

from utilities import query_for_algorithm, query_algorithm_v2
from algorithm_v2 import step2, step1

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
    return graph.run(
        query_algorithm_v2.find_paths_from_sources_to_targets(sources, targets, user_id, 10)).data()


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


def add_list_to_list(native_list, added_list):
    for element in added_list:
        if element in native_list:
            continue
        else:
            native_list.append(element)


def add_list_to_front_list(native_list, added_list):
    copy_native_list = native_list.copy()
    native_list.clear()
    native_list.extend(added_list)
    for element in copy_native_list:
        if element in native_list:
            native_list.remove(element)
            native_list.append(element)
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
            if i == path1[0] or i == path2[0]:
                continue
            else:
                return i
    return 0


def is_two_list_different(list1, list2):
    if list1.__len__() != list2.__len__():
        return False
    for i in range(list2.__len__()):
        if list1[i] != list2[i]:
            return False
    return True


def find_except_node(path_final):
    except_node = []
    for path in path_final:
        except_node.extend(path)
    return except_node


def get_target_common_source_path_two_element(paths, source, targets):
    targets_return = []
    sources_return = []
    for path in paths:
        if source in path and path.__len__() == 2:
            add_list_to_list(targets_return, [path[1]])
    paths_removed = []
    for target in targets_return:
        if [source, target] in paths:
            paths.remove([source, target])
        for path in paths:
            if path.__len__() == 2 and path[1] == target:
                paths_removed.append(path)
                add_list_to_list(sources_return, [path[0]])
            elif path[path.__len__() - 1] == target and path[0] == source:
                targets.append(path[path.__len__() - 2])
                paths_removed.append(path)
                paths.append(path[1:path.__len__() - 1])
            elif path[path.__len__() - 1] == target:
                targets.append(path[path.__len__() - 2])
                paths_removed.append(path)
                paths.append(path[0:path.__len__() - 1])
        if target in targets:
            targets.remove(target)
    for path_removed in paths_removed:
        paths.remove(path_removed)
    paths_removed.clear()
    for path in paths:
        if path[0] == source:
            target_removed = path[path.__len__() - 1]
            targets.remove(target_removed)
            for inner_path in paths:
                if inner_path[0] != source and target_removed in inner_path and inner_path.__len__() > 2 and not \
                        inner_path[0] in targets_return:
                    paths.append(inner_path[0:inner_path.__len__() - 1])
                    targets.append(inner_path[inner_path.__len__() - 2])
                    paths_removed.append(inner_path)
            add_list_to_list(targets_return, path[1:path.__len__()])
            paths_removed.append(path)
    for path_removed in paths_removed:
        paths.remove(path_removed)
    return sources_return + targets_return


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
        path_added.extend(path_check)
        path_final.append(path_added)
        paths.remove(path_check)
        return
    sources = []
    for path_chosen in paths_have_common_node:
        sources.append(path_chosen[0])
    sources = list(set(sources))
    path_added = []
    for source in sources:
        path_added.extend(hash_map.get(source))
    for path in paths_have_common_node:
        if common_node != 0 and common_node in path:
            add_list_to_list(path_added, path[0:path.index(common_node)])
    new_hash_map[common_node] = path_added


def create_path_final(path_final, sources, targets, hash_map, user_id):
    if sources.__len__() == 0:
        return
    for target in targets:
        if is_in_path_final(target, path_final):
            targets.remove(target)
    for source in sources:
        if is_in_path_final(source, path_final):
            sources.remove(source)
    paths = find_distinct_path(find_path_source_target(sources, targets, user_id))
    new_hash_map = {}
    for path in paths:
        if path.__len__() == 2:
            source = path[0]
            targets_returned = get_target_common_source_path_two_element(paths, source, targets)
            path_added = hash_map.get(source) + [source] + targets_returned
            path_final.append(path_added)
    for path in paths:
        handle_path(paths, path, hash_map, path_final, new_hash_map)
    create_path_final(path_final, list(new_hash_map.keys()), targets, new_hash_map, user_id)


def get_final_result(user_id):
    set_courses = step2.get_input_for_step3(user_id)
    paths = []
    for set_course in set_courses:
        set_course = list(set(set_course))
        remove_label()
        remote_relationship_btw_courses()
        add_new_label(set_course)
        create_relationship_btw_courses(set_course)
        create_sub_graph(user_id)
        path_final = []
        single_nodes = get_list_id(find_single_nodes())
        for node in single_nodes:
            path_final.append([node])
        source_nodes = get_list_id(find_source_nodes())
        target_nodes = get_list_id(find_target_nodes())
        hash_map = {}
        for node in source_nodes:
            hash_map[node] = []
        create_path_final(path_final, source_nodes, target_nodes, hash_map, user_id)
        paths.append(path_final.copy())
        remove_sub_graph(user_id)
        remove_label()
        remote_relationship_btw_courses()
    return paths


def is_in_path_final(node, path_final):
    for outer in path_final:
        for inner in outer:
            if node == inner:
                return True
    return False
# get_final_result(52)
# get_final_result(5)
# print(step2.get_input_for_step3(13))
