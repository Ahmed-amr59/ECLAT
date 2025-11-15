
import pandas as pd
from itertools import combinations

filePath = "Horizontal_Format.xlsx"

data = pd.read_excel(filePath, sheet_name="Sheet1")

transactions = []
# read transactions from Excel Sheet
for index, row in data.iterrows():
    transactionsItem = str(row["items"]).split(",")
    cleanItems = []

    for item in transactionsItem:
        item = item.strip()
        if item != "":
            cleanItems.append(item)

    transactions.append(set(cleanItems))

# set Support & Confidence
minSup = 0.6
minCon = 0.7


minSupCount = int(minSup * len(transactions))

itemTidSet = {}
# From Horizontal to Vertical format
for tid, transaction in enumerate(transactions):
    for item in transaction:
        if item not in itemTidSet:
            itemTidSet[item] = set()
        itemTidSet[item].add(tid)

freqSets = {}


# freq itemsets
def eclat(currentSet, candidateList, currentTidSet=None):
    if currentTidSet is None:
        currentTidSet = set()

    for i in range(len(candidateList)):
        item_name = candidateList[i][0]
        item_tid = candidateList[i][1]

        if currentSet == ():
            new_tidset = item_tid
        else:
            new_tidset = currentTidSet.intersection(item_tid)

        supCount = len(new_tidset)

        if supCount >= minSupCount:

            new_itemset = tuple(sorted(currentSet + (item_name,)))
            freqSets[new_itemset] = supCount

            next_list = []
            for j in range(i + 1, len(candidateList)):
                next_item = candidateList[j][0]
                next_tid = candidateList[j][1]
                inter_tid = new_tidset.intersection(next_tid)
                inter_count = len(inter_tid)
                if inter_count >= minSupCount:
                    next_list.append((next_item, inter_tid))

            if len(next_list) > 0:
                eclat(new_itemset, next_list, new_tidset)


sorted_items = sorted(itemTidSet.items(), key=lambda x: len(x[1]), reverse=True)

eclat((), sorted_items)

print("All Frequent Itemsets:")
level = 1
while True:
    level_sets = [s for s in freqSets if len(s) == level]

    if len(level_sets) == 0:
        break


    level_sorted = sorted(level_sets, key=lambda x: freqSets[x], reverse=True)

    for s in level_sorted:
        print(" ", s, "==> support_count =", freqSets[s])

    level += 1

print("\nStrong Rules:")

for itemset in freqSets:
    if len(itemset) < 2:
        continue

    for k in range(1, len(itemset)):
        subsets = combinations(itemset, k)

        for left_side in subsets:
            left_side = tuple(sorted(left_side))
            right_side = tuple(sorted(set(itemset) - set(left_side)))

            sup_itemset = freqSets[itemset]
            sup_left = freqSets.get(left_side, 0)
            sup_right = freqSets.get(right_side, 0)

            if sup_left == 0:
                continue

            confidence_value = sup_itemset / sup_left

            if confidence_value >= minCon:
                lift_value = confidence_value / (sup_right / len(transactions)) if sup_right > 0 else 0

                print("\nRule:", left_side, "==>", right_side)
                print(" support count =", sup_itemset)
                print(" confidence =", round(confidence_value, 3))
                print(" lift =", round(lift_value, 3))