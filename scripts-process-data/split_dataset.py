import os
import random
import shutil
from tqdm import tqdm

# origin dir
ANNOTATIONS_DIR = '../metadata/Annotations'
IMAGES_DIR = '../metadata/JPEGImages'

# destination dir
OUT_IMAGES_DIR = '../dataset/images'
OUT_LABELS_DIR = '../dataset/labels'

# split ratio
train_ratio = 0.7
val_ratio = 0.2
test_ratio = 0.1


# make dirs
def make_dirs():
    for split in ['train', 'val', 'test']:
        os.makedirs(os.path.join(OUT_IMAGES_DIR, split), exist_ok=True)
        os.makedirs(os.path.join(OUT_LABELS_DIR, split), exist_ok=True)


# read file .xml
def get_all_files():
    return [f for f in os.listdir(ANNOTATIONS_DIR) if f.endswith('.xml')]


def split_files(files):
    random.shuffle(files)
    total = len(files)
    train_end = int(train_ratio * total)
    val_end = int((train_ratio + val_ratio) * total)
    return files[:train_end], files[train_end:val_end], files[val_end:]


def copy_files(files, split):
    for file in tqdm(files, desc=f"Copying {split}"):
        file_base = os.path.splitext(file)[0]
        img_src = os.path.join(IMAGES_DIR, file_base + '.JPG')
        ann_src = os.path.join(ANNOTATIONS_DIR, file)

        img_dst = os.path.join(OUT_IMAGES_DIR, split, file_base + '.JPG')
        ann_dst = os.path.join(OUT_LABELS_DIR, split, file)

        if os.path.exists(img_src) and os.path.exists(ann_src):
            shutil.copy(img_src, img_dst)
            shutil.copy(ann_src, ann_dst)


if __name__ == '__main__':
    make_dirs()
    files = get_all_files()
    train_files, val_files, test_files = split_files(files)

    copy_files(train_files, 'train')
    copy_files(val_files, 'val')
    copy_files(test_files, 'test')

    print(f"✅ Done splitting: {len(train_files)} train, {len(val_files)} val, {len(test_files)} test.")
