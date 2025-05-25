"""
Module chứa các mô hình hồi quy để ước tính khối lượng từ thể tích 
và cơ sở dữ liệu calorie của các loại thực phẩm.

Các mô hình được xây dựng từ dữ liệu trong file excel về mối quan hệ giữa thể tích và khối lượng.
"""

# Hệ số hồi quy volume → weight theo từng loại thực phẩm
# Mô hình: weight = coefficient * volume + intercept
regression_models = {
    'apple': (0.689415, 30.876216),
    'banana': (0.626376, 48.26164),
    'bread': (0.006667, 26.875),
    'bun': (0.194086, 35.21191),
    'doughnut': (0.173122, 25.88878),
    'egg': (1.07, 4.7),
    'fired_dough_twist': (0.159125, 30.55875),
    'grape': (1.088095, -41.642857),
    'lemon': (0.163333, 77.6),
    'litchi': (1.1975, -8.375),
    'mango': (0.978617, 10.01383),
    'mooncake': (0.734314, 13.257843),
    'orange': (0.399855, 110.877126),
    'pear': (0.943484, 1.907932),
    'peach': (1.073654, -5.769231),
    'plum': (1.03, -2.7),
    'qiwi': (0.907095, 9.873311),
    'sachima': (0.2725, -8.3),
    'tomato': (0.666538, 58.815385),
}

# Cơ sở dữ liệu calorie cho mỗi loại thực phẩm (calories/100g)
food_calorie_database = {
    # Trái cây
    'apple': 52,      # táo
    'banana': 89,     # chuối
    'orange': 47,     # cam
    'grape': 67,      # nho
    'lemon': 29,      # chanh vàng
    'litchi': 66,     # vải(lychee)
    'mango': 60,      # xoài
    'pear': 57,       # lê
    'peach': 39,      # đài
    'plum': 46,       # mận
    'qiwi': 61,       # kiwi
    'tomato': 18,     # cà chua
    
    # Bánh & đồ ngọt
    'bread': 265,     # bánh mì gối
    'bun': 310,       # bánh bao
    'doughnut': 450,  # bánh donut
    'mooncake': 370,  # bánh trung thu
    'fired_dough_twist': 460,  # quẩy
    'sachima': 325,   # bánh sachima
    
    # Khác
    'egg': 155,       # trứng
    
    # Giá trị mặc định cho các loại thực phẩm chưa được định nghĩa
    'default': 100    # 100 kcal per 100g
}


def weight_estimator(food_type, volume):
    """
    Ước tính khối lượng (g) của thực phẩm dựa trên thể tích (cm³)
    sử dụng mô hình hồi quy tuyến tính.
    
    Parameters:
    -----------
    food_type : str
        Loại thực phẩm
    volume : float
        Thể tích của thực phẩm (cm³)
        
    Returns:
    --------
    float
        Khối lượng ước tính (g)
    """
    if food_type in regression_models:
        coefficient, intercept = regression_models[food_type]
        
        # Áp dụng mô hình hồi quy: weight = coefficient * volume + intercept
        weight = coefficient * volume + intercept
        return max(0, weight)  # Đảm bảo khối lượng không âm
    else:
        # Nếu không có mô hình cho loại thực phẩm, giả định tỷ trọng là 0.8 g/cm³
        return volume * 0.8