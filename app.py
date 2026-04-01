from flask import Flask, render_template, request
import os
from docling.document_converter import DocumentConverter

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Docling
converter = DocumentConverter()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    file = request.files["html_file"]

    if not file:
        return "No file uploaded"

    # Save file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # 🔥 Docling conversion (MAIN PART)
    result = converter.convert(file_path)

    # Convert to markdown
    markdown = result.document.export_to_markdown()

    # Show output in browser
    return f"<h2>Docling Output</h2><pre>{markdown}</pre>"

if __name__ == "__main__":
    app.run(debug=True)