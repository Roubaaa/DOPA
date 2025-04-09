# DOPA - Detection of Prohibited Areas

A deep learning-based system for detecting prohibited drilling areas (wellpads) in satellite imagery.

## Project Overview

This project uses a U-Net architecture to segment satellite imagery and identify wellpads. The system processes satellite images and outputs binary masks indicating the presence of wellpads, along with bounding boxes and percentage coverage.

## Project Structure

```
ml_model/
├── wellpad/
│   ├── data.py           # Data loading and preprocessing
│   ├── workflow.py       # Training workflow
│   ├── augmentation.py   # Data augmentation functions
│   └── ...
├── results/
│   ├── models/           # Saved model files
│   ├── metrics/          # Training metrics
│   └── visualizations/   # Training visualizations
└── detect.py             # Inference script
```

## Installation

1. Clone the repository:
   ```
   git clone
   cd dopa
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Training the Model

To train the model on your dataset:

```python
from ml_model.wellpad.workflow import *

# The workflow.py script will:
# 1. Load and preprocess your data
# 2. Train the U-Net model
# 3. Save the model and metrics
```

### Detecting Wellpads

To detect wellpads in a new image:

```bash
python ml_model/detect.py path/to/your/image.jpg
```

The script will output a JSON result with:
- Whether wellpads were detected
- Percentage of image covered by wellpads
- Number of wellpads found
- Bounding boxes for each wellpad

## Model Details

- **Architecture**: U-Net
- **Input Size**: 256×256 pixels
- **Output**: Binary segmentation mask
- **Training Data**: Satellite imagery with wellpad annotations

## Running the Frontend
The frontend is built with Next.js and provides a user interface for uploading images and viewing detection results.

### Prerequisites

- Node.js (v14 or later)
- npm or yarn

### Installation

1. Install frontend dependencies:
   ```
   npm install
   # or
   yarn install
   ```

2. Create a `.env.local` file in the root directory with the following content:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:5000
   ```

### Development

To run the frontend in development mode:

```
npm run dev
# or
yarn dev
```

This will start the development server at http://localhost:3000.

### Production Build

To create a production build:

```
npm run build
# or
yarn build
```

To start the production server:

```
npm start
# or
yarn start
```

### Frontend Features

- Upload satellite imagery for wellpad detection
- View detection results with bounding boxes
- See percentage of image covered by wellpads
- View historical detection results
- Responsive design for desktop and mobile

### Screenshots

#### Home Page
![DOPA Home Page](website_one.png)

#### Detection Results Page
![DOPA Detection Results](website_two.png)