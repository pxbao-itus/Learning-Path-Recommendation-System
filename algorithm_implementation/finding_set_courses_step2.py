import itertools

from concurrent.futures.thread import ThreadPoolExecutor
from py2neo import Graph

from utilities.query_for_algorithm import *
from constants.algorithm_constants import *

graph = Graph()