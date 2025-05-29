from flask import Flask, request, jsonify, render_template, url_for, flash, redirect
import cv2
import numpy as np
from werkzeug.utils import secure_filename
from models.model_utils import load_model, detect_objects, calculate_volume, coin_reference_scale
from models.regression_models import weight_estimator, food_calorie_database
from config.database import food_records, users
from database.models import FoodRecord, User
from flask_login import LoginManager, current_user, login_required
from auth import auth
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'your-secret-key'

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(ObjectId(user_id))

app.register_blueprint(auth)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

model_path = 'models/last.pt'
try:
    detection_model = load_model(model_path)
except Exception as e:
    print(f"Error loading model: {e}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
@login_required
def analyze_food():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            file_content = file.read()
            image = cv2.imdecode(np.frombuffer(file_content, np.uint8), cv2.IMREAD_COLOR)
            
            if image is None:
                return jsonify({'error': 'Cannot read image'}), 400
                
            detections = detect_objects(detection_model, image)
            
            coin_detection = None
            food_detections = []
            
            for det in detections:
                if det['class_name'] == 'coin':
                    coin_detection = det
                else:
                    food_detections.append(det)
            
            if not coin_detection:
                return jsonify({
                    'error': 'Reference coin not found in image',
                    'detections': detections
                }), 400
            
            pixel_to_mm_ratio = coin_reference_scale(coin_detection)
            results = []
            
            for food in food_detections:
                food_volume = calculate_volume(food, pixel_to_mm_ratio)
                food_volume_cm3 = food_volume / 1000
                food_weight = weight_estimator(food['class_name'], food_volume_cm3)
                calorie = food_calorie_database.get(food['class_name'], 0) * food_weight / 100

                results.append({
                    'name': food['class_name'],
                    'confidence': round(food['confidence'], 2),  # Changed from * 100 to proper percentage
                    'volume_cm3': round(food_volume_cm3, 2),
                    'weight_g': round(food_weight, 2),
                    'calories': round(calorie, 2)
                })

            total_calories = sum(item['calories'] for item in results)
            
            food_record = FoodRecord(
                user_id=current_user._id,
                results=results,
                total_calories=total_calories
            )
            
            food_records.insert_one(food_record.to_dict())
            
            return jsonify({
                'results': results,
                'total_calories': total_calories
            })
        
        return jsonify({'error': 'Invalid file type'}), 400
        
    except Exception as e:
        print(f"Error in analyze_food: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/history')
@login_required
def view_history():
    user_records = list(food_records.find(
        {"user_id": current_user._id}
    ).sort("created_at", -1))
    
    return render_template('history.html', records=user_records)

@app.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    try:
        username = request.form.get('username')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password and new_password != confirm_password:
            flash('Mật khẩu xác nhận không khớp', 'error')
            return redirect(url_for('view_history'))
        
        if current_user.update_profile(username=username, new_password=new_password):
            flash('Cập nhật thông tin thành công!', 'success')
        else:
            flash('Không có thông tin nào được thay đổi', 'info')
            
        return redirect(url_for('view_history'))
        
    except Exception as e:
        flash(f'Có lỗi xảy ra: {str(e)}', 'error')
        return redirect(url_for('view_history'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)