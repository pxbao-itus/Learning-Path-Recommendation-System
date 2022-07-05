def query_create_user(user_id, cost, time):
    return f'match (u:User) where id(u) = {user_id} set u.cost = {cost} set u.time = {time} return id(u) as id;'


def query_register(name, email):
    return "merge (n:User {name:'%s', email:'%s'}) return id(n) as id; " % (
        name, email)


def query_get_id_by_email(email):
    return f'match (u:User) where u.email = "{email}" return id(u) as id;'


def query_get_user_info(user_id):
    return f'match (u:User)' \
           f'where id(u)={user_id} ' \
           f'return id(u) as id, u.email as email, u.name as name, u.cost as cost, u.time as time;'


def query_create_objective_career(user_id, career_id):
    return f'MATCH (a:User), (b:Career) WHERE id(a)={user_id} AND id(b)={career_id} merge (a)-[r:HAS_OBJECTIVE]->(b) ' \
           f'return id(r) as id; '


def query_get_objective(user_id):
    return f'Match (u:User)-[r]->(c:Career) ' \
           f'where id(u) = {user_id} ' \
           f'return id(c) as id, c.creTitle as title'


def query_create_has_lo(user_id, lo):
    return f"MATCH (a:User), (b) WHERE id(a)={user_id} AND id(b)={lo.get('id')} " \
           f"merge (a)-[r:HAS_{lo.get('type').upper()}" \
           "{Level:%d}]->(b);" % (lo.get('level'))


def query_create_user_need_lo(user_id):
    return [" Match (u: User )-[:HAS_OBJECTIVE]->(c: Career)"
            " Match (u)-[ru:HAS_TOOL]->(ku:Tool)<-[rcc:NEED_TOOL]-(c)"
            f" Where id(u)={user_id} and ((ru.Level < rcc.Level) )"
            " merge (u)-[r:NEED_TOOL{Level:rcc.Level}]->(ku) return id(r) as id;",
            " Match (u: User )-[:HAS_OBJECTIVE]->(c: Career)"
            " match (c)-[rc:NEED_TOOL]->(kc)"
            f" Where id(u)={user_id} and not (u)-[:HAS_TOOL]->(kc)"
            " merge (u)-[r:NEED_TOOL{Level:rc.Level}]->(kc) return id(r) as id;",
            " Match (u: User )-[:HAS_OBJECTIVE]->(c: Career)"
            " Match (u)-[ru:HAS_KNOWLEDGE]->(ku)<-[rcc:NEED_KNOWLEDGE]-(c)"
            f" Where id(u)={user_id} and ((ru.Level < rcc.Level) )"
            " merge (u)-[r:NEED_KNOWLEDGE{Level:rcc.Level}]->(ku) return id(r) as id;",
            " Match (u: User )-[:HAS_OBJECTIVE]->(c: Career)"
            " match (c)-[rc:NEED_KNOWLEDGE]->(kc)"
            f" Where id(u)={user_id} and not (u)-[:HAS_KNOWLEDGE]->(kc)"
            " merge (u)-[r:NEED_KNOWLEDGE{Level:rc.Level}]->(kc) return id(r) as id;",
            " Match (u: User )-[:HAS_OBJECTIVE]->(c: Career)"
            " Match (u)-[ru:HAS_PLATFORM]->(ku)<-[rcc:NEED_PLATFORM]-(c)"
            f" Where id(u)={user_id} and ((ru.Level < rcc.Level) )"
            " merge (u)-[r:NEED_PLATFORM{Level:rcc.Level}]->(ku) return id(r) as id;",
            " Match (u: User )-[:HAS_OBJECTIVE]->(c: Career)"
            " match (c)-[rc:NEED_PLATFORM]->(kc)"
            f" Where id(u)={user_id} and not (u)-[:HAS_PLATFORM]->(kc)"
            " merge (u)-[r:NEED_PLATFORM{Level:rc.Level}]->(kc) return id(r) as id;",
            " Match (u: User )-[:HAS_OBJECTIVE]->(c: Career)"
            " Match (u)-[ru:HAS_FRAMEWORK]->(ku)<-[rcc:NEED_FRAMEWORK]-(c)"
            f" Where id(u)={user_id} and ((ru.Level < rcc.Level) )"
            " merge (u)-[r:NEED_FRAMEWORK{Level:rcc.Level}]->(ku) return id(r) as id;",
            " Match (u: User )-[:HAS_OBJECTIVE]->(c: Career)"
            " match (c)-[rc:NEED_FRAMEWORK]->(kc)"
            f" Where id(u)={user_id} and not (u)-[:HAS_FRAMEWORK]->(kc)"
            " merge (u)-[r:NEED_FRAMEWORK{Level:rc.Level}]->(kc) return id(r) as id;",
            " Match (u: User )-[:HAS_OBJECTIVE]->(c: Career)"
            " Match (u)-[ru:HAS_PROGRAMINGLANGUAGE]->(ku)<-[rcc:NEED_PROGRAMINGLANGUAGE]-(c)"
            f" Where id(u)={user_id} and ((ru.Level < rcc.Level) )"
            " merge (u)-[r:NEED_PROGRAMINGLANGUAGE{Level:rcc.Level}]->(ku) return id(r) as id;",
            " Match (u: User )-[:HAS_OBJECTIVE]->(c: Career)"
            " match (c)-[rc:NEED_PROGRAMINGLANGUAGE]->(kc)"
            f" Where id(u)={user_id} and not (u)-[:HAS_PROGRAMINGLANGUAGE]->(kc)"
            " merge (u)-[r:NEED_PROGRAMINGLANGUAGE{Level:rc.Level}]->(kc) return id(r) as id;"]


