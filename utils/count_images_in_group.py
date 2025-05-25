import os

# origin dir
IMAGES_DIR = '../metadata/JPEGImages'
# class names
CLASS = ["apple", "banana", "bread", "bun", "doughnut", "egg", "fired_dough_twist", "grape", "lemon", "litchi", "mango", "mooncake", "orange", "pear", "peach", "plum", "qiwi", "sachima", "tomato"]


def count_images_in_class():
    res = {class_name: 0 for class_name in CLASS}
    for file in os.listdir(IMAGES_DIR):
        for class_name in CLASS:
            if class_name in file:
                res[class_name] += 1
    sorted_res = dict(sorted(res.items(), key=lambda item: item[1], reverse=True))
    return sorted_res


def print_images_name_in_class(dict_input):
    print('---------Number of images in each class----------')
    for class_name in dict_input.keys():
        print(f'Class `{class_name}`: {dict_input[class_name]}.')
    print('-------------------------')


if __name__ == "__main__":
    res = count_images_in_class()

    print_images_name_in_class(res)
