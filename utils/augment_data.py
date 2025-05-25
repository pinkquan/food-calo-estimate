import os
import albumentations as A
import cv2
import random
from tqdm import tqdm
from collections import defaultdict
import get_augment_class

# Cấu hình
IMAGES_DIR = '../dataset/images/train'
LABELS_DIR = '../dataset/labels/train'
AUG_IMAGES_DIR = '../dataset/images/train_aug'
AUG_LABELS_DIR = '../dataset/labels/train_aug'
TARGET_PER_CLASS = 200
CLASSES_TO_AUG = get_augment_class.get_augment_classes()

os.makedirs(AUG_IMAGES_DIR, exist_ok=True)
os.makedirs(AUG_LABELS_DIR, exist_ok=True)

# Pipeline augment
transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.5),
    A.Rotate(limit=15, p=0.5),
    A.GaussNoise(p=0.3),
    A.RandomScale(scale_limit=0.2, p=0.5),
], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels'], min_visibility=0.3))

def load_labels(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines]

def save_labels(path, lines):
    with open(path, 'w') as f:
        f.write('\n'.join(lines))

if __name__ == "__main__":
    cls_counts = defaultdict(int)

    for file in os.listdir(LABELS_DIR):
        if not file.endswith('.txt'):
            continue
        with open(os.path.join(LABELS_DIR, file)) as f:
            for line in f:
                cls_id = int(line.strip().split()[0])
                cls_counts[cls_id] += 1

    for file in tqdm(os.listdir(LABELS_DIR)):
        if not file.endswith('.txt'):
            continue

        label_path = os.path.join(LABELS_DIR, file)
        image_path = os.path.join(IMAGES_DIR, file.replace(".txt", ".jpg"))
        if not os.path.exists(image_path):
            image_path = image_path.replace(".jpg", ".JPG")  # fallback

        lines = load_labels(label_path)

        bboxes = []
        labels = []
        for line in lines:
            parts = line.strip().split()
            cls_id = int(parts[0])
            bbox = list(map(float, parts[1:]))
            bboxes.append(bbox)
            labels.append(cls_id)

        augmentable_indices = [i for i, cls_id in enumerate(labels) if cls_id in CLASSES_TO_AUG and cls_counts[cls_id] < TARGET_PER_CLASS]

        if not augmentable_indices:
            continue

        img = cv2.imread(image_path)

        for i in augmentable_indices:
            cls_id = labels[i]
            if cls_counts[cls_id] >= TARGET_PER_CLASS:
                continue  

            # Augment
            try:
                augmented = transform(
                    image=img,
                    bboxes=[bboxes[i]],
                    class_labels=[labels[i]]
                )
            except Exception as e:
                continue 

            aug_img = augmented['image']
            aug_bbox = augmented['bboxes'][0]
            aug_label = augmented['class_labels'][0]

            cls_counts[cls_id] += 1

            new_name = f"aug_{cls_id}_{random.randint(10000,99999)}"
            cv2.imwrite(os.path.join(AUG_IMAGES_DIR, new_name + ".jpg"), aug_img)
            save_labels(os.path.join(AUG_LABELS_DIR, new_name + ".txt"), [f"{aug_label} {' '.join(map(str, aug_bbox))}"])

            if cls_counts[cls_id] >= TARGET_PER_CLASS:
                break  
