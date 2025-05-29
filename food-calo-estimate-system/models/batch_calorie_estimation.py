import os
import pandas as pd
import re
from regression_models import regression_models, food_calorie_database, weight_estimator
from calorie_estimation import estimate_calories

def calculate_average_error(test_folder, excel_path):
    total_error_percentage = 0
    total_images = 0

    for image_name in os.listdir(test_folder):
        if image_name.lower().endswith(('.jpg', '.jpeg', '.png')):  # Chỉ xử lý file ảnh
            try:
                if "mix" in image_name:
                    continue

                result = estimate_calories(image_name, excel_path)

                actual_weight = result["actual_weight"]
                weight_error = result["weight_error"]
                error_percentage = (weight_error / actual_weight) * 100

                total_error_percentage += error_percentage
                total_images += 1
            except Exception as e:
                print(f"Lỗi khi xử lý {image_name}: {e}")

    if total_images == 0:
        raise ValueError("Không có ảnh hợp lệ trong thư mục test.")
    
    average_error_percentage = total_error_percentage / total_images
    return average_error_percentage


if __name__ == "__main__":
    test_folder = "../../dataset/images/test"
    excel_path = "../../metadata/density.xls"

    try:
        average_error_percentage = calculate_average_error(test_folder, excel_path)
        print(f"% Sai số trung bình: {average_error_percentage:.2f}%")
    except Exception as e:
        print(f"Lỗi: {e}")