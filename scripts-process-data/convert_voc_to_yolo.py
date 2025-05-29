import os
import xml.etree.ElementTree as ET
from tqdm import tqdm


CLASS = ["coin", "apple", "banana", "bread", "bun", "doughnut", "egg", 
         "fired_dough_twist", "grape", "lemon", "litchi", "mango", 
         "mooncake", "orange", "pear", "peach", "plum", "qiwi", 
         "sachima", "tomato"]

class_name_to_id = {name: idx for idx, name in enumerate(CLASS)}

XML_ROOT = "../dataset/labels"
SPLITS = ["train", "val", "test"]


def convert_bbox(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x_center = (box[0] + box[2]) / 2.0
    y_center = (box[1] + box[3]) / 2.0
    w = box[2] - box[0]
    h = box[3] - box[1]
    return (x_center * dw, y_center * dh, w * dw, h * dh)


def convert_xml_file(xml_path, txt_output_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    size = root.find("size")
    w = int(size.find("width").text)
    h = int(size.find("height").text)

    with open(txt_output_path, "w") as out_file:
        for obj in root.findall("object"):
            class_name = obj.find("name").text
            if class_name not in class_name_to_id:
                continue  
            class_id = class_name_to_id[class_name]

            bndbox = obj.find("bndbox")
            xmin = int(bndbox.find("xmin").text)
            ymin = int(bndbox.find("ymin").text)
            xmax = int(bndbox.find("xmax").text)
            ymax = int(bndbox.find("ymax").text)

            bbox = convert_bbox((w, h), (xmin, ymin, xmax, ymax))
            out_file.write(f"{class_id} {' '.join(f'{x:.6f}' for x in bbox)}\n")


if __name__ == "__main__":
    for split in SPLITS:
        xml_dir = os.path.join(XML_ROOT, split)
        out_dir = os.path.join(XML_ROOT, split)

        xml_files = [f for f in os.listdir(xml_dir) if f.endswith(".xml")]

        for xml_file in tqdm(xml_files, desc=f"Converting {split}"):
            xml_path = os.path.join(xml_dir, xml_file)
            txt_output_path = os.path.join(out_dir, xml_file.replace(".xml", ".txt"))
            convert_xml_file(xml_path, txt_output_path)

            os.remove(xml_path)  

    print("Done converting XML to YOLO format.")
