import pandas as pd
import re
from regression_models import regression_models, food_calorie_database, weight_estimator

def estimate_calories(image_name, excel_path):
    match = re.match(r"([a-zA-Z_]+[0-9]+)", image_name)
    if not match:
        raise ValueError("Tên ảnh không hợp lệ, không thể trích xuất ID.")
    food_id = match.group(1)
    food_type = re.match(r"([a-zA-Z_]+)", food_id).group(1)
    try:
        df = pd.read_excel(excel_path, sheet_name=food_type)
    except ValueError:
        raise ValueError(f"Không tìm thấy trang tính cho loại thực phẩm: {food_type}")
    df['weight(g)'] = df['weight(g)'].replace({',': '.'}, regex=True).astype(float)
    food_data = df[df['id'] == food_id]
    if food_data.empty:
        raise ValueError(f"Không tìm thấy dữ liệu cho ID: {food_id} trong trang tính {food_type}")
    volume = food_data.iloc[0]['volume(cm^3)']
    actual_weight = food_data.iloc[0]['weight(g)']
    estimated_weight = weight_estimator(food_type, volume)
    calorie_per_100g = food_calorie_database.get(food_type, food_calorie_database['default'])
    estimated_calories = (estimated_weight / 100) * calorie_per_100g
    weight_error = abs(actual_weight - estimated_weight)

    return {
        "food_id": food_id,
        "food_type": food_type,
        "volume": volume,
        "actual_weight": actual_weight,
        "estimated_weight": estimated_weight,
        "calorie_per_100g": calorie_per_100g,
        "estimated_calories": estimated_calories,
        "weight_error": weight_error
    }


if __name__ == "__main__":
    excel_path = "../../metadata/density.xls"
    image_name = "apple002S(4).JPG"

    result = estimate_calories(image_name, excel_path)
    print("Kết quả đánh giá:")
    for key, value in result.items():
        if key == "weight_error":
            print(f"=>{key}: {value}(g)")
        else:
            print(f"{key}: {value}")