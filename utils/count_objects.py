from collections import Counter
import os

CLASS_NAMES = ["coin", "apple", "banana", "bread", "bun", "doughnut", "egg", "fired_dough_twist",
               "grape", "lemon", "litchi", "mango", "mooncake", "orange", "pear", "peach",
               "plum", "qiwi", "sachima", "tomato"]


def count_objects():
    labels_dir = "../dataset/labels/train"
    counter = Counter()

    for file in os.listdir(labels_dir):
        if file.endswith(".txt"):
            with open(os.path.join(labels_dir, file)) as f:
                for line in f:
                    cls_id = line.strip().split()[0]
                    counter[cls_id] += 1
    return counter


if __name__ == "__main__":
    counter = count_objects()
    for class_id, class_name in enumerate(CLASS_NAMES):
        print(f'Class `{class_name}`: {counter[str(class_id)]}')