def query_delete_relationship_user_need_lo(user_id):
    return 'match (u:User)-[r]->(lo) ' \
           f'where id(u) = {user_id} and type(r) =~"NEED_.*" ' \
           'delete r'


def query_get_course_name_by_id(set_course):
    return f'with {set_course} as list ' \
           f'match (c:Course) ' \
           f'where id(c) in list ' \
           f'return c.crsName as name'


def query_get_lo_need_by_career(career_id):
    return ' match (c:Career)-[r]->(lo) ' \
           f'where id(c) = {career_id} ' \
           f'return id(lo) as id, lo.value as name, type(r) as type'


def query_update_career(user_id, career_id):
    return f'match (u:User)-[r]->(c:Career) ' \
           f'where id(u) = {user_id} ' \
           f'detach delete r  ;'


def query_get_info_a_course(course_id):
    return 'match (c:Course) ' \
           f'where id(c) = {course_id} ' \
           f'return id(c) as id, c.crsName as name, c.crsEnroll as enroll, c.crsFee as cost, c.crsLink as link,' \
           f' c.crsTime as time, c.crsRating as rating'


def query_get_lo_user_has(user_id):
    return 'match (u:User)-[r]-(lo) ' \
           f'where id(u) = {user_id} and type(r) <> "HAS_OBJECTIVE" ' \
           f'return id(lo) as id, lo.value as value, r.Level as level'


def query_get_lo_need_by_career_by_user_id(user_id):
    return ' match (u:User)-[r1]->(c:Career)-[r]->(lo) ' \
           f'where id(u) = {user_id} ' \
           f'return id(lo) as id, lo.value as name, r.Level as level, type(r) as type'


def query_get_top_100_lo():
    return ' with ["Knowledge", "Tool", "Platform", "ProgramingLanguage", "Framework"] as types ' \
           'match (u) ' \
           'where labels(u)[0] in types ' \
           'return id(u) as id, u.value as value, labels(u)[0] as type limit 100'


def query_search_lo(value):
    return 'with ["Knowledge", "Tool", "Platform", "ProgramingLanguage", "Framework"] as types ' \
           'match (u) ' \
           f'where labels(u)[0] in types and u.value contains "{value}"' \
           'return id(u) as id, u.value as value, labels(u)[0] as type limit 100'


def query_get_lo_has(user_id):
    return 'match (u:User)-[r]->(lo) ' \
           f'where id(u) = {user_id} and type(r) =~ "HAS_.*" and type(r) <> "HAS_OBJECTIVE" ' \
           f'return id(lo) as id, lo.value as value, r.Level as level ' \
           f'order by id;'


def query_delete_lo_has(user_id, lo_id):
    return 'match (u:User)-[r]->(lo) ' \
           f'where id(u) ={user_id} and id(lo) = {lo_id} ' \
           f'detach delete r'


def query_create_lo_has(user_id, lo_id, level, type):
    return 'match (u:User)' \
           f'where id(u) = {user_id} ' \
           f'match (lo) ' \
           f'where id(lo) = {lo_id} ' + "merge (u)-[r:HAS_%s {Level: %s}]->(lo) return id(r) as id" % (
               type.upper(), level)


def query_get_type(lo_id):
    return 'match (lo) ' \
           f'where id(lo) = {lo_id} ' \
           f'return labels(lo)[0] as type'


def query_get_courses_info(course_id):
    return 'match (c:Course) ' \
           f'where id(c) = {course_id} ' \
           f'return id(c) as id, c.crsName as name, c.crsFee as cost, c.crsTime as Time, c.crsRating as rating, ' \
           f'c.crsLink as link, c.crsEnroll as enroll; '
