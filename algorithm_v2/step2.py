# Import library
import random
import math
from py2neo import Graph



#Import directory
from constants.algorithm_constants import *
from utilities.query_for_algorithm import *

#Declare Variable
graph = Graph()

def run_genetic_algorithm(all_set_of_candidate_course,user):
    LO_imax = finding_length_of_population(all_set_of_candidate_course) # LO_imax has max length of candidate_course
    if not LO_imax:
        print("Can not find LO_imax")
        return
    length_of_population = LO_imax[1] # s is the length of candidate course LO_imax
    native_population = initial_population(all_set_of_candidate_course,LO_imax)
    loop_times = 0
    selected_population_dict = []
    while(loop_times < AlgorithmConstant.GENETIC_LOOP_TIMES):
        selected_population_dict = evaluate_and_filter(native_population,length_of_population,user)
        n = selected_population_dict.__len__()
        while(n < length_of_population):
            selected_population_dict = rebuild_population(selected_population_dict,all_set_of_candidate_course)
            n = selected_population_dict.__len__()
            if(n > length_of_population):
                selected_population_dict.popitem()
                break
        loop_times += 1

    return selected_population_dict

def finding_optimization_courses(all_set_of_candidate_course,user):
    # Declare
    
    user_need_time = user.time
    user_need_cost = user.cost
    filter_set_of_course = []

    # Main Process
    set_of_course_with_score = run_genetic_algorithm(all_set_of_candidate_course,user)
    if not set_of_course_with_score:
        print("Can not find set of course from running genetic algorithm")
        return
    if(user_need_time == 0 and user_need_cost == 0):
        filter_set_of_course = set_of_course_with_score
    elif(user_need_time != 0):
        filter_set_of_course = user_filter_time(user_need_time,set_of_course_with_score)
    elif(user_need_cost != 0):
        filter_set_of_course = user_filter_cost(user_need_cost,set_of_course_with_score)

    # Return
    return get_set_of_course_by_omega(filter_set_of_course)


# Private function
def finding_length_of_population(all_set_of_candidate_course):
    max_length = 0
    LO_imax = []
    for set_of_candidate_course in all_set_of_candidate_course:
        if len(set_of_candidate_course) > max_length:
            max_length = len(set_of_candidate_course)
            LO_imax = [index(all_set_of_candidate_course,set_of_candidate_course),max_length]
    if not LO_imax:
        print("Cannot find LO_imax in finding_length_of_population function")
        return
    return LO_imax

def initial_population(all_set_of_candidate_course,LO_imax):
    imax = LO_imax[0]
    s = LO_imax[1]
    stop_point = 0
    native_population = []
    stop_point = 0 
    j = 0
    while(stop_point < s):
        individual = []
        for set_of_candidate_course in all_set_of_candidate_course:
            i = index(all_set_of_candidate_course,set_of_candidate_course)
            if(i != LO_imax):
                length_of_candidate_course = len(set_of_candidate_course)
                if(stop_point > length_of_candidate_course - 1 ):
                    j = random_int(0,length_of_candidate_course)
                else:
                    j = stop_point
                individual.append(set_of_candidate_course[j])
            else:
                individual.append(set_of_candidate_course[stop_point])
        native_population.append(individual)
        stop_point += 1
    if not native_population:
        print("Cannot find native_population")
        return
    return native_population


def evaluate_and_filter(native_population,length_of_population,user):
    set_of_score_list = {}
    population_filtered = []
    for individual in native_population:
        individual_score = calculate_score_for_individual(individual,user)
        set_of_score_list.update({individual:individual_score})
    sort_score_list = dict_sorted_by_value(set_of_score_list)
    n = math.floor(AlgorithmConstant.LAMBDA * length_of_population)
    for individual in sort_score_list:
        if len(population_filtered) == n:
            break
        elif len(population_filtered) < n:
            population_filtered.append(individual)
        else:
            print("Cannot find population_filtered")
            return
    if not population_filtered:
        print("Cannot find population_filtered")
        return
    return population_filtered

