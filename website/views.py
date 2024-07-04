import os
import cv2
from PIL import Image
import numpy as np
from PIL import Image
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
from django.conf import settings
from django.template.response import TemplateResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from App.models import Patient
import zipfile
from django.core.files.storage import FileSystemStorage
import csv
from django.contrib.auth.decorators import login_required

class CustomFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']

        user = authenticate(username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request, 'login.html')
def logout(request):
    auth_logout(request)
    return redirect('login')
def add_patient(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        patient_id = request.POST.get('patient_id')
        date = request.POST.get('date')
        medical_image = request.FILES.get('medical_image')
        type = request.POST.get('type')
        result = request.POST.get('result')

        if name and patient_id and date and type and result and medical_image:
            patient = Patient(name=name, patient_id=patient_id, date=date, type=type, result=result, medical_image=medical_image)
            patient.save()
            return render(request, 'add_patient.html', {'success': True})

    return render(request, 'add_patient.html')

def view_patients(request):
    patients = Patient.objects.all()
    return render(request, 'view_patients.html', {'patients': patients})


def download_patients_with_images(request):
    patients = Patient.objects.all()

    # Create a temporary directory to store images and CSV
    temp_dir = 'temp_images'
    os.makedirs(temp_dir, exist_ok=True)

    # Create a zip file
    zip_filename = 'patients_with_images.zip'
    zip_file_path = os.path.join(temp_dir, zip_filename)
    zip_file = zipfile.ZipFile(zip_file_path, 'w')

    # Create a CSV file
    csv_file_path = os.path.join(temp_dir, 'patients.csv')
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Patient ID', 'Date', 'Type', 'Result'])

        # Write patient data to CSV and add image files to zip
        for patient in patients:
            writer.writerow([patient.name, patient.patient_id, patient.date, patient.type, patient.result])
            if patient.medical_image:
                image_path = os.path.join(temp_dir, f'{patient.id}_{patient.name}.jpg')
                with open(image_path, 'wb') as image_file:
                    for chunk in patient.medical_image.chunks():
                        image_file.write(chunk)
                zip_file.write(image_path, arcname=f'{patient.id}_{patient.name}.jpg')

    # Add the CSV file to the zip file
    zip_file.write(csv_file_path, arcname='patients.csv')

    zip_file.close()

    # Create response
    response = HttpResponse(open(zip_file_path, 'rb').read(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

    # Clean up temporary directory
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)
    os.rmdir(temp_dir)

    return response
@login_required
def home(request):
    return TemplateResponse(request, "home.html")
@login_required
def index(request):
    message = ""
    prediction = ""
    fss = CustomFileSystemStorage()
    try:
        image = request.FILES["image"]
        print("Name", image.file)
        _image = fss.save(image.name, image)
        path = str(settings.MEDIA_ROOT) + "/" + image.name
        
        image_url = fss.url(_image)
        
        imag=cv2.imread(path)
        img_from_ar = Image.fromarray(imag, 'RGB')
        resized_image = img_from_ar.resize((256, 256))

        test_image =np.expand_dims(resized_image, axis=0) 

        
        model = tf.keras.models.load_model(os.getcwd() + '/Brainstroke2.h5')

        result = model.predict(test_image) 
       
        print("Prediction: " + str(np.argmax(result)))

        if (np.argmax(result) == 0):
            prediction = "Normal"
        elif (np.argmax(result) == 1):
            prediction = "Stroke"
         
        else:
            prediction = "Unknown"
        
        return TemplateResponse(
            request,
            "index.html",
            {
                "message": message,
                "image": image,
                "image_url": image_url,
                "prediction": prediction,
            },
        )
    except MultiValueDictKeyError:

        return TemplateResponse(
            request,
            "index.html",
            {"message": "No Image Selected"},
        )
def index1(request):
    message = ""
    prediction = ""
    fss = CustomFileSystemStorage()
    try:
        image = request.FILES["image"]
        print("Name", image.file)
        _image = fss.save(image.name, image)
        path = str(settings.MEDIA_ROOT) + "/" + image.name
        
        image_url = fss.url(_image)
        
        imag=cv2.imread(path)
        img_from_ar = Image.fromarray(imag, 'RGB')
        resized_image = img_from_ar.resize((256, 256))

        test_image =np.expand_dims(resized_image, axis=0) 

        
        model = tf.keras.models.load_model(os.getcwd() + '/LungCancer3.h5')

        result = model.predict(test_image) 
       
        print("Prediction: " + str(np.argmax(result)))

        if (np.argmax(result) == 0):
            prediction = "Adenocarcinoma"
        elif (np.argmax(result) == 1):
            prediction = "Benign Tumors"
        elif (np.argmax(result) == 2):
            prediction = "Large Cell Carcinoma"
        elif (np.argmax(result) == 3):
           prediction = "Malignant Tumors"
        elif (np.argmax(result) == 4):
            prediction = "Normal"
        elif (np.argmax(result) == 5):
           prediction = "Squamous Cell Carcinoma"
        else:
            prediction = "Unknown"
        
        return TemplateResponse(
            request,
            "index1.html",
            {
                "message": message,
                "image": image,
                "image_url": image_url,
                "prediction": prediction,
            },
        )
    except MultiValueDictKeyError:

        return TemplateResponse(
            request,
            "index1.html",
            {"message": "No Image Selected"},
        )
def index2(request):
    message = ""
    prediction = ""
    fss = CustomFileSystemStorage()
    try:
        image = request.FILES["image"]
        print("Name", image.file)
        _image = fss.save(image.name, image)
        path = str(settings.MEDIA_ROOT) + "/" + image.name
        
        image_url = fss.url(_image)
        
        imag=cv2.imread(path)
        img_from_ar = Image.fromarray(imag, 'RGB')
        resized_image = img_from_ar.resize((256, 256))

        test_image =np.expand_dims(resized_image, axis=0) 

        
        model = tf.keras.models.load_model(os.getcwd() + '/Lungdisease1.h5')

        result = model.predict(test_image) 
       
        print("Prediction: " + str(np.argmax(result)))

        if (np.argmax(result) == 0):
            prediction = "Normal"
        elif (np.argmax(result) == 1):
            prediction = "PNEUMONIA BACTERIAL"
        elif (np.argmax(result) == 2):
            prediction = "PNEUMONIA VIRAL"
        elif (np.argmax(result) == 3):
            prediction = "TUBERCULOSIS"
        
        else:
            prediction = "Unknown"
        
        return TemplateResponse(
            request,
            "index2.html",
            {
                "message": message,
                "image": image,
                "image_url": image_url,
                "prediction": prediction,
            },
        )
    except MultiValueDictKeyError:

        return TemplateResponse(
            request,
            "index2.html",
            {"message": "No Image Selected"},
        )
def contact(request):
    return TemplateResponse(request, "contact.html")
def about(request):
    return TemplateResponse(request, "about.html")