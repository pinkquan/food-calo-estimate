import math
from ultralytics import YOLO

def load_model(model_path):
    """
    Load YOLOv8 PyTorch model (.pt)
    """
    try:
        model = YOLO(model_path)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None


def detect_objects(model, image, conf_threshold=0.66):
    """
    Thực hiện phát hiện đối tượng trên ảnh với YOLOv8 PyTorch
    Args:
        model: Model YOLO đã load
        image: Ảnh đầu vào
        conf_threshold: Ngưỡng confidence (default: 0.7)
    """
    # Dự đoán với confidence threshold
    results = model(image, conf=conf_threshold)  # Set confidence threshold here
    detections = []
    class_names = ['coin', 'apple', 'banana', 'bread', 'bun', 'doughnut', 'egg', 
                   'fired_dough_twist', 'grape', 'lemon', 'litchi', 'mango', 
                   'mooncake', 'orange', 'pear', 'peach', 'plum', 'qiwi', 'sachima', 'tomato']

    for r in results:
        boxes = r.boxes.xyxy.cpu().numpy()
        confs = r.boxes.conf.cpu().numpy()
        class_ids = r.boxes.cls.cpu().numpy().astype(int)
        
        for box, conf, class_id in zip(boxes, confs, class_ids):
            # Double check confidence threshold
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
    """
    Tính toán tỷ lệ pixel-to-mm từ đồng xu tham chiếu
    Đồng xu có đường kính 25mm
    """
    x1, y1, x2, y2 = coin_detection['bbox']
    
    # Tính đường kính đồng xu trên ảnh (pixels)
    coin_width = x2 - x1
    coin_height = y2 - y1
    
    # Lấy trung bình của width và height để ước tính đường kính
    coin_diameter_px = (coin_width + coin_height) / 2
    
    # Đường kính thực của đồng xu (25mm)
    coin_diameter_mm = 25.0
    
    # Tỷ lệ pixel-to-mm
    pixel_to_mm_ratio = coin_diameter_mm / coin_diameter_px
    
    return pixel_to_mm_ratio

def calculate_volume(food_detection, pixel_to_mm_ratio):
    """
    Tính toán thể tích (ước lượng) của thực phẩm dựa trên bounding box
    và tỷ lệ pixel-to-mm. Kết quả trả về là mm³.
    """
    x1, y1, x2, y2 = food_detection['bbox']

    # Kích thước thực của bounding box (mm)
    width_mm = (x2 - x1) * pixel_to_mm_ratio
    height_mm = (y2 - y1) * pixel_to_mm_ratio

    # Giả định về độ dày (theo loại thực phẩm)
    food_type = food_detection['class_name']

    # Depth estimation factors (ước lượng độ dày dựa trên kích thước 2D)
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

    # Tính thể tích (mm³)
    if food_type in ['apple', 'orange', 'peach', 'plum', 'qiwi', 'litchi', 'grape', 'tomato']:
        # Hình cầu: V = (4/3) * π * r³
        radius_mm = min(width_mm, height_mm) / 2
        volume = (4/3) * math.pi * (radius_mm ** 3)
    elif food_type in ['banana']:
        # Chuối: elipsoid dẹt, chiều dày nhỏ hơn nhiều so với chiều dài
        a = (width_mm) / 2
        b = (height_mm) / 2
        c = min(a, b) * 0.3  # Độ dày chỉ khoảng 30% bán kính nhỏ nhất
        volume = (4/3) * math.pi * a * b * c
    elif food_type in ['lemon', 'mango']:
        # Elipsoid gần tròn hơn
        a = (width_mm) / 2
        b = (height_mm) / 2
        c = min(a, b) * 0.7
        volume = (4/3) * math.pi * a * b * c
    elif food_type in ['doughnut']:
        # Đặc biệt cho bánh donut: hình trụ rỗng
        outer_radius_mm = min(width_mm, height_mm) / 2
        inner_radius_mm = outer_radius_mm * 0.3  # Giả sử lỗ chiếm 30% đường kính
        donut_depth_mm = min(width_mm, height_mm) * 0.3  # Độ dày
        volume = math.pi * (outer_radius_mm**2 - inner_radius_mm**2) * donut_depth_mm
    elif food_type in ['bun', 'mooncake']:
        # Bánh tròn dẹt: hình trụ dẹt
        radius_mm = min(width_mm, height_mm) / 2
        volume = math.pi * (radius_mm ** 2) * depth_mm
    elif food_type in ['pear']:
        # Hình giọt nước (xấp xỉ bằng hình nón + nửa hình cầu)
        radius_mm = min(width_mm, height_mm) / 2
        cone_height_mm = max(width_mm, height_mm) - 2 * radius_mm
        volume_cone = (1/3) * math.pi * (radius_mm ** 2) * cone_height_mm
        volume_hemisphere = (2/3) * math.pi * (radius_mm ** 3)
        volume = volume_cone + volume_hemisphere
    else:
        # Mặc định: hình hộp chữ nhật (bread, fired_dough_twist, sachima, egg)
        volume = width_mm * height_mm * depth_mm

    return volume