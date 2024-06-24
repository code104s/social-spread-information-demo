import sys; sys.path.append('..')
import src.seed as seed
from src.data import data_load
from src.influence import influence_count, coverage, precision

# Parameters
path = '../data/example.txt'  # dataset file path
init_rate = 0.01  # tỷ lệ ảnh hưởng ban đầu, khuyến nghị từ 0 đến 0,05
threshold = 1  # ngưỡng ảnh hưởng, khuyến nghị từ 0 đến 1

# Seed selection policy, option: 'degree', 'random',
# 'degree_discount', 'degree_neighbor', 'degree_neighbor_fix', 'mia'
policy = 'mia'

# Seed selection
nodes, edges = data_load(path)
seeds_number = int(len(nodes) * init_rate)

if policy == 'degree':
    seeds = seed.degree(edges, seeds_number)
elif policy == 'random':
    seeds = seed.random(nodes, seeds_number)
elif policy == 'degree_discount':
    seeds = seed.degree_discount(edges, seeds_number)
elif policy == 'degree_neighbor':
    seeds = seed.degree_neighbor(edges, seeds_number)
elif policy == 'degree_neighbor_fix':
    seeds = seed.degree_neighbor_fix(edges, seeds_number)
elif policy == 'mia':
    seeds = seed.mia(nodes, edges, seeds_number)
elif policy == 'greedy':
    seeds = seed.greedy(edges, seeds_number)
else:
    raise NameError("Unknown policy")

print(f'Number of Seeds: {len(seeds)}')

print(f'Selected seeds: {seeds}')

# Tính số lượng ảnh hưởng cuối cùng
influence_number = influence_count(nodes, edges, seeds, threshold)
print(f'Final Influence Number: {influence_number}')

# Tính độ phủ
coverage = coverage(nodes, influence_number)
print(f'Coverage: {coverage}')

# Tính độ chính xác
predicted_positives = len(seeds)
true_positives = influence_number
precision = precision(true_positives, predicted_positives)
print(f'Precision: {precision}')

