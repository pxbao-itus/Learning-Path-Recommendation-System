def query_get_user_need_lo(user_id):
    return f"MATCH (u:User)-[r]->(k)" \
           f"WHERE ID(u) = {user_id} AND TYPE(r) =~ 'NEED_.*' " \
           f"RETURN id(k) as id, r.Level as level;"


# get set lo that user has and need
def query_get_user_lo(user_id):
    return f"MATCH (u:User)-[r]->(k) " \
           f"WHERE ID(u) = {user_id} AND (TYPE(r) =~ 'NEED_.*' OR TYPE(r) =~'HAS_.*') AND TYPE(r) <> 'HAS_OBJECTIVE' " \
           f"RETURN id(k) as id, r.Level as level;"


# get set LO that a course can provide
def query_get_lo_provided_by_course(course_id):
    query = 'MATCH (lo) <- [r2] - (c:Course) ' \
            f'WHERE id(c) = {course_id} ' \
            f'AND TYPE(r2) =~ "TEACH_.*" ' \
            f'RETURN id(lo) as id, r2.Level as level'
    return query


# get input LO of a course
def query_get_input_lo_of_a_course(course_id):
    return 'MATCH (c:Course)-[r]->(lo) ' \
           f'WHERE id(c) = {course_id} AND TYPE(r) =~ "REQUIRE_.*" ' \
           'RETURN id(lo) as id, r.Level as level'


# get set courses provided lo
def query_get_courses_provided_a_lo(lo_id, level):
    return f'MATCH (lo)<-[r]-(c:Course) ' \
           f'match (lo1)<-[r1]-(c1:Course)-[r2]->(lo1) ' \
           f'where type(r1) =~ "REQUIRE.*" and type(r2) =~ "TEACH.*" ' \
           f'with lo, c, r, collect(id(c1)) as except ' \
           f'WHERE id(lo) = {lo_id} and r.Level >= {level} and not id(c) in except ' \
           f'and type(r)=~"TEACH.*" return id(c) as id'


# get overlap similarity for user
def query_get_top_courses_with_overlap_similarity(user_id, courses, muy):
    return 'MATCH (p1:User)-[ru]-(e1) ' \
           f' where type(ru) <> "HAS_OBJECTIVE" and id(p1) = {user_id} ' \
           f'WITH p1, collect(id(e1)) AS p1entity_type , {courses} as courses ' \
           f'MATCH (p2:Course)-[rc]-(e2) ' \
           f'WHERE (type(rc) =~ "TEACH_.*" or type(rc) =~"REQUIRE_.*") and id(p2) in courses ' \
           'WITH p1, p1entity_type, p2, collect(id(e2)) AS p2entity_type ' \
           'WHERE gds.similarity.overlap(p1entity_type, p2entity_type) > 0 ' \
           'RETURN id(p2) as id, gds.similarity.overlap(p1entity_type, p2entity_type) AS similarity ' \
           'ORDER BY similarity DESC ' \
           f'LIMIT {muy}'


# ================= step 3 ========================

# add label for courses
def add_new_label_for_courses_selected(courses):
    return f'with {courses} as course ' \
           'match (c:Course) ' \
           'where id(c) in course ' \
           'set c:Selected; '


# remove label for courses
def remove_label_selected():
    return 'MATCH (n:Selected)' \
           'REMOVE n:Selected' \
           'RETURN n.name, labels(n);'


# create relationship between courses selected
def create_relationship_btw_courses_selected(courses):
    return f'with {courses} as courses ' \
           'match (c:Course)-[r]->(lo)<-[r1]-(c1:Course) ' \
           'where type(r) =~"REQUIRE.*" and type(r1) =~"TEACH.*"  and id(c) in courses ' \
           'and id(c1) in courses and id(c) <> id(c1) ' \
           'MERGE (c)-[:SELECTED{weight: 1}]->(c1); '


# remove relationship btw courses
def remove_relationship_btw_courses():
    return 'match ()-[r:SELECTED]->() ' \
           'delete r; '


# create sub graph
def create_sub_graph_from_list_courses(user_id):
    return 'CALL gds.graph.project( ' \
           f'"{user_id}", ' \
           '"Selected", ' \
           '"SELECTED", ' \
           '{nodeProperties: "id", relationshipProperties: "weight"})'


# remove sub graph
def remove_sub_graph(user_id):
    return f'CALL gds.graph.drop("{user_id}")'


# find single nodes
def find_single_nodes_inside_sub_graph():
    return 'match (s:Selected)<-[r]-(s1:Selected) ' \
           'where type(r) = "SELECTED" ' \
           'with collect(id(s)) as target, collect(id(s1)) as source ' \
           'match (s2:Selected) ' \
           'where not ( id(s2) in target) and not (id(s2)) in source ' \
           'return id(s2) as id'


# find source nodes
def find_source_nodes_inside_sub_graph():
    return 'match (s:Selected)<-[r]-(s1:Selected) ' \
           'where type(r) = "SELECTED" ' \
           'with collect(id(s)) as target, collect(id(s1)) as source ' \
           'match (s2:Selected) ' \
           'where not ( id(s2) in target) and id(s2) in source ' \
           'return id(s2) as id'


# find target nodes
def find_target_node_inside_sub_graph():
    return 'match (s:Selected)<-[r]-(s1:Selected) ' \
           'where type(r) = "SELECTED" ' \
           'with collect(id(s1)) as source, collect(id(s)) as target ' \
           'match (s2:Selected) ' \
           'where not ( id(s2) in source) and id(s2) in target ' \
           'return id(s2) as id'


# find paths from source to target
def find_paths_from_sources_to_targets(sources, targets, user_id, k):
    return f'with {sources} as nodeSource, {targets} as nodeTarget ' \
           'MATCH (source:Selected), (target:Selected) ' \
           'where id(source) in nodeSource and id(target) in nodeTarget ' \
           f'CALL gds.shortestPath.yens.stream("{user_id}", ' \
           '{sourceNode: source, ' \
           'targetNode: target, ' \
           f'k: {k}, ' \
           'relationshipWeightProperty: "weight" ' \
           '}) ' \
           'YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path ' \
           'RETURN ' \
           'id(gds.util.asNode(sourceNode)) AS sourceNodeName, ' \
           'id(gds.util.asNode(targetNode)) AS targetNodeName, ' \
           'totalCost, ' \
           '[nodeId IN nodeIds | id(gds.util.asNode(nodeId))] AS nodeNames ' \
           'ORDER BY sourceNode, targetNode, totalCost DESC '


