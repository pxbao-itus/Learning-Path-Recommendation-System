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


