# Import library
import random
import math
from py2neo import Graph
from py2neo.matching import *
from models.user import User

# Import directory
from constants.algorithm_constants import *
from utilities.query_for_algorithm import *
from utilities.query_for_services import *
from algorithm_v2 import step1

# Declare Variable
graph = Graph()
nodes = NodeMatcher(graph)


def run_genetic_algorithm(all_set_of_candidate_course, user):
    LO_imax = finding_length_of_population(all_set_of_candidate_course)  # LO_imax has max length of candidate_course
    if not LO_imax:
        print("Can not find LO_imax")
        return
    length_of_native_population = LO_imax[1]  # length is the length of candidate course LO_imax
    native_population = initial_population(all_set_of_candidate_course, LO_imax)
    loop_times = 0
    optimized_population = []
    while (loop_times < AlgorithmConstant.V2_GENETIC_LOOP_TIMES):
        optimized_population = evaluate_and_filter(native_population, length_of_native_population, user)
        n = len(optimized_population)
        while (n < length_of_native_population):
            optimized_population = rebuild_population(optimized_population, all_set_of_candidate_course, user)
            n = optimized_population.__len__()
            if (n > length_of_native_population):
                optimized_population.pop()
                break
        loop_times += 1

    return optimized_population


def finding_optimization_courses(all_set_of_candidate_course, user):
    # Declare

    user_need_time = user.time
    user_need_cost = user.cost
    filter_set_of_course = []

    # Main Process
    optimized_population = run_genetic_algorithm(all_set_of_candidate_course, user)
    if not optimized_population:
        print("Can not find set of course from running genetic algorithm")
        return
    if (user_need_time == 0 and user_need_cost == 0):
        filter_set_of_course = optimized_population
    elif (user_need_time != 0):
        filter_set_of_course = user_filter_time(user_need_time, optimized_population)
    elif (user_need_cost != 0):
        filter_set_of_course = user_filter_cost(user_need_cost, optimized_population)
    optimized_population = run_genetic_algorithm(all_set_of_candidate_course, user)
    optimized_set_of_course = []
    for individual in optimized_population:
        optimized_set_of_course.append(get_set_of_course_from_individual(individual))
    if not optimized_population:
        print("Can not find set of course from running genetic algorithm")
        return
    if (user_need_time == 0 and user_need_cost == 0):
        filter_set_of_course = optimized_set_of_course
    elif (user_need_time != 0):
        filter_set_of_course = user_filter_time(user_need_time, optimized_set_of_course)
    elif (user_need_cost != 0):
        filter_set_of_course = user_filter_cost(user_need_cost, optimized_set_of_course)

    # Return
    return filter_set_of_course[0:AlgorithmConstant.V2_OMEGA]


# Private function
def finding_length_of_population(all_set_of_candidate_course):
    max_length = 0
    LO_imax = []
    for set_of_candidate_course in all_set_of_candidate_course:
        if len(set_of_candidate_course) > max_length:
            max_length = len(set_of_candidate_course)
            LO_imax = [index(all_set_of_candidate_course, set_of_candidate_course), max_length]
    if not LO_imax:
        print("Cannot find LO_imax in finding_length_of_population function")
        return
    return LO_imax


def initial_population(all_set_of_candidate_course, LO_imax):
    imax = LO_imax[0]
    s = LO_imax[1]
    stop_point = 0
    native_population = []
    stop_point = 0
    j = 0
    while (stop_point < s):
        individual = []
        for set_of_candidate_course in all_set_of_candidate_course:
            i = index(all_set_of_candidate_course, set_of_candidate_course)
            if (i != LO_imax):
                length_of_candidate_course = len(set_of_candidate_course)
                if (stop_point > length_of_candidate_course - 1):
                    j = random_int(0, length_of_candidate_course - 1)
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


def evaluate_and_filter(native_population, length_of_population, user):
    set_of_score_list = {}
    population_filtered = []
    optimized_population = []
    for individual in native_population:
        individual_score = calculate_score_for_individual(individual, user)
        set_of_score_list.update({index(native_population, individual): individual_score})
    sort_score_list = dict_sorted_by_value(set_of_score_list)
    n = math.floor(AlgorithmConstant.V2_LAMBDA * length_of_population)
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
    for i in population_filtered:
        optimized_population.append(native_population[i])
    return optimized_population


def rebuild_population(optimized_population, all_set_of_candidate_course, user):
    n = optimized_population.__len__()
    length_of_individual_gen = all_set_of_candidate_course.__len__()
    index_1 = random_int(0, n - 1)
    index_2 = random_int(0, n - 1)
    while (index_1 == index_2):
        index_2 = random_int(0, n - 1)
    individual_1 = optimized_population[index_1]
    individual_2 = optimized_population[index_2]
    ratio = random.random()
    if (ratio > AlgorithmConstant.V2_ALPHA):
        new_individuals = crossover(individual_1, individual_2)
        optimized_population.append(new_individuals[0])
        optimized_population.append(new_individuals[1])
    else:
        i = random_int(0, length_of_individual_gen - 1)
        new_individual_1 = mutate(individual_1, all_set_of_candidate_course[i], i)
        new_individual_2 = mutate(individual_2, all_set_of_candidate_course[i], i)
        optimized_population.append(new_individual_1)
        optimized_population.append(new_individual_2)
    return optimized_population


