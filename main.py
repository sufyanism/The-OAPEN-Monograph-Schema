# =====================================================
# Flat-File to ONIX 3.0 Generator (OAPEN Monograph)
# Tech Stack: FastAPI + Python 3.10 + Vanilla JS
# Stateless | No DB | No File Storage
# =====================================================

# =============================
# BACKEND: main.py
# =============================
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
        body { font-family: Arial; text-align: center; margin-top: 50px; }
        input, button { padding: 10px; margin: 10px; }
        button { cursor: pointer; }
    </style>
</head>
<body>
    <h2>Flat-File to ONIX 3.0 Generator</h2>
    <input type="file" id="fileInput" accept=".yaml" />
    <br>
    <button onclick="upload()">Convert to ONIX</button>

    <script>
        async function upload() {
            const file = document.getElementById('fileInput').files[0];
            if (!file) return alert('Select a YAML file');

            const formData = new FormData();
            formData.append('file', file);

            const res = await fetch('/convert', {
                method: 'POST',
                body: formData
            });

            if (!res.ok) {
                const err = await res.json();
                return alert(err.detail);
            }

            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);

            const a = document.createElement('a');
            a.href = url;
            a.download = 'onix.xml';
            a.click();
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


