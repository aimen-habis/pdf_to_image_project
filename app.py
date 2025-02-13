import os
from flask import Flask, render_template, request, jsonify, send_from_directory
import fitz  # PyMuPDF

app = Flask(__name__)

# إعداد مجلدات لحفظ الملفات والصور
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# تأكد من وجود المجلدات
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# الصفحة الرئيسية لرفع ملف PDF
@app.route('/')
def index():
    return render_template('index.html')

# مسار لتحميل PDF وتحويله إلى صورة
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf' not in request.files:
        return jsonify({"success": False, "message": "No file part"})
    
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"})
    
    if file and file.filename.endswith('.pdf'):
        # حفظ الملف PDF في مجلد uploads
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        # تحويل PDF إلى صورة
        image_path = os.path.join(OUTPUT_FOLDER, 'converted_image.jpg')
        
        doc = fitz.open(file_path)  # فتح ملف PDF
        page = doc.load_page(0)  # تحميل الصفحة الأولى
        pix = page.get_pixmap()  # تحويل الصفحة إلى صورة
        pix.save(image_path)  # حفظ الصورة
        
        # إرسال الصورة للمستخدم لتحميلها
        return jsonify({"success": True, "imageUrl": f"/download/{file.filename}"})
    
    return jsonify({"success": False, "message": "Invalid file format"})

# مسار لتحميل الصورة المحولة
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, 'converted_image.jpg', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