def mutate(individual, set_of_course, i):
    mutate_point_index = random_int(0, set_of_course.__len__() - 1)
    individual[i] = set_of_course[mutate_point_index]
    return individual


def crossover(individual_1, individual_2):
    crossover_point_index = math.floor((individual_1.__len__() - 1) / 2)
    i = 0
    while (i <= crossover_point_index):
        temp = individual_1[i]
        individual_1[i] = individual_2[i]
        individual_2[i] = temp
        i += 1
    return [individual_1, individual_2]


def calculate_score_for_set_of_course(set_of_course, user):
    user_lo_need = graph.run(query_get_user_need_lo(user.id)).data()
    f1 = calculate_number_of_course(set_of_course)
    f2 = calculate_number_of_redundant_LO(set_of_course, user_lo_need)
    f3 = calculate_number_of_overlap_LO(set_of_course)
    f4 = calculate_number_of_overlap_level(set_of_course, user_lo_need)
    w1 = AlgorithmConstant.V2_W1
    w2 = AlgorithmConstant.V2_W2
    w3 = AlgorithmConstant.V2_W3
    w4 = AlgorithmConstant.V2_W4
    weighted_sum = f1 * w1 + f2 * w2 + f3 * w3 + f4 * w4
    return weighted_sum


def calculate_score_for_individual(individual, user):
    set_of_course = get_set_of_course_from_individual(individual)
    return calculate_score_for_set_of_course(set_of_course, user)


def calculate_number_of_course(set_of_course):
    return len(set_of_course)


def calculate_number_of_redundant_LO(set_of_course, user_lo_need):
    lo_provided = graph.run(query_to_get_list_lo_provided_by_set_course(set_of_course)).data()
    set_lo = list(set(get_list_id(lo_provided)))
    return set_lo.__len__() - user_lo_need.__len__()


def calculate_number_of_overlap_LO(set_of_course):
    lo_provided = graph.run(query_to_get_list_lo_provided_by_set_course(set_of_course)).data()
    set_lo = list(set(get_list_id(lo_provided)))
    return lo_provided.__len__() - set_lo.__len__()


def calculate_number_of_overlap_level(set_of_course, user_lo_need):
    counter = 0
    lo_provided = graph.run(query_to_get_list_lo_provided_by_set_course(set_of_course)).data()

    for lo in user_lo_need:
        for lo_provided_element in lo_provided:
            if lo.get('id') == lo_provided_element.get('id'):
                counter += lo_provided_element.get('level') - lo.get('level')
                break
    return counter


def calculate_sum_time_of_individual(set_of_course):
    list_time = graph.run(query_get_list_time_of_set_course(set_of_course)).data()
    total_time = 0

    for time in list_time:
        try:
            total_time += float(time.get('time')[0: time.get('time').find(" ")])
        except:
            total_time += 0

    return total_time


def calculate_sum_cost_of_individual(set_of_course):
    sumFee = graph.run(query_get_sum_tuition_set_course(set_of_course)).data()
    return sumFee[0].get('sumFee') or 0


def get_individual_by_index(selected_population_dict, index, native_population):
    return native_population[index]


def user_filter_time(user_need_time, optimized_set_of_course):
    filter_set_of_course = []
    for set_of_course in optimized_set_of_course:
        sum_time_set_of_course = calculate_sum_time_of_individual(set_of_course)
        if (user_need_time >= sum_time_set_of_course):
            filter_set_of_course.append(set_of_course)
    return filter_set_of_course


def user_filter_cost(user_need_cost, optimized_set_of_course):
    filter_set_of_course = []
    for set_of_course in optimized_set_of_course:
        sum_cost_set_of_course = calculate_sum_cost_of_individual(set_of_course)
        if (user_need_cost >= sum_cost_set_of_course):
            filter_set_of_course.append(set_of_course)
    return filter_set_of_course


def get_set_of_course_by_omega(filter_set_of_course):
    set_of_course = []
    i = 0
    while (i < AlgorithmConstant.V2_OMEGA):
        set_of_course.append(filter_set_of_course[i])
        i += 1
    return set_of_course


def random_int(start, end):
    return random.randint(start, end)


def index(array, value):
    return array.index(value)


def map_list_dict_to_list(dict):
    return dict.get('id')


def get_list_id(list_dict):
    return list(map(map_list_dict_to_list, list_dict))


def dict_sorted_by_value(dictionary):
    sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1]))
    return sorted_dict


def get_set_of_course_from_individual(individual):
    list_set = []
    for gen in individual:
        if type(gen) == type([]):
            for course_id in gen:
                list_set.append(course_id)
        elif (type(gen) == type(1)):
            list_set.append(gen)
        else:
            print("type of gen in individual is not true")
            return
    return list(list_set)


def get_input_for_step3(user_id):
    all_set_of_candidate_course = []
    sets_of_course = step1.get_input_for_step2(user_id)
    for set_of_course in sets_of_course:
        set_of_candidate_course_by_LO = []
        for candidate_course in set_of_course:
            set_of_candidate_course_by_LO.append(candidate_course.get_value())
        all_set_of_candidate_course.append(set_of_candidate_course_by_LO)
    if not all_set_of_candidate_course:
        print("cannot find all_set_of_candidate_course")
    user = User(nodes.get(user_id))
    user.id = user_id
    return finding_optimization_courses(all_set_of_candidate_course, user)


def main():
    result = get_input_for_step3(5)
    print(result)

# main()
