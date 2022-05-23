# queries for algorithm step 1

def get_lo_provided_by_course(course_id, user_id):
    query = 'MATCH (u:User) - [r1] -> (lo) <- [r2] - (c:Course)' \
            f'WHERE id(u)={user_id} AND id(c) = {course_id} ' \
            f'AND TYPE(r1) =~ "NEED_.*" AND TYPE(r2) =~ "TEACH_.*"' \
            f'RETURN lo.value as value, id(lo) as id'
    return query
