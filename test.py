# simple_eclat_fixed.py
# Very Simple & Correct ECLAT - No Errors!

import pandas as pd
from itertools import combinations

# ========================= CONFIG =========================
filePath = "Horizontal_Format.xlsx"
minSup = 0.6          # Change here to test
minCon = 0.7          # Change here to test
# =========================================================

# 1. Load data
data = pd.read_excel(filePath, sheet_name="Sheet1")
transactions = []
for index, row in data.iterrows():
    items = [x.strip() for x in str(row['items']).split(',') if x.strip()]
    transactions.append(set(items))

print(f"Loaded {len(transactions)} transactions\n")

# 2. Vertical format: item → tidset
itemDict = {}
for tid, trans in enumerate(transactions):
    for item in trans:
        if item not in itemDict:
            itemDict[item] = set()
        itemDict[item].add(tid)

# 3. ECLAT Mining
freqItemSets = {}  # tuple → support

def eclat(prefix, items_list, prefix_tidset=None):
    if prefix_tidset is None:
        # First call: get tidset from first item
        prefix_tidset = items_list[0][1] if prefix else set()

    for i in range(len(items_list)):
        item, tidset = items_list[i]
        current_tidset = tidset if prefix == () else prefix_tidset & tidset
        support = len(current_tidset) / len(transactions)

        if support >= minSup:
            new_itemset = tuple(sorted(prefix + (item,)))
            freqItemSets[new_itemset] = support

            # Build next candidates
            next_candidates = []
            for j in range(i + 1, len(items_list)):
                item2, tidset2 = items_list[j]
                inter = current_tidset & tidset2
                if len(inter) / len(transactions) >= minSup:
                    next_candidates.append((item2, inter))

            if next_candidates:
                eclat(new_itemset, next_candidates, current_tidset)

# Start mining
min_support_count = minSup * len(transactions)
items_sorted = sorted(itemDict.items(), key=lambda x: len(x[1]), reverse=True)

print("Starting ECLAT mining...")
eclat((), items_sorted)

# 4. Print Frequent Itemsets
print("\n" + "="*60)
print("FREQUENT ITEMSETS")
print("="*60)

for size in range(1, 10):
    current = [itemset for itemset in freqItemSets.keys() if len(itemset) == size]
    if not current:
        break
    print(f"\nL{size} ({len(current)} itemsets):")
    for itemset in sorted(current, key=lambda x: freqItemSets[x], reverse=True):
        print(f"  {itemset}  →  support = {freqItemSets[itemset]:.3f}")

# 5. Print Strong Rules with Lift
print("\n" + "="*70)
print(f"STRONG RULES (min_sup={minSup}, min_conf={minCon})")
print("="*70)

for itemset in list(freqItemSets.keys()):
    if len(itemset) < 2:
        continue
    for i in range(1, len(itemset)):
        for subset in combinations(itemset, i):
            antecedent = tuple(sorted(subset))
            consequent = tuple(sorted(set(itemset) - set(subset)))

            sup_all = freqItemSets[itemset]
            sup_ant = freqItemSets.get(antecedent, 0)
            if sup_ant == 0:
                continue

            confidence = sup_all / sup_ant
            if confidence < minCon:
                continue

            sup_con = freqItemSets.get(consequent, 0)
            lift = confidence / sup_con if sup_con > 0 else float('inf')

            print(f"\n{antecedent}  →  {consequent}")
            print(f"    support     = {sup_all:.3f}")
            print(f"    confidence  = {confidence:.3f}")
            print(f"    lift        = {lift:.3f}")

print("\nECLAT Completed Successfully!")