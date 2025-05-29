import math
from ultralytics import YOLO


def load_model(model_path):
    try:
        model = YOLO(model_path)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None


def detect_objects(model, image, conf_threshold=0.66):
    results = model(image, conf=conf_threshold)  
    detections = []
    class_names = ['coin', 'apple', 'banana', 'bread', 'bun', 'doughnut', 'egg', 
                   'fired_dough_twist', 'grape', 'lemon', 'litchi', 'mango', 
                   'mooncake', 'orange', 'pear', 'peach', 'plum', 'qiwi', 'sachima', 'tomato']

    for r in results:
        boxes = r.boxes.xyxy.cpu().numpy()
        confs = r.boxes.conf.cpu().numpy()
        class_ids = r.boxes.cls.cpu().numpy().astype(int)
        
        for box, conf, class_id in zip(boxes, confs, class_ids):
            if conf >= conf_threshold:
                class_name = class_names[class_id] if class_id < len(class_names) else f"class_{class_id}"
                detections.append({
                    'bbox': box.astype(int).tolist(),
                    'confidence': float(conf),
                    'class_id': int(class_id),
                    'class_name': class_name
                })
    return detections


def coin_reference_scale(coin_detection):
    x1, y1, x2, y2 = coin_detection['bbox']
    coin_width = x2 - x1
    coin_height = y2 - y1
    coin_diameter_px = (coin_width + coin_height) / 2
    coin_diameter_mm = 25.0
    pixel_to_mm_ratio = coin_diameter_mm / coin_diameter_px
    
    return pixel_to_mm_ratio


def calculate_volume(food_detection, pixel_to_mm_ratio):
    x1, y1, x2, y2 = food_detection['bbox']
    width_mm = (x2 - x1) * pixel_to_mm_ratio
    height_mm = (y2 - y1) * pixel_to_mm_ratio
    food_type = food_detection['class_name']
    depth_factors = {
        'apple': 0.9,      # Hình cầu
        'banana': 0.5,     # Hình trụ cong
        'orange': 0.9,     # Hình cầu
        'bread': 0.4,      # Hình hộp chữ nhật
        'bun': 0.6,        # Hình tròn dẹt
        'doughnut': 0.3,   # Hình tròn lỗ giữa
        'egg': 0.8,        # Hình elipsoid
        'fired_dough_twist': 0.4,
        'grape': 0.9,
        'lemon': 0.8,
        'litchi': 0.9,
        'mango': 0.7,
        'mooncake': 0.3,
        'pear': 0.8,
        'peach': 0.9,
        'plum': 0.9,
        'qiwi': 0.9,
        'sachima': 0.5,
        'tomato': 0.9
    }
    depth_mm = min(width_mm, height_mm) * depth_factors.get(food_type, 0.5)

    if food_type in ['apple', 'orange', 'peach', 'plum', 'qiwi', 'litchi', 'grape', 'tomato']:
        # Hình cầu: V = (4/3) * π * r³
        radius_mm = min(width_mm, height_mm) / 2
        volume = (4/3) * math.pi * (radius_mm ** 3)
    elif food_type in ['banana']:
        # Chuối: elipsoid dẹt
        a = (width_mm) / 2
        b = (height_mm) / 2
        c = min(a, b) * 0.3  
        volume = (4/3) * math.pi * a * b * c
    elif food_type in ['lemon', 'mango']:
        # Elipsoid gần tròn hơn
        a = (width_mm) / 2
        b = (height_mm) / 2
        c = min(a, b) * 0.7
        volume = (4/3) * math.pi * a * b * c
    elif food_type in ['doughnut']:
        # Bánh donut: hình trụ rỗng
        outer_radius_mm = min(width_mm, height_mm) / 2
        inner_radius_mm = outer_radius_mm * 0.3  
        donut_depth_mm = min(width_mm, height_mm) * 0.3  
        volume = math.pi * (outer_radius_mm**2 - inner_radius_mm**2) * donut_depth_mm
    elif food_type in ['bun', 'mooncake']:
        # Bánh tròn dẹt: hình trụ dẹt
        radius_mm = min(width_mm, height_mm) / 2
        volume = math.pi * (radius_mm ** 2) * depth_mm
    elif food_type in ['pear']:
        # Hình giọt nước (~ bằng hình nón + nửa hình cầu)
        radius_mm = min(width_mm, height_mm) / 2
        cone_height_mm = max(width_mm, height_mm) - 2 * radius_mm
        volume_cone = (1/3) * math.pi * (radius_mm ** 2) * cone_height_mm
        volume_hemisphere = (2/3) * math.pi * (radius_mm ** 3)
        volume = volume_cone + volume_hemisphere
    else:
        # Mặc định: hình hộp chữ nhật (bread, fired_dough_twist, sachima, egg)
        volume = width_mm * height_mm * depth_mm

    return volume