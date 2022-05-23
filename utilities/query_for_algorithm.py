# queries for algorithm step 1

# get set course that user need
def query_get_user_need_lo(user_id):
    return f"MATCH (u:User)-[r]->(k) " \
           f"WHERE ID(u) = {user_id} AND TYPE(r) =~ 'NEED_.*' " \
           f"RETURN id(k) as id, r.Level as level;"


# get set LO that a course can provide
def query_get_lo_provided_by_course(course_id):
    query = 'MATCH (lo) <- [r2] - (c:Course)' \
            f'WHERE id(c) = {course_id} ' \
            f'AND TYPE(r2) =~ "TEACH_.*" AND TYPE(r2) <> "TEACH_IN"' \
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
def query_get_courses_provided_a_lo(lo_id):
    return f'MATCH (lo)<-[r]-(c:Course) WHERE id(lo) = {lo_id} return id(c) as id'
