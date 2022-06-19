# queries for algorithm step 1
# =========================STEP1=================================
# get set lo that user need
def query_get_user_need_lo(user_id):
    return f"MATCH (u:User)-[r]->(k)" \
           f"WHERE ID(u) = {user_id} AND TYPE(r) =~ 'NEED_.*' " \
           f"RETURN id(k) as id, r.Level as level;"

def query_get_user_need_lo_id(user_id):
    return f"MATCH (u:User)-[r]->(k)" \
           f"WHERE ID(u) = {user_id} AND TYPE(r) =~ 'NEED_.*' " \
           f"RETURN collect(id(k)) as lo_list"


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


# get information of a course
def query_get_rating_course(course_id):
    return f'MATCH (c: Course) WHERE id(c) = {course_id} RETURN c.crsRating as rating'


# get set courses provided lo
def query_get_courses_provided_a_lo(lo_id, level):
    return f'MATCH (lo)<-[r]-(c:Course) WHERE id(lo) = {lo_id} and r.Level >= {level} ' \
           f'and type(r)=~"TEACH.*" return id(c) as id'


# calculate similarity between a Course and a User
def query_calculate_similarity_jaccard(user_id, course_id):
    return 'MATCH (p1:User)-[ru]-(e1)' \
           f' where type(ru) =~ "NEED_.*" and id(p1) = {user_id}' \
           ' WITH p1, collect(id(e1)) AS p1entity_type' \
           f' MATCH (p2:Course)-[rc]-(e2) WHERE type(rc) =~ "TEACH_.*" and id(p2) = {course_id}' \
           f' and type(rc) <> "TEACH_IN"' \
           ' WITH p1, p1entity_type, p2, collect(id(e2)) AS p2entity_type' \
           ' RETURN gds.similarity.jaccard(p1entity_type, p2entity_type) AS similarity'


def query_calculate_similarity_overlap(user_id, course_id):
    return 'MATCH (p1:User)-[ru]-(e1) ' \
           f' where type(ru) =~ "NEED_.*" and id(p1) = {user_id} ' \
           'WITH p1, collect(id(e1)) AS p1entity_type ' \
           f'MATCH (p2:Course)-[rc]-(e2) WHERE (type(rc) =~ "TEACH_.*" or type(rc) =~"REQUIRE_.*") and id(p2) = {course_id}' \
           f'  and type(rc) <> "TEACH_IN" ' \
           'WITH p1, p1entity_type, p2, collect(id(e2)) AS p2entity_type ' \
           'RETURN gds.similarity.overlap(p1entity_type, p2entity_type) AS similarity '


# ===============================STEP 2==========================================
def query_lo_require_a_course(course_id):
    return 'MATCH (c:Course)-[r]->(lo) ' \
           f'WHERE id(c)={course_id} AND TYPE(r)=~"REQUIRE_.*" ' \
           'RETURN id(lo) AS id, r.Level AS level'


def query_to_get_list_lo_provided_by_set_course(set_course_id):
    return f'with {set_course_id} as listCourse ' \
           'match (lo)<-[r1]-(c:Course) ' \
           f'where type(r1)=~"TEACH_.*" and id(c) in listCourse ' \
           'return id(lo) as id, r1.Level as level'


def query_to_create_temporary_relationship_user_lo(user_id, list_lo):
    return f'WITH {list_lo} as list ' \
           f'MATCH (a:User), (b) WHERE id(a)={user_id} AND id(b) in list ' \
           'CREATE (a)-[r:NEED_TEMPORARY {Level:1}]->(b);'


def query_to_remove_temporary_relationship_created(user_id):
    return f'MATCH (a:User)-[r]-> (b) WHERE id(a)={user_id} AND type(r) = "NEED_TEMPORARY" ' \
           'DELETE r'


def query_get_rating_set_course(set_course_id):
    return f'WITH {set_course_id} as listCourse ' \
           'MATCH (c:Course) ' \
           'WHERE id(c) in listCourse ' \
           'RETURN avg(c.crsRating) as avgRating '


def query_get_sum_tuition_set_course(set_course_id):
    return f'WITH {set_course_id} as listCourse ' \
           'MATCH (c:Course) ' \
           'WHERE id(c) in listCourse ' \
           'RETURN sum(c.crsFee) as sumFee'


def query_get_list_time_of_set_course(set_course_id):
    return f'WITH {set_course_id} as listCourse ' \
           'MATCH (c:Course) ' \
           'WHERE id(c) in listCourse ' \
           'RETURN c.crsTime as time '


# ================================STEP 4==========================================
# Query to get set of lo that user has
def query_get_lo_user_has(user_id):
    return 'MATCH (u:User)-[ru]->(m) ' \
           f'where id(u) = {user_id} and type(ru) =~ "HAS_.*" and type(ru) <> "HAS_OBJECTIVE"' \
           f'RETURN id(m) AS id_lo, ru.Level AS level'
