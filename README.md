# 📚 The OAPEN Monograph Schema

A structured schema and transformation system for converting flat-file metadata into **ONIX 3.0-compliant XML**, tailored for **OAPEN (Open Access Publishing in European Networks)** monographs.

---

## 🚀 Overview

The **OAPEN Monograph Schema** project provides a standardized approach to representing and transforming metadata for open-access academic books.

This project focuses on:
- Defining a structured metadata schema (YAML-based)
- Mapping metadata to ONIX 3.0 format
- Enabling seamless integration with publishing and distribution systems

---

## 🎯 Objectives

- 📖 Standardize monograph metadata representation  
- 🔄 Convert flat-file data into ONIX 3.0 XML  
- 🌐 Support open-access publishing workflows  
- ⚡ Provide a lightweight, stateless processing system  
- 🧩 Ensure compatibility with OAPEN infrastructure  

---

## ✨ Features

- 📄 YAML-based metadata input  
- 🔁 Automated ONIX 3.0 XML generation  
- ⚡ Fast, in-memory processing (no storage)  
- 🧱 Modular and extensible schema design  
- 🔍 Validates structured metadata fields  
- 🌍 Designed for open-access monograph ecosystems  

---

## 🏗️ Tech Stack

**Backend**
- Python 3.10+  
- FastAPI (stateless microservice)

**Frontend**
- HTML5  
- CSS3  
- Vanilla JavaScript  

**Libraries**
- pyyaml – YAML parsing  
- lxml – XML generation  

---

## 📁 Project Structure

```
The-OAPEN-Monograph-Schema/
│
├── app/
│   ├── main.py
│   ├── transformer.py
│   └── schema.yaml
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
│
├── examples/
│   ├── sample.yaml
│   └── output.xml
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository
```
git clone https://github.com/sufyanism/The-OAPEN-Monograph-Schema.git
cd The-OAPEN-Monograph-Schema
```

### 2. Create virtual environment
```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate    # Windows
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

---

## ▶️ Usage

### Run the application
```
uvicorn app.main:app --reload
```

### Open in browser
```
http://127.0.0.1:8000
```

### Workflow

1. Upload a `.yaml` metadata file  
2. System validates input structure  
3. Converts data into ONIX 3.0 XML  
4. Downloads generated XML instantly  

---

## 🧾 Example YAML Input

```yaml
title: Example Book Title
author: John Doe
publisher: Open Access Press
isbn: 9781234567890
language: eng
price: 0.00
currency: USD
```

---

## 📄 Example Output (ONIX 3.0)

```xml
<Product>
  <RecordReference>REF001</RecordReference>
  <NotificationType>03</NotificationType>
  <DescriptiveDetail>
    <TitleDetail>
      <TitleText>Example Book Title</TitleText>
    </TitleDetail>
  </DescriptiveDetail>
</Product>
```

---

## 🔒 Architecture Principles

- ❌ No database  
- ❌ No file storage  
- ✅ Fully stateless backend  
- ✅ In-memory processing only  
- ✅ Secure and privacy-friendly  

---

## 🛠 Future Improvements

- ONIX 3.0 full schema validation (XSD)  
- Multi-author and contributor support  
- Subject classification integration  
- DOI and funding metadata support  
- API versioning and deployment support  

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository  
2. Create a feature branch  
3. Commit your changes  
4. Submit a Pull Request  

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Sufyan**  
Building tools for open-access publishing and metadata transformation  
