import random
from load_data import Dataset
from enum_criteria import Criteria
from numpy import matmul , argmax , array, sqrt
import numpy
import pandas as pd



WEIGHTS_VECTOR = [0.6, 0.1, 0.07, 0.13, 0.05, 0.05]
TYPE = [True, False, False, False, False, False]


def change_importace(arr):
    global arr_importance
    arr_importance = arr
    
    
def change_array(arr):
    global arr_criteria
    arr_criteria = arr


def draw_three_hotels(data):
    three_hotels = []
    three_idx = []
    
    while(len(three_idx) < 3):
        idx = random.randint(1, 120)
        if idx not in three_idx:
            three_idx.append(idx)
            
    for idx in three_idx:
        three_hotels.append(data.get_dicts_array()[idx])
        
    return three_hotels


def choose_3_hotels(data, criterion, min_lim, max_lim):
    hotels = []
    ids = []

    filtered_data =  [d for d in data.rows if d[criterion] != "unknown" and int(d[criterion]) >= min_lim and int(d[criterion]) <= max_lim]
    ids = [int(f[0]) for f in filtered_data]
    n = len(ids)

    while n < 3:
        idx = random.randint(1, len(data))
        if idx not in ids:
            ids.append(idx)
            n += 1
    
    if n > 3: ids = random.sample(ids, 3)

    for idx in ids:
        hotels.append(data.get_dicts_array()[idx])
    

    return hotels


def create_matrix_criteria_alternatives(hotels):
    matrix = [[0]*len(Criteria) for i in range(3)]
    
    for i in range(len(hotels)):
        for critery in Criteria:
            matrix[i][critery.value] = int(hotels[i].get(critery.get_origin_name()))
    
    return normalize_matrix(matrix)
    
    
def normalize_matrix(matrix):
    vector =  numpy.sqrt(numpy.sum(array(matrix), axis=0))
    return [[matrix[i][j]/vector[j]  for j in range(len(matrix[0]))] for i in range(len(matrix))]
    

def weighted_matrix(matrix):
    return [[matrix[i][j]*WEIGHTS_VECTOR[j]  for j in range(len(matrix[0]))] for i in range(len(matrix))]
    
    
def choose_ideal(matrix):
    max_vector = numpy.max(array(matrix), axis=0)
    min_vector = numpy.min(array(matrix), axis=0)
    ideal_best = [min_vector[j] if TYPE[j] else max_vector[j] for j in range(len(matrix[0]))]
    ideal_worst = [max_vector[j] if TYPE[j] else min_vector[j] for j in range(len(matrix[0]))]
    return ideal_best, ideal_worst
   

def calculate_separation(matrix, ideal_best, ideal_worst):
    separation_array_positive = [0 for i in range(len(matrix))]
    separation_array_negative = [0 for i in range(len(matrix))]
    
    for i in range(len(matrix)):
        temp_sum_positive = 0
        temp_sum_negative = 0
        for j in range(len(matrix[i])):
            temp_sum_positive += (matrix[i][j] - ideal_best[j])**2
            temp_sum_negative += (matrix[i][j] - ideal_worst[j])**2
        separation_array_positive[i], separation_array_negative[i] = sqrt(temp_sum_positive), sqrt(temp_sum_negative)
    return [separation_array_negative[i]/(separation_array_negative[i]+separation_array_positive[i]) for i in range(len(matrix))]
 
    
def get_best(hotels):
    matrix = create_matrix_criteria_alternatives(hotels)
    matrix = weighted_matrix(matrix)
    ideal_best, ideal_worst = choose_ideal(matrix)
    ci_array = calculate_separation(matrix, ideal_best, ideal_worst)
    
    return ci_array.index(min(ci_array))
   
