import pandas as pd
from itertools import combinations

file_path = "Horizontal_Format.xlsx"
min_support_percent = 0.6
min_confidence = 0.7

data = pd.read_excel(file_path, sheet_name="Sheet1")

transactions = []
for index, row in data.iterrows():
 raw_items = str(row["items"]).split(",")
 clean_items = []

 for item in raw_items:
   item = item.strip()
   if item != "":
     clean_items.append(item)

 transactions.append(set(clean_items))

print("Loaded", len(transactions), "transactions\n")

min_support_count = int(min_support_percent * len(transactions))


item_tidset = {}

for tid, transaction in enumerate(transactions):
 for item in transaction:
   if item not in item_tidset:
     item_tidset[item] = set()
   item_tidset[item].add(tid)

frequent_sets = {} # itemset → support_count

def eclat(current_set, candidate_list, current_tidset=None):

  if current_tidset is None:
     current_tidset = set()

  for i in range(len(candidate_list)):
    item_name = candidate_list[i][0]
    item_tid = candidate_list[i][1]

    if current_set == ():
       new_tidset = item_tid
    else:
       new_tidset = current_tidset.intersection(item_tid)

    support_count = len(new_tidset)

    if support_count >= min_support_count:

      new_itemset = tuple(sorted(current_set + (item_name,)))
      frequent_sets[new_itemset] = support_count

      next_list = []
      for j in range(i + 1, len(candidate_list)):
         next_item = candidate_list[j][0]
         next_tid = candidate_list[j][1]

         inter_tid = new_tidset.intersection(next_tid)
         inter_count = len(inter_tid)
         if inter_count >= min_support_count:
            next_list.append((next_item, inter_tid))

    if len(next_list) > 0:
      eclat(new_itemset, next_list, new_tidset)

sorted_items = sorted(item_tidset.items(), key=lambda x: len(x[1]), reverse=True)

print("Starting ECLAT...\n")
eclat((), sorted_items)

print("\n" + "="*60)
print("FREQUENT ITEMSETS (Support as Count)")
print("="*60)

level = 1
while True:
    level_sets = [s for s in frequent_sets if len(s) == level]

    if len(level_sets) == 0:
      break

    print("\nL", level, "(", len(level_sets), "itemsets ):")
    level_sorted = sorted(level_sets, key=lambda x: frequent_sets[x], reverse=True)

    for s in level_sorted:
       print(" ", s, "→ support_count =", frequent_sets[s])

    level += 1

print("\n" + "="*70)
print("STRONG RULES")
print("="*70)

for itemset in frequent_sets:
  if len(itemset) < 2:
     continue

  for k in range(1, len(itemset)):
     subsets = combinations(itemset, k)

     for left_side in subsets:
       left_side = tuple(sorted(left_side))
       right_side = tuple(sorted(set(itemset) - set(left_side)))

       sup_itemset = frequent_sets[itemset]
       sup_left = frequent_sets.get(left_side, 0)
       sup_right = frequent_sets.get(right_side, 0)

       if sup_left == 0:
         continue

       confidence_value = sup_itemset / sup_left

       if confidence_value >= min_confidence:
           lift_value = confidence_value / (sup_right / len(transactions)) if sup_right > 0 else 0

           print("\nRule:", left_side, "→", right_side)
           print(" support_count =", sup_itemset)
           print(" confidence =", round(confidence_value, 3))
           print(" lift =", round(lift_value, 3))