
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response, HTMLResponse
import yaml
from lxml import etree

app = FastAPI(title="ONIX 3.0 Generator", version="1.0")

# -----------------------------
# YAML → ONIX 3.0 Transformer
# -----------------------------
def build_onix_xml(data: dict) -> bytes:
    try:
        root = etree.Element("ONIXMessage", release="3.0")

        # HEADER
        header = etree.SubElement(root, "Header")
        sender = etree.SubElement(header, "Sender")
        etree.SubElement(sender, "SenderName").text = data.get("sender", "OAPEN")

        # PRODUCT
        product = etree.SubElement(root, "Product")
        etree.SubElement(product, "RecordReference").text = data.get("record_reference", "REF001")
        etree.SubElement(product, "NotificationType").text = "03"

        # IDENTIFIER
        identifier = etree.SubElement(product, "ProductIdentifier")
        etree.SubElement(identifier, "ProductIDType").text = "15"  # ISBN-13
        etree.SubElement(identifier, "IDValue").text = data.get("isbn", "0000000000000")

        # DESCRIPTIVE DETAIL
        desc = etree.SubElement(product, "DescriptiveDetail")
        etree.SubElement(desc, "ProductComposition").text = "00"
        etree.SubElement(desc, "ProductForm").text = "EB"

        # TITLE
        title_detail = etree.SubElement(desc, "TitleDetail")
        etree.SubElement(title_detail, "TitleType").text = "01"
        title_element = etree.SubElement(title_detail, "TitleElement")
        etree.SubElement(title_element, "TitleElementLevel").text = "01"
        etree.SubElement(title_element, "TitleText").text = data.get("title", "Untitled")

        # AUTHOR
        contributor = etree.SubElement(desc, "Contributor")
        etree.SubElement(contributor, "SequenceNumber").text = "1"
        etree.SubElement(contributor, "ContributorRole").text = "A01"
        etree.SubElement(contributor, "PersonName").text = data.get("author", "Unknown")

        # LANGUAGE
        language = etree.SubElement(desc, "Language")
        etree.SubElement(language, "LanguageRole").text = "01"
        etree.SubElement(language, "LanguageCode").text = data.get("language", "eng")

        # PUBLISHING DETAIL
        pub = etree.SubElement(product, "PublishingDetail")
        publisher = etree.SubElement(pub, "Publisher")
        etree.SubElement(publisher, "PublishingRole").text = "01"
        etree.SubElement(publisher, "PublisherName").text = data.get("publisher", "Unknown")

        # SUPPLY DETAIL
        supply = etree.SubElement(product, "ProductSupply")
        supply_detail = etree.SubElement(supply, "SupplyDetail")
        etree.SubElement(supply_detail, "ProductAvailability").text = "20"

        price = etree.SubElement(supply_detail, "Price")
        etree.SubElement(price, "PriceType").text = "01"
        etree.SubElement(price, "PriceAmount").text = str(data.get("price", "0.00"))
        etree.SubElement(price, "CurrencyCode").text = data.get("currency", "USD")

        return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    except Exception as e:
        raise ValueError(f"XML Generation Failed: {str(e)}")

# -----------------------------
# API Endpoint (Stateless)
# -----------------------------
@app.post("/convert")
async def convert(file: UploadFile = File(...)):
    if not file.filename.endswith(".yaml"):
        raise HTTPException(status_code=400, detail="Only .yaml files allowed")

    try:
        content = await file.read()
        data = yaml.safe_load(content)

        if not isinstance(data, dict):
            raise HTTPException(status_code=400, detail="Invalid YAML structure")

        xml_output = build_onix_xml(data)

        return Response(
            content=xml_output,
            media_type="application/xml",
            headers={"Content-Disposition": "attachment; filename=onix.xml"}
        )

    except yaml.YAMLError:
        raise HTTPException(status_code=400, detail="Invalid YAML format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# FRONTEND (Vanilla JS)
# -----------------------------
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>ONIX 3.0 Generator</title>

    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .container {
            background: #111827;
            padding: 40px;
            border-radius: 16px;
            width: 400px;
            text-align: center;
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        }

        h2 {
            margin-bottom: 20px;
        }

        .drop-zone {
            border: 2px dashed #374151;
            padding: 30px;
            border-radius: 12px;
            cursor: pointer;
            transition: 0.3s;
        }

        .drop-zone:hover {
            border-color: #3b82f6;
            background: rgba(59,130,246,0.1);
        }

        .drop-zone.dragover {
            border-color: #22c55e;
            background: rgba(34,197,94,0.1);
        }

        button {
            margin-top: 20px;
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            background: #3b82f6;
            color: white;
            font-size: 16px;
            cursor: pointer;
            transition: 0.3s;
        }

        button:hover {
            background: #2563eb;
        }

        button:disabled {
            background: #555;
            cursor: not-allowed;
        }

        #status {
            margin-top: 20px;
            font-size: 14px;
        }

        .success { color: #22c55e; }
        .error { color: #ef4444; }
    </style>
</head>

<body>

<div class="container">
    <h2>📘 ONIX 3.0 Generator</h2>

    <div class="drop-zone" id="dropZone">
        Drag & Drop YAML File<br>or Click to Upload
        <input type="file" id="fileInput" accept=".yaml" hidden>
    </div>

    <button id="convertBtn" onclick="upload()">Convert to ONIX</button>

    <div id="status"></div>
</div>

<script>
const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const statusDiv = document.getElementById("status");
const btn = document.getElementById("convertBtn");

dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    fileInput.files = e.dataTransfer.files;
});

async function upload() {
    const file = fileInput.files[0];

    if (!file) {
        statusDiv.innerHTML = "<span class='error'>⚠️ Please select a YAML file</span>";
        return;
    }

    btn.disabled = true;
    statusDiv.innerHTML = "⏳ Processing...";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch("/convert", {
            method: "POST",
            body: formData
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail);
        }

        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;
        a.download = "onix.xml";
        a.click();

        statusDiv.innerHTML = "<span class='success'>✅ Conversion successful! Download started.</span>";

    } catch (err) {
        statusDiv.innerHTML = "<span class='error'>❌ " + err.message + "</span>";
    }

    btn.disabled = false;
}
</script>

</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE

# =============================
# RUN
# =============================
# pip install fastapi uvicorn pyyaml lxml
# uvicorn main:app --reload
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
# open http://localhost:8000/

