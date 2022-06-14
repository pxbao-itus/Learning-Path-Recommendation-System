def query_create_user(name, email, cost, time):
    return "merge (n:User {name:'%s', email:'%s', cost:%d, time:%d}) return id(n) as id; " % (
        name, email, cost, time)


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
           f'return id(c) as id'


def query_create_has_lo(user_id, lo):
    return f"MATCH (a:User), (b) WHERE id(a)={user_id} AND id(b)={lo.get('id')} " \
           f"merge (a)-[r:HAS_{lo.get('type').upper()}" \
           "{Level:%d}]->(b);" % (lo.get('level'))


def query_create_user_need_lo(user_id):
    return [" Match (u: User )-[:HAS_OBJECTIVE]->(c: Career)"
            " Match (u)-[ru:HAS_TOOL]->(ku:Tool)<-[rcc:NEED_TOOL]-(c)"
            f" Where id(u)={user_id} and ((ru.Level < rcc.Level) )"
            " merge (u)-[r:NEED_TOOL{Level:rcc.Level}]->(ku)return id(r) as id;",
            " Match (u: User )-[:HAS_OBJECTIVE]->(c: Career)"
            " match (c)-[rc:NEED_TOOL]->(kc)"
            f" Where id(u)={user_id} and not (u)-[:HAS_TOOL]->(kc)"
            " merge (u)-[r:NEED_TOOL{Level:rc.Level}]->(kc)return id(r) as id;",
            " Match (u: User )-[:HAS_OBJECTIVE]->(c: Career)"
            " Match (u)-[ru:HAS_KNOWLEDGE]->(ku)<-[rcc:NEED_KNOWLEDGE]-(c)"
            f" Where id(u)={user_id} and ((ru.Level < rcc.Level) )"
            " merge (u)-[r:NEED_KNOWLEDGE{Level:rcc.Level}]->(ku)return id(r) as id;",
            " Match (u: User )-[:HAS_OBJECTIVE]->(c: Career)"
            " match (c)-[rc:NEED_KNOWLEDGE]->(kc)"
            f" Where id(u)={user_id} and not (u)-[:HAS_KNOWLEDGE]->(kc)"
            " merge (u)-[r:NEED_KNOWLEDGE{Level:rc.Level}]->(kc)return id(r) as id;",
            " Match (u: User )-[:HAS_OBJECTIVE]->(c: Career)"
            " Match (u)-[ru:HAS_PLATFORM]->(ku)<-[rcc:NEED_PLATFORM]-(c)"
            f" Where id(u)={user_id} and ((ru.Level < rcc.Level) )"
            " merge (u)-[r:NEED_PLATFORM{Level:rcc.Level}]->(ku)return id(r) as id;",
            " Match (u: User )-[:HAS_OBJECTIVE]->(c: Career)"
            " match (c)-[rc:NEED_PLATFORM]->(kc)"
            f" Where id(u)={user_id} and not (u)-[:HAS_PLATFORM]->(kc)"
            " merge (u)-[r:NEED_PLATFORM{Level:rc.Level}]->(kc)return id(r) as id;",
            " Match (u: User )-[:HAS_OBJECTIVE]->(c: Career)"
            " Match (u)-[ru:HAS_FRAMEWORK]->(ku)<-[rcc:NEED_FRAMEWORK]-(c)"
            f" Where id(u)={user_id} and ((ru.Level < rcc.Level) )"
            " merge (u)-[r:NEED_FRAMEWORK{Level:rcc.Level}]->(ku)return id(r) as id;",
            " Match (u: User )-[:HAS_OBJECTIVE]->(c: Career)"
            " match (c)-[rc:NEED_FRAMEWORK]->(kc)"
            f" Where id(u)={user_id} and not (u)-[:HAS_FRAMEWORK]->(kc)"
            " merge (u)-[r:NEED_FRAMEWORK{Level:rc.Level}]->(kc)return id(r) as id;",
            " Match (u: User )-[:HAS_OBJECTIVE]->(c: Career)"
            " Match (u)-[ru:HAS_PROGRAMINGLANGUAGE]->(ku)<-[rcc:NEED_PROGRAMINGLANGUAGE]-(c)"
            f" Where id(u)={user_id} and ((ru.Level < rcc.Level) )"
            " merge (u)-[r:NEED_PROGRAMINGLANGUAGE{Level:rcc.Level}]->(ku)return id(r) as id;",
            " Match (u: User )-[:HAS_OBJECTIVE]->(c: Career)"
            " match (c)-[rc:NEED_PROGRAMINGLANGUAGE]->(kc)"
            f" Where id(u)={user_id} and not (u)-[:HAS_PROGRAMINGLANGUAGE]->(kc)"
            " merge (u)-[r:NEED_PROGRAMINGLANGUAGE{Level:rc.Level}]->(kc)return id(r) as id;"]


def query_delete_relationship_user_need_lo(user_id):
    return 'match (u:User)-[r]->(lo) ' \
           f'where id(u) = {user_id} and type(r) =~"NEED_.*" ' \
           'delete r'


def query_get_course_name_by_id(set_course):
    return f'with {set_course} as list ' \
           f'match (c:Course) ' \
           f'where id(c) in list ' \
           f'return c.crsName as name'
