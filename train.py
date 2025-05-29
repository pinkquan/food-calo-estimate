from ultralytics import YOLO
import multiprocessing

model = YOLO('yolov8n.pt')


if __name__ == "__main__":
    model.train(
        data='dataset/data.yaml',
        epochs=50,
        imgsz=640,
        batch=32,
        project='runs',
        name='food_calo_project',
        device=0,
        patience=10,           
        save_period=10,       
        workers=8,            
        optimizer='AdamW',     
        cos_lr=True,     
        augment=True
    )

