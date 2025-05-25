import numpy as np
from sklearn.linear_model import LinearRegression

# Dữ liệu không có ngoại lai (loại bỏ bread003, bread005, bread007)
volume = np.array([140, 150, 170, 140]).reshape(-1, 1)
weight = np.array([26.6, 28.8, 27.7, 28.4])

model = LinearRegression().fit(volume, weight)
a = model.coef_[0]
b = model.intercept_
print(f"Hệ số hồi quy bread: ({a:.6f}, {b:.6f})")