def rebuild_population(selected_population_dict,all_set_of_candidate_course):
    n = selected_population_dict.__len__()
    length_of_individual_gen = all_set_of_candidate_course.__len__()
    index_1 = random_int(0,n-1)
    index_2 = random_int(0,n-1)
    while(index_1 != index_2):
        index_2 = random_int(0,n-1)
    individual_1 = get_individual_by_index(selected_population_dict,index_1)
    individual_2 = get_individual_by_index(selected_population_dict,index_2)
    ratio = random.random()
    if(ratio > AlgorithmConstant.ALPHA):
        new_individuals = crossover(individual_1,individual_2)
        selected_population_dict.update({new_individuals[0]:calculate_score_for_individual(new_individuals[0],user)})
        selected_population_dict.update({new_individuals[1]:calculate_score_for_individual(new_individuals[1],user)})
    else:
        index = random_int(0,length_of_individual_gen-1)
        new_individual_1 = mutate(individual_1,all_set_of_candidate_course[index],index)
        new_individual_2 = mutate(individual_2,all_set_of_candidate_course[index],index)
        selected_population_dict.update({new_individual_1:calculate_score_for_individual(new_individual_1,user)})
        selected_population_dict.update({new_individual_2:calculate_score_for_individual(new_individual_2,user)})
    return selected_population_dict


def mutate(individual,set_of_course,index):
    mutate_point_index = random(0,set_of_course.__len__()-1)
    individual[index] = set_of_course[mutate_point_index]
    return individual

def crossover(individual_1,individual_2):
    crossover_point_index = math.floor((individual_1.__len__()-1)/2)
    i = 0
    while(i <= crossover_point_index):
        temp = individual_1[i]
        individual_1[i] = individual_2[i]
        individual_2[i] = temp
        i += 1
    return [individual_1,individual_2]

def calculate_score_for_individual(individual,user):
    thisset = {}
    for gen in individual:
        if type(gen) == type([]):
            for course_id in gen:
                thisset.add(course_id)
        elif (type(gen) == type(1)):
            thisset.add(gen)
        else:
            print("type of gen in individual is not true")
            return
    user_lo_need =  graph.run(query_get_user_need_lo(user.id)).data()

    f1 = calculate_number_of_course(thisset)
    f2 = calculate_number_of_redundant_LO(thisset,user_lo_need)
    f3 = calculate_number_of_overlap_LO(thisset)
    f4 = calculate_number_of_overlap_level(thisset,user_lo_need)
    w1 = AlgorithmConstant.W1
    w2 = AlgorithmConstant.W2
    w3 = AlgorithmConstant.W3
    w4 = AlgorithmConstant.W4
    weighted_sum = f1*w1 + f2*w2 + f3*w3 + f4*w4
    return weighted_sum

def calculate_number_of_course(thisset):
    return len(thisset)

def calculate_number_of_redundant_LO(thisset,user_lo_need):
    lo_provided = graph.run(query_to_get_list_lo_provided_by_set_course(list(thisset))).data()
    set_lo = list(set(get_list_id(lo_provided)))
    return set_lo.__len__() - user_lo_need.__len__()

def calculate_number_of_overlap_LO(thisset):
    lo_provided = graph.run(query_to_get_list_lo_provided_by_set_course(list(thisset))).data()
    set_lo = list(set(get_list_id(lo_provided)))
    return lo_provided.__len__() - set_lo.__len__()

def calculate_number_of_overlap_level(thisset,user_lo_need):
    counter = 0
    lo_provided = graph.run(query_to_get_list_lo_provided_by_set_course(list(thisset))).data()

    for lo in user_lo_need:
        for lo_provided_element in lo_provided:
            if lo.get('id') == lo_provided_element.get('id'):
                counter += lo_provided_element.get('level') - lo.get('level')
                break
    return counter

def get_individual_by_index(selected_population_dict,index):
    pivot = 0
    individual = []
    for i in selected_population_dict:
        if(pivot != index):
            pivot += 1
            continue
        else:
            individual = i
    if not individual:
        print("Cannot find individual by index")
        return
    return individual

def sort_individual_by_score(set_of_score_list):

    return

def user_filter_time(user_need_time,optimized_set_of_course):
    return

def user_filter_cost(user_need_time,optimized_set_of_course):
    return

def get_set_of_course_by_omega(filter_set_of_course):
    sorted_set_of_course_by_score = dict_sorted_by_value(filter_set_of_course)
    set_of_course = []
    i = 0
    while(i < AlgorithmConstant.V2_OMEGA):
        set_of_course.append(sorted_set_of_course_by_score[i])
        i += 1
    return set_of_course

def get_input_for_step3():
    return

def random_int(start,end):
    return random.randint(start,end)

def index(array,value):
    return array.index(value)

def map_list_dict_to_list(dict):
    return dict.get('id')

def get_list_id(list_dict):
    return list(map(map_list_dict_to_list, list_dict))

def dict_sorted_by_value(dictionary):
    sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1]))