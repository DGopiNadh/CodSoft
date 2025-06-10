Face Recognition

Description

main.py uses OpenCV LBPH to train on labeled face images and recognize faces in a test image.

Setup
1.	Python 3.8+
2.	Dataset: faces/person1/image1.jpg, etc.
3.	Test image: faces/test.jpg

Install dependencies:

pip install -r requirements.txt

Files Organization

FaceRecognition/

├── main.py

├── requirements.txt

├── README.md

└── faces/
   
    ├── person1/
    
    │   ├── image1.jpg
    
    │   ├── image2.jpg
    
    ├── person2/
    
    │   ├── image3.jpg
    
    └── test.jpg
