# Gel Electrophoresis Band Detection Web Application

A complete Django web application for analyzing DNA gel electrophoresis images using computer vision. The application provides disease prediction and forensics analysis capabilities with a modern, responsive interface built with Tailwind CSS.

## Features

- **Disease Prediction**: Upload a single DNA gel image to detect disease markers with confidence scoring
- **Forensics Analysis**: Compare two DNA samples (crime scene vs suspect) with advanced match scoring
- **Advanced Image Processing**: Uses OpenCV with lane detection, band analysis, and feature extraction
- **Multi-level Analysis**: Band-level, lane-level, and image-level feature extraction
- **Quality Assessment**: Automatic image quality evaluation and analysis confidence scoring
- **Modern UI**: Responsive design with Tailwind CSS (no JavaScript required)
- **Real-time Results**: Instant analysis with visual overlays showing detected lanes and bands

## Project Structure

```
C:\Users\hp\Desktop\DNA\gel_electro\
├── gel_electro/              # Django project
│   ├── settings.py           # Django settings with static/media config
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py
├── gel_detection/            # Django app
│   ├── views.py              # Image processing and view logic
│   ├── forms.py              # Django forms for file uploads
│   ├── models.py             # Database models
│   ├── urls.py               # App URL routing
│   ├── gel_analysis.py       # Advanced gel analysis functions
│   └── templates/
│       ├── home.html         # Homepage with upload forms
│       ├── disease_result.html
│       └── forensics_result.html
├── static/
│   └── css/
│       └── tailwind.css      # Built Tailwind CSS (no JS)
├── media/
│   ├── uploads/              # Original uploaded images
│   └── processed/            # Processed images with band overlays
├── src/
│   └── input.css             # Tailwind directives
├── requirements.txt          # Python dependencies
├── package.json              # Node.js dependencies for Tailwind
├── tailwind.config.js        # Tailwind configuration
├── manage.py
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.10 or higher
- Node.js and npm (for Tailwind CSS build)
- Windows operating system

### Step 1: Create and Activate Virtual Environment

```bash
# Navigate to project directory
cd C:\Users\hp\Desktop\DNA\gel_electro

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate
```

### Step 2: Install Python Dependencies

```bash
# Install required Python packages
pip install -r requirements.txt
```

### Step 3: Install and Build Tailwind CSS

```bash
# Initialize npm (if not already done)
npm init -y

# Install Tailwind CSS and dependencies
npm install -D tailwindcss postcss autoprefixer

# Build Tailwind CSS to static/css/tailwind.css
npx tailwindcss -i ./src/input.css -o ./static/css/tailwind.css --minify
```

### Step 4: Run Database Migrations

```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Start Development Server

```bash
# Activate virtual environment (if not already active)
venv\Scripts\activate

# Start Django development server
python manage.py runserver
```

### Step 6: Access the Application

Open your web browser and navigate to:
```
http://127.0.0.1:8000/
```

## Usage

### Disease Prediction

1. Navigate to the "Disease Prediction" section on the homepage
2. Upload a DNA gel electrophoresis image using the file input
3. Click "Analyze for Disease"
4. View results showing:
   - Disease prediction (Detected/Not Detected)
   - Number of bands detected
   - Original and processed images with highlighted bands

### Forensics Analysis

1. Navigate to the "Forensics Analysis" section on the homepage
2. Upload two images:
   - Crime scene DNA gel image
   - Suspect DNA gel image
3. Click "Compare DNA Samples"
4. View results showing:
   - Match score percentage (0-100%)
   - Band count for each sample
   - Side-by-side comparison of original and processed images

## Image Processing Algorithm

The application uses an advanced OpenCV-based processing pipeline:

### Lane Detection
1. **Vertical Projection**: Analyze column-wise pixel intensity to identify lane centers
2. **Peak Detection**: Use scipy.signal.find_peaks to locate lane positions
3. **Lane Validation**: Filter peaks based on distance and prominence criteria

### Band Detection
1. **Horizontal Projection**: For each lane, analyze row-wise pixel intensity
2. **Peak Finding**: Detect bands as peaks in horizontal projection profiles
3. **Band Filtering**: Apply prominence and distance thresholds for accurate detection
4. **Quality Assessment**: Calculate band sharpness and intensity metrics

### Feature Extraction
1. **Band-level Features**: Position, intensity, sharpness for each detected band
2. **Lane-level Features**: Band count, average sharpness, lane position
3. **Image-level Features**: Global intensity, edge detection, overall quality metrics

### Visualization
1. **Lane Markers**: Green vertical lines showing detected lane centers
2. **Band Markers**: Red horizontal lines highlighting detected bands
3. **Quality Overlay**: Color-coded indicators for analysis confidence

## Match Score Calculation

The forensics analysis uses a heuristic algorithm combining:

- **Band Count Similarity**: `1 - |c1 - c2| / max(c1, c2)`
- **Position Similarity**: Based on relative vertical positions of bands
- **Combined Score**: Weighted average (60% band count, 40% position) × 100

## Technical Details

### Dependencies

**Python Packages:**
- Django 4.2+ (Web framework)
- opencv-python-headless 4.8+ (Computer vision)
- Pillow 10.0+ (Image processing)
- numpy 1.24+ (Numerical operations)

**Node.js Packages:**
- tailwindcss 3.3+ (CSS framework)
- postcss 8.4+ (CSS processing)
- autoprefixer 10.4+ (CSS vendor prefixes)

### File Storage

- **Original Images**: Stored in `media/uploads/` with unique filenames
- **Processed Images**: Stored in `media/processed/` with band overlays
- **Static Files**: CSS and other assets in `static/` directory

### Database

- Uses SQLite database (db.sqlite3) for storing image metadata
- Optional GelImage model tracks uploads and processing results

## Troubleshooting

### Common Issues

1. **Tailwind CSS not loading**: Ensure you've run the build command:
   ```bash
   npx tailwindcss -i ./src/input.css -o ./static/css/tailwind.css --minify
   ```

2. **Images not displaying**: Check that media files are being served in development:
   - Verify `DEBUG = True` in settings.py
   - Ensure media URL configuration is correct

3. **OpenCV import errors**: Install the correct OpenCV package:
   ```bash
   pip install opencv-python-headless
   ```

4. **File upload errors**: Check file permissions on media directories:
   ```bash
   # Ensure directories exist and are writable
   mkdir media\uploads
   mkdir media\processed
   ```

### Development Notes

- The application runs in Django's development mode with DEBUG=True
- Media files are served directly by Django (not suitable for production)
- All image processing happens synchronously (may be slow for large images)
- No JavaScript is used anywhere in the application

## License

MIT License - See package.json for details.

## Support

For issues or questions, please check the troubleshooting section above or review the Django and OpenCV documentation.
