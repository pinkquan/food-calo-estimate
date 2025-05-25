import count_objects

TARGET = 200 

def get_augment_classes():
    class_counts = dict(count_objects.count_objects())
    return [int(cls) for cls, count in class_counts.items() if count < TARGET]
    


if __name__ == "__main__":
    augment_classes = get_augment_classes()
    print(augment_classes)