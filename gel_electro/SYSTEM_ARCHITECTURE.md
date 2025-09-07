# 🏗️ System Architecture Diagram

## 📊 **High-Level Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                    GEL ELECTROPHORESIS ANALYSIS PLATFORM        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FRONTEND      │    │    BACKEND      │    │   DATABASE      │
│                 │    │                 │    │                 │
│ • Django        │◄──►│ • Django        │◄──►│ • SQLite        │
│   Templates     │    │   Views         │    │   (Dev)         │
│ • Tailwind CSS  │    │ • Models        │    │ • PostgreSQL    │
│ • JavaScript    │    │ • URLs          │    │   (Production)  │
│ • Responsive    │    │ • Forms         │    │                 │
│   Design        │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   USER          │    │   PROCESSING    │    │   STORAGE       │
│   INTERFACE     │    │   ENGINE        │    │                 │
│                 │    │                 │    │ • Analysis      │
│ • File Upload   │    │ • Image         │    │   Results       │
│ • Results       │    │   Processing    │    │ • User Data     │
│   Display       │    │ • AI Analysis   │    │ • Processed     │
│ • Visualizations│    │ • Band          │    │   Images        │
│                 │    │   Detection     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔄 **Data Flow Architecture**

```
USER UPLOAD
    │
    ▼
┌─────────────────┐
│   WEB INTERFACE │
│   (Templates)   │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   DJANGO VIEWS  │
│   (Business     │
│    Logic)       │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   IMAGE         │
│   PROCESSING    │
│   (OpenCV/PIL)  │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   AI ANALYSIS   │
│   (Vision       │
│   Transformer)  │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   VISUALIZATION │
│   (Matplotlib/  │
│   Seaborn)      │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   DATABASE      │
│   STORAGE       │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   RESULTS       │
│   DISPLAY       │
└─────────────────┘
```

## 🧠 **AI Processing Pipeline**

```
GEL IMAGE INPUT
    │
    ▼
┌─────────────────┐
│   PREPROCESSING │
│ • Median Filter │
│ • CLAHE         │
│ • Normalization │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   LANE          │
│   DETECTION     │
│ • Vertical      │
│   Projection    │
│ • Peak Finding  │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   BAND          │
│   DETECTION     │
│ • Horizontal    │
│   Projection    │
│ • Contour       │
│   Analysis      │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   AI            │
│   CLASSIFICATION│
│ • Vision        │
│   Transformer   │
│ • Disease       │
│   Prediction    │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   RESULTS       │
│ • Classification│
│ • Confidence    │
│ • Visualizations│
└─────────────────┘
```

## 🎨 **Frontend Architecture**

```
┌─────────────────┐
│   BASE.HTML     │
│   (Layout)      │
└─────────────────┘
    │
    ├─── Navigation
    ├─── Dark/Light Mode
    ├─── Static Files
    └─── Common Styling
    │
    ▼
┌─────────────────┐
│   PAGE          │
│   TEMPLATES     │
└─────────────────┘
    │
    ├─── home.html
    ├─── disease_prediction.html
    ├─── forensics_result.html
    ├─── about.html
    └─── faqs.html
    │
    ▼
┌─────────────────┐
│   TAILWIND CSS  │
│   STYLING       │
└─────────────────┘
    │
    ├─── Responsive Design
    ├─── Dark Mode
    ├─── Animations
    └─── Modern UI
```

## 🔧 **Backend Architecture**

```
┌─────────────────┐
│   DJANGO        │
│   FRAMEWORK     │
└─────────────────┘
    │
    ├─── Settings
    ├─── URLs
    ├─── Models
    ├─── Views
    └─── Forms
    │
    ▼
┌─────────────────┐
│   PROCESSING    │
│   MODULES       │
└─────────────────┘
    │
    ├─── gel_analysis.py
    ├─── robust_detection.py
    ├─── forensic_visualization.py
    └─── disease_patterns.py
    │
    ▼
┌─────────────────┐
│   EXTERNAL      │
│   LIBRARIES     │
└─────────────────┘
    │
    ├─── OpenCV (Image Processing)
    ├─── PyTorch (AI/ML)
    ├─── Matplotlib (Visualization)
    └─── NumPy/SciPy (Scientific Computing)
```

## 🗄️ **Database Schema**

```
┌─────────────────┐
│   DISEASE       │
│   PREDICTION    │
│   TABLE         │
└─────────────────┘
    │
    ├─── id (Primary Key)
    ├─── image_path
    ├─── prediction_result
    ├─── confidence_score
    ├─── bands_detected
    ├─── lanes_detected
    ├─── created_at
    └─── updated_at
    │
    ▼
┌─────────────────┐
│   FORENSIC      │
│   ANALYSIS      │
│   TABLE         │
└─────────────────┘
    │
    ├─── id (Primary Key)
    ├─── crime_scene_image
    ├─── suspect_image
    ├─── match_score
    ├─── similarity_analysis
    ├─── visualization_paths
    ├─── created_at
    └─── updated_at
```

## 🚀 **Deployment Architecture**

```
┌─────────────────┐
│   RENDER.COM    │
│   (Cloud Host)  │
└─────────────────┘
    │
    ├─── Web Service
    │    ├─── Django App
    │    ├─── Gunicorn Server
    │    └─── Static Files
    │
    └─── Database Service
         ├─── PostgreSQL
         ├─── Data Persistence
         └─── Backup
    │
    ▼
┌─────────────────┐
│   GITHUB        │
│   (Code Repo)   │
└─────────────────┘
    │
    ├─── Auto-Deploy
    ├─── Version Control
    └─── CI/CD Pipeline
```

## 📊 **Key Components Summary**

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Django Templates + Tailwind CSS | User Interface |
| **Backend** | Django (Python) | Web Framework |
| **Image Processing** | OpenCV, PIL, NumPy | Gel Analysis |
| **AI/ML** | PyTorch, Vision Transformer | Disease Prediction |
| **Visualization** | Matplotlib, Seaborn | Data Plots |
| **Database** | SQLite/PostgreSQL | Data Storage |
| **Deployment** | Render.com | Cloud Hosting |
| **Version Control** | GitHub | Code Management |

## 🎯 **System Strengths**

### **1. Modular Architecture:**
- Clear separation of concerns
- Easy to maintain and extend
- Reusable components

### **2. Scalable Design:**
- Can handle multiple users
- Database optimization
- Cloud-ready deployment

### **3. Professional Quality:**
- Production-ready code
- Error handling
- Security measures

### **4. User-Friendly:**
- Intuitive interface
- Real-time feedback
- Comprehensive results

---

**This architecture demonstrates a well-designed, professional-grade scientific computing platform!** 🚀
