import os
import pandas as pd
import re
from regression_models import regression_models, food_calorie_database, weight_estimator
from calorie_estimation import estimate_calories

def calculate_average_error(test_folder, excel_path):
    total_error_percentage = 0
    total_images = 0

    # Duyệt qua tất cả các file trong thư mục test
    for image_name in os.listdir(test_folder):
        if image_name.lower().endswith(('.jpg', '.jpeg', '.png')):  # Chỉ xử lý file ảnh
            try:
                # Bỏ qua các ảnh có loại thực phẩm không hợp lệ (vd: mix)
                if "mix" in image_name:
                    continue

                # Tính toán kết quả cho từng ảnh
                result = estimate_calories(image_name, excel_path)

                # Tính phần trăm sai số cho từng ảnh
                actual_weight = result["actual_weight"]
                weight_error = result["weight_error"]
                error_percentage = (weight_error / actual_weight) * 100

                total_error_percentage += error_percentage
                total_images += 1
            except Exception as e:
                print(f"Lỗi khi xử lý {image_name}: {e}")

    # Tính % sai số trung bình
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