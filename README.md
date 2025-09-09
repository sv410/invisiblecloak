# Harry Potter Invisibility Cloak

A magical computer vision project that creates an invisibility cloak effect using Python, OpenCV, and a red cloth!

## How It Works

This project uses computer vision techniques to create the illusion of an invisibility cloak:

1. **Background Capture**: First, we capture a static background frame
2. **Color Detection**: We detect red-colored cloth in real-time using HSV color space
3. **Segmentation**: We create a mask to isolate the red cloth pixels
4. **Magic**: We replace the red cloth pixels with the background pixels to create the invisibility effect!

## Requirements

- Python 3.7+
- A webcam
- A red colored cloth (your "invisibility cloak")
- Good lighting conditions

## Installation

1. Install the required Python packages:
\`\`\`bash
pip install -r scripts/requirements.txt
\`\`\`

Or install manually:
\`\`\`bash
pip install opencv-python numpy
\`\`\`

## Usage

### Step 1: Capture Background
First, run the background capture script:
\`\`\`bash
python scripts/background.py
\`\`\`

**Important**: Make sure you and the red cloth are NOT in the frame when capturing the background!

### Step 2: Start the Magic
Run the main invisibility cloak script:
\`\`\`bash
python scripts/invisible_cloak.py
\`\`\`

### Controls
- **q**: Quit the application
- **s**: Save a screenshot of the magic moment
- **h**: Show help and controls

## Tips for Best Results

1. **Lighting**: Use consistent, bright lighting
2. **Background**: Choose a static background without red objects
3. **Cloth**: Use a solid red cloth (avoid patterns or mixed colors)
4. **Camera**: Keep the camera steady and at the same position used for background capture
5. **Movement**: Move slowly for smoother effects

## Troubleshooting

### Red Detection Issues
If the red cloth isn't being detected properly:

1. Run the color adjustment tool:
\`\`\`bash
python scripts/invisible_cloak.py
# Choose option 2 for color range adjustment
\`\`\`

2. Adjust the HSV sliders until your red cloth is properly detected
3. Note down the optimal values and update them in the main script

### Common Issues
- **"Background image not found"**: Run `background.py` first
- **Poor detection**: Try different lighting or adjust color ranges
- **Flickering effect**: Ensure stable lighting and camera position

## How the Magic Works

The invisibility cloak effect is achieved through:

1. **HSV Color Space**: We convert images to HSV (Hue, Saturation, Value) for better color detection
2. **Color Masking**: We create masks to identify red pixels in the frame
3. **Morphological Operations**: We clean up the mask using opening, closing, and dilation
4. **Background Replacement**: We replace masked pixels with corresponding background pixels
5. **Gaussian Blur**: We smooth the mask edges for a more natural effect

## Project Structure

\`\`\`
scripts/
├── background.py          # Background capture script
├── invisible_cloak.py     # Main invisibility cloak effect
└── requirements.txt       # Python dependencies
\`\`\`

## Credits

Inspired by the magical world of Harry Potter and computer vision techniques for augmented reality effects.

Enjoy your magical invisibility cloak! 🪄✨
