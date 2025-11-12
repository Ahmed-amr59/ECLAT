import pandas as pd
from itertools import combinations

file_path = "Horizontal_Format.xlsx"
data = pd.read_excel(file_path, sheet_name="Sheet1")

transactions = [set(row['items'].split(',')) for index, row in data.iterrows()]

min_sup = 0.8
min_conf = 0.6

item_dict = {}
for tid, trns in enumerate(transactions):
    for item in trns:
        if item not in item_dict:
            item_dict[item] = set()
        item_dict[item].add(tid)

freqItemsets = {}

items = list(item_dict.keys())
for length in range(1, len(items) + 1):
    for comb in combinations(items, length):
        common_tids = set.intersection(*(item_dict[i] for i in comb))
        support = len(common_tids) / len(transactions)
        if support >= min_sup:
            freqItemsets[comb] = support

print("freq items:\n")
for items, support in freqItemsets.items():
    print(f"{items} support={support:.3f}")

print("\nassociation rules:")
for itemset, support in freqItemsets.items():
    if len(itemset) > 1:
        for i in range(1, len(itemset)):
            for subset in combinations(itemset, i):
                subset = set(subset)
                remain = set(itemset) - subset
                subset_support = sum(1 for t in transactions if subset.issubset(t)) / len(transactions)
                if subset_support > 0:
                    confidence = support / subset_support
                    if confidence >= min_conf:
                        print(f"\n{tuple(subset)}→{tuple(remain)}:\nsupport = {support:.3f}\nconfidence = {confidence:.3f}")