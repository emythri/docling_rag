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
    file = request.files.get("html_file")

    if not file:
        return "No file uploaded"

    # Save file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # 🔥 Docling conversion
    result = converter.convert(file_path)

    # Convert to markdown
    markdown = result.document.export_to_markdown()

    # Render nicely
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial; margin: 40px; }}
            h2 {{ color: #2c3e50; }}
            pre {{
                background: #f4f4f4;
                padding: 15px;
                border-radius: 8px;
                white-space: pre-wrap;
            }}
        </style>
    </head>
    <body>
        <h2>Docling Output</h2>
        <pre>{markdown}</pre>
    </body>
    </html>
    """

# 🔥 IMPORTANT FOR LOCAL ONLY
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
