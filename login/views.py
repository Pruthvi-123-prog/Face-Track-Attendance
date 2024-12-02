from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpRequest
from django.conf import settings
from django.contrib.auth.hashers import check_password
from typing import Dict, List, Any, Optional
import cv2
import face_recognition
import numpy as np
import json
import os
from pathlib import Path

# Configure data file path for local development
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / 'data' / 'students.json'

def register_student(request: HttpRequest) -> JsonResponse:
    """Handle student registration with face recognition."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            usn = data.get('usn')
            department = data.get('department')
            section = data.get('section')
            image_data = data.get('imageData')

            if not all([usn, department, section, image_data]):
                return JsonResponse({"message": "Missing required fields."}, status=400)

            # Decode and process image
            image_data = image_data.split(',')[1]
            image_data = base64.b64decode(image_data)
            nparr = np.frombuffer(image_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Face detection
            face_encodings = face_recognition.face_encodings(frame)
            if not face_encodings:
                return JsonResponse({"message": "No face detected. Please try again."}, status=400)

            encoding = face_encodings[0].tolist()

            # Ensure data directory exists
            DATA_FILE.parent.mkdir(exist_ok=True)

            # Load or create students list
            students = load_students()

            # Add new student
            students.append({
                'usn': usn,
                'department': department,
                'section': section,
                'encoding': encoding
            })

            # Save updated data
            save_students(students)
            return JsonResponse({"message": "Student registered successfully!"})

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON data."}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Registration failed: {str(e)}"}, status=500)

    return render(request, 'signup.html')

def login_student(request: HttpRequest) -> JsonResponse:
    """Handle student login with face recognition."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            usn = data.get('usn')
            image_data = data.get('imageData')

            if not all([usn, image_data]):
                return JsonResponse({"message": "Missing required fields."}, status=400)

            # Process image
            image_data = image_data.split(',')[1]
            image_data = base64.b64decode(image_data)
            nparr = np.frombuffer(image_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Face detection
            face_encodings = face_recognition.face_encodings(frame)
            if not face_encodings:
                return JsonResponse({"message": "No face detected. Please try again."}, status=400)

            encoding = face_encodings[0]
            students = load_students()

            # Verify student
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
                    return JsonResponse({"message": "Face does not match. Access denied."}, status=400)

            return JsonResponse({"message": "Student not found. Please sign up first."}, status=400)

        except Exception as e:
            return JsonResponse({"message": f"Login failed: {str(e)}"}, status=500)

    return render(request, 'login.html')

def home(request: HttpRequest):
    """Render home page."""
    return render(request, 'home.html')

def get_student_data(request: HttpRequest) -> JsonResponse:
    """Get all student data."""
    if not request.session.get('data_access_verified'):
        return redirect('verify_data_access')
    
    students = load_students()
    if students:
        return JsonResponse(students, safe=False)
    return JsonResponse({"message": "No students found."}, status=404)

def verify_data_access(request: HttpRequest):
    """Verify admin credentials for data access."""
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

def data_page(request: HttpRequest):
    """Render data page."""
    if not request.session.get('data_access_verified'):
        return redirect('verify_data_access')
    return render(request, 'data.html')

def load_students() -> List[Dict[str, Any]]:
    """Load students data from JSON file."""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

def save_students(students: List[Dict[str, Any]]) -> None:
    """Save students data to JSON file."""
    with open(DATA_FILE, 'w') as file:
        json.dump(students, file, indent=4)