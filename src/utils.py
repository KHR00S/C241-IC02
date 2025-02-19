import io
import numpy as np
import torchvision.transforms as transforms
import psycopg2
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()

def preprocess_image_atas(image):
    transform = transforms.Compose([
        transforms.Resize((640, 640)),
        transforms.ToTensor()
    ])
    img = transform(image)  # Convert image to tensor
    img = np.array(img)    # Convert tensor to numpy array
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

def preprocess_image_depan(image):
    IMAGE_SIZE = 416
    img_resized = image.resize((IMAGE_SIZE, IMAGE_SIZE))
    img = np.array(img_resized)
    img = np.transpose(img, (2, 0, 1))  # Change dimensions from (224, 224, 3) to (3, 224, 224)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0
    return img

def preprocess_image_bawah(image):
    input_size=(640, 640)
    transform = transforms.Compose([
        transforms.Resize(input_size),
        transforms.ToTensor(),
    ])
    img = transform(image).unsqueeze(0).numpy()
    return img

def resize_image(image):
    target_size=(416, 416)

    # Resize the image
    image = image.resize(target_size, Image.Resampling.LANCZOS)

    # Convert the resized image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img= img_byte_arr.getvalue()
    return img

def connect_to_database():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn