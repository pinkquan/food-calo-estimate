# 🍱 Food Calorie Estimation System

A lightweight and efficient system for estimating the **calories of food items from images**, using deep learning techniques such as **YOLOv8** for object detection and **Linear Regression** for calorie prediction.

## 📌 Overview

This project aims to automate the process of calorie estimation in meals by detecting and identifying food items through images and predicting their respective calorie values using pre-trained machine learning models.

<p align="center">
  <img src="docs/demo_result.png" width="600" alt="Sample Output">
</p>

---

## 🚀 Features

- 🍔 Detects food items using **YOLOv8**
- 🔢 Predicts calories using **linear regression**
- 🖼️ Works with static images
- 🧪 Ready for integration in diet tracking or health assistant applications

---

## 🛠️ Tech Stack

- `Python 3.10`
- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)
- `OpenCV`
- `Pandas`, `NumPy`, `Matplotlib`
- `Scikit-learn` (for linear regression)

---
## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/pinkquan/food-calo-estimate.git
cd food-calo-estimate
```

### 2. Create virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download model weights
`Place YOLOv8 trained weights and regression model in the models/ directory.`

## ▶️ Usage
`cd food-calo-estimate-system and run app.pypy`

## 🤝 Contributing
`Contributions are welcome! Please open an issue or pull request.`

## 🙋‍♂️ Author
`Pink Quan`
<a href="https://github.com/pinkquan">GitHub Profile</a>