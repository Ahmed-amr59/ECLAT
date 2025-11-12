import pandas as pd
from itertools import combinations


class ECLAT:
    def __init__(self, min_support=0.5, min_confidence=0.5):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.itemsets = {}
        self.transactions = []

    def load_data(self, file_path):
        data = pd.read_excel(file_path, sheet_name='Sheet1')
        for index, row in data.iterrows():
            items = row['items'].split(',')
            self.transactions.append(set(items))

    def vertical_format(self):
        item_dict = {}
        for idx, transaction in enumerate(self.transactions):
            for item in transaction:
                if item not in item_dict:
                    item_dict[item] = set()
                item_dict[item].add(idx)
        return item_dict

    def eclat(self, item_dict, min_support):
        freq_itemsets = {}
        items = list(item_dict.keys())
        for length in range(1, len(items) + 1):
            for combo in combinations(items, length):
                common_transactions = set.intersection(*(item_dict[item] for item in combo))
                if len(common_transactions) / len(self.transactions) >= min_support:
                    freq_itemsets[combo] = len(common_transactions)
        return freq_itemsets

    def generate_association_rules(self, freq_itemsets):
        rules = []
        for itemset, support in freq_itemsets.items():
            # Generate all subsets of the itemset
            for i in range(1, len(itemset)):
                for subset in combinations(itemset, i):
                    # Use the correct way to retrieve support for the subset
                    subset_support = sum(1 for idx in self.transactions if set(subset).issubset(idx))
                    if subset and subset_support > 0:
                        conf = support / subset_support
                        if conf >= self.min_confidence:
                            rules.append((subset, tuple(set(itemset) - set(subset)), support, conf))
        return rules

    def calculate_lift(self, rule, freq_itemsets):
        # Rule is of the form (A, B, support, confidence)
        support_A = freq_itemsets[rule[0]]
        support_B = freq_itemsets[rule[1]]
        return rule[2] / (support_A * support_B)

    def run(self, file_path):
        self.load_data(file_path)
        item_dict = self.vertical_format()
        freq_itemsets = self.eclat(item_dict, self.min_support)

        print("Frequent Itemsets:")
        for items, support in freq_itemsets.items():
            print(f"Itemset: {items}, Support: {support}")

        rules = self.generate_association_rules(freq_itemsets)

        print("\nAssociation Rules:")
        for rule in rules:
            lift = self.calculate_lift(rule, freq_itemsets)
            print(f"Rule: {rule[0]} -> {rule[1]}, Support: {rule[2]}, Confidence: {rule[3]}, Lift: {lift}")


if __name__ == "__main__":
    eclat = ECLAT(min_support=.8, min_confidence=0.7)
    eclat.run('Horizontal_Format.xlsx')