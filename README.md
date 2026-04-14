# 📚 The OAPEN Monograph Schema

A structured schema and transformation system for converting flat-file metadata into **ONIX 3.0-compliant XML**, **OAPEN (Open Access Publishing in European Networks)** monographs.


## 🚀 Overvie
The **OAPEN Monograph Schema** project provides a standardized approach to representing and transforming metadata for open-access academic books.
This project focuses on:
- Defining a structured metadata schema (YAML-based)
- Mapping metadata to ONIX 3.0 format
- Enabling seamless integration with publishing and distribution systems


## 🎯 Objectives
- 📖 Standardize monograph metadata representation  
- 🔄 Convert flat-file data into ONIX 3.0 XML  
- ⚡ Provide a lightweight, stateless processing system  
- 🧩 Ensure compatibility with OAPEN infrastructure  


## ✨ Features
- 📄 YAML-based metadata input  
- 🔁 Automated ONIX 3.0 XML generation  
- ⚡ Fast, in-memory processing (no storage)  
- 🧱 Modular and extensible schema design  
- 🔍 Validates structured metadata fields  
- 🌍 Designed for open-access monograph ecosystems  


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
      <TitleText>Example

 Book Title</TitleText>
    </TitleDetail>
  </DescriptiveDetail>
</Product>
```

## ▶️ Demo
OAPEN-Schema.mp4


## About Me 
✨ I’m **Sufyan bin Uzayr**, an open-source developer passionate about building and sharing meaningful projects.
You can learn more about me and my work at [sufyanism.com](https://sufyanism.com/) or connect with me on [Linkedin](https://www.linkedin.com/in/sufyanism)

## Your all-in-one learning hub! 
🚀 Explore courses and resources in coding, tech, and development at **zeba.academy** and **code.zeba.academy**. Empower yourself with practical skills through curated tutorials, real-world projects, and hands-on experience. Level up your tech game today! 💻✨

**Zeba Academy**  is a learning platform dedicated to **coding**, **technology**, and **development**.  
➡ Visit our main site: [zeba.academy](https://zeba.academy)   </br>
➡ Explore hands-on courses and resources at: [code.zeba.academy](https://code.zeba.academy)   </br>
➡ Check out our YouTube for more tutorials: [zeba.academy](https://www.youtube.com/@zeba.academy)  </br>
➡ Follow us on Instagram: [zeba.academy](https://www.instagram.com/zeba.academy/)  </br>

**Thank you for visiting!**







