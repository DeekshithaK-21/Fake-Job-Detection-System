# app/routes.py

from flask import Blueprint, render_template, request
from app.predict import predict_pipeline
import os
import uuid

routes = Blueprint("routes", __name__)

@routes.route("/", methods=["GET", "POST"])
def home():
    result = None
    raw_text = ""

    if request.method == "POST":

        input_type = request.form.get("input_type")
        print("INPUT TYPE:", input_type)

        # -------- TEXT --------
        if input_type == "text":
            text = request.form.get("text", "").strip()

            if not text:
                print("⚠ Empty text input")
            else:
                print("TEXT INPUT:", text[:100])

            result = predict_pipeline(text, "text")

        # -------- IMAGE / PDF --------
        elif input_type in ["image", "pdf"]:

            file = None 
            if input_type == "image":
                file = request.files.get("image_file")
            elif input_type == "pdf":
                file = request.files.get("pdf_file")
            print("FILES RECEIVED:", request.files)

            if not file or file.filename == "":
                print("❌ No file uploaded")
                result = None

            else:
                print("FILE RECEIVED:", file.filename)

                # ✅ CREATE UPLOAD FOLDER
                upload_dir = "uploads"
                os.makedirs(upload_dir, exist_ok=True)

                # ✅ SAFE UNIQUE FILE NAME
                ext = file.filename.split(".")[-1]
                unique_name = f"{uuid.uuid4()}.{ext}"

                file_path = os.path.join(upload_dir, unique_name)

                # ✅ SAVE FILE
                file.save(file_path)

                print("SAVED PATH:", file_path)

                try:
                    size = os.path.getsize(file_path)
                    print("FILE SIZE:", size)
                except:
                    print("⚠ Could not get file size")

                # -------- IMAGE --------
                if input_type == "image":
                    result = predict_pipeline(file_path, "image")

                # -------- PDF --------
                elif input_type == "pdf":
                    result = predict_pipeline(file_path, "pdf")

        else:
            print("❌ INVALID INPUT TYPE")

    # -------- SAFE RAW TEXT --------
    if result:
        raw_text = result.get("raw_text", "")
        print("EXTRACTED TEXT PREVIEW:", raw_text[:200])

    return render_template("index.html", result=result, raw_text=raw_text)