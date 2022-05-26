import sys
sys.path.insert(0, '../')
from utilities.query_for_algorithm import *
from constants.algorithm_constants import *
import numpy as np
import json
from py2neo import Graph

graph = Graph()

# data sample for test
course_user_need_to_learn = [[1275,1393,2318,1884,1922,2919,4159,4277,3557,1905]]

# Check if user can learn the course
def user_can_learn(current_user_lo,course_id):
    course_need_lo = graph.run(query_get_input_lo_of_a_course(course_id))
    flag = False
    if not course_need_lo:
        return True
    for i in course_need_lo:
        for j in current_user_lo:
            if i.get('id') == j.get('id_lo'):
                flag = True
                if(i.get('level') > j.get('level')):
                    return False
        if(flag == False):
            return False
        else:
            flag = False
    return True

# Finding course that user can learn with current LO
def find_courses_can_learn(set_of_course,current_user_lo):
    course_can_learn = []
    for course_id in set_of_course:
        if(user_can_learn(current_user_lo,course_id) == True):
            course_can_learn.append(course_id)
    return course_can_learn

#Update LO which user has, following the learning path
def update_user_has_lo(current_user_lo,course_id):
    lo_provided_course = graph.run(query_get_lo_provided_by_course(course_id))
    for i in lo_provided_course:
        flag = False
        for j in current_user_lo:
            if(i.get('id') == j.get('id_lo')):
                flag = True
                updated_level_lo = {'id_lo':i.get('id'),'level': i.get('level')}
                index = current_user_lo.index(j)
                current_user_lo[index] = updated_level_lo
                break
        if(flag == False):
            newLo = {'id_lo':i.get('id'),'level':i.get('level')}
            current_user_lo.append(newLo)
    return current_user_lo

# Create Learning Path for only set of course
def create_LP(set_of_course,user_id):
    i = 1
    learning_path = []
    user_has_lo = graph.run(query_get_lo_user_has(user_id)).data()
    while True:
        course_can_learn = find_courses_can_learn(set_of_course,user_has_lo)
        if not course_can_learn:
            break;  
        for course_id in course_can_learn:
            user_has_lo = update_user_has_lo(user_has_lo,course_id)
            if i == 1:
                print(user_has_lo)
                i+=1
            set_of_course.pop(set_of_course.index(course_id))
            learning_path.append(course_id)
        if not set_of_course:
            break
    return learning_path

# Find all of proper Learning path for many set of course
# input: set of course from step 3, user_id of User
# output: List of Learning Path
def finding_set_of_LP(all_of_course,user_id):
    set_of_lp = []
    for set_of_course in all_of_course:
        set_of_lp.append(create_LP(set_of_course,user_id))
    return set_of_lp

# print(finding_set_of_LP(course_user_need_to_learn,4678))


