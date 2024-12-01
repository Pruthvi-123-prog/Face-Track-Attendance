from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.hashers import check_password
import cv2
import face_recognition
import numpy as np
import json
import os
import base64

# Path to the JSON file
DATA_FILE = 'students.json'

def register_student(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON data."}, status=400)

        usn = data.get('usn')
        department = data.get('department')
        section = data.get('section')
        image_data = data.get('imageData')

        if not usn or not department or not section or not image_data:
            return JsonResponse({"message": "Missing required fields."}, status=400)

        try:
            # Decode the image data
            image_data = image_data.split(',')[1]
            image_data = base64.b64decode(image_data)
            nparr = np.frombuffer(image_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        except Exception as e:
            return JsonResponse({"message": f"Error decoding image data: {str(e)}"}, status=400)

        # Perform face recognition
        face_encodings = face_recognition.face_encodings(frame)
        if not face_encodings:
            return JsonResponse({"message": "No face detected. Please try again."}, status=400)

        encoding = face_encodings[0].tolist()

        # Load existing data
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as file:
                students = json.load(file)
        else:
            students = []

        # Add new student data
        students.append({
            'usn': usn,
            'department': department,
            'section': section,
            'encoding': encoding
        })

        # Save data to JSON file
        with open(DATA_FILE, 'w') as file:
            json.dump(students, file)

        return JsonResponse({"message": "Student registered successfully!"})
    else:
        return render(request, 'signup.html')

def login_student(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON data."}, status=400)

        usn = data.get('usn')
        image_data = data.get('imageData')

        if not usn or not image_data:
            return JsonResponse({"message": "Missing required fields."}, status=400)

        try:
            # Decode the image data
            image_data = image_data.split(',')[1]
            image_data = base64.b64decode(image_data)
            nparr = np.frombuffer(image_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        except Exception as e:
            return JsonResponse({"message": f"Error decoding image data: {str(e)}"}, status=400)

        # Perform face recognition
        face_encodings = face_recognition.face_encodings(frame)
        if not face_encodings:
            return JsonResponse({"message": "No face detected. Please try again."}, status=400)

        encoding = face_encodings[0]

        # Load existing data
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as file:
                students = json.load(file)
        else:
            return JsonResponse({"message": "No registered students found. Please sign up first."}, status=400)

        # Verify the student data
        for student in students:
            if student['usn'] == usn:
                known_encoding = np.array(student['encoding'])
                matches = face_recognition.compare_faces([known_encoding], encoding)
                if matches[0]:
                    return JsonResponse({
                        "message": "Login successful!",
                        "usn": student['usn'],
                        "department": student['department']
                    })
                else:
                    return JsonResponse({"message": "Face does not match. Access denied."}, status=400)

        return JsonResponse({"message": "Student not found. Please sign up first."}, status=400)
    else:
        return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def get_student_data(request):
    if not request.session.get('data_access_verified'):
        return redirect('verify_data_access')
        
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            students = json.load(file)
            return JsonResponse(students, safe=False)
    return JsonResponse({"message": "No students found."}, status=404)

def verify_data_access(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        valid_username = username == settings.DATA_ACCESS_CREDENTIALS['username']
        try:
            valid_password = check_password(
                password,
                settings.DATA_ACCESS_CREDENTIALS['password']
            )
        except ValueError:
            return render(request, 'verify_access.html', {'error': 'Invalid credentials'})
        
        if valid_username and valid_password:
            request.session['data_access_verified'] = True
            request.session.save()
            return redirect('data')
        
        return render(request, 'verify_access.html', {'error': 'Invalid username or password'})
    
    return render(request, 'verify_access.html')

def data_page(request):
    if not request.session.get('data_access_verified'):
        return redirect('verify_data_access')
    return render(request, 'data.html')