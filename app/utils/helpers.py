import os
import shutil
import re
from fastapi import UploadFile
from datetime import datetime

def generate_slug(text: str) -> str:
    """Converts a string like 'My Course Title!' into 'my-course-title'"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def send_email_background(email_to: str, subject: str, body: str):
    """
    Mock email sender. 
    In production, integrate smtplib or a third-party API like SendGrid here.
    """
    print(f"\n--- EMAIL DISPATCHED ---")
    print(f"To: {email_to}")
    print(f"Subject: {subject}")
    print(f"Body:\n{body}")
    print(f"------------------------\n")

def save_upload_file(upload_file: UploadFile, folder: str) -> str:
    """
    Saves an uploaded file (like a course thumbnail) to the local disk.
    Organizes files by year and month.
    """
    if not upload_file:
        return None
    
    current_month = datetime.now().strftime("%Y/%m")
    upload_dir = f"media/{folder}/{current_month}"
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = f"{upload_dir}/{upload_file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
        
    return file_path