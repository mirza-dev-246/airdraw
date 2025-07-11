AirDraw: Virtual Drawing with Color-Based Object Tracking
AirDraw is a computer vision project that allows users to draw on a virtual canvas in real-time by moving a colored object (such as a pen cap or marker) in front of a webcam. This project uses HSV (Hue, Saturation, Value) color segmentation to detect the object and track its movement to draw lines on the screen, similar to a digital whiteboard but without physical contact.

Key Features
Color-based object tracking: Detects and tracks a colored object using HSV thresholds to identify it in the video frame.

Six color choices: The drawing interface offers six predefined colors — Blue, Green, Red, Yellow, Purple, and Orange — to choose from.

Real-time drawing: Tracks the position of the colored object frame-by-frame and renders the drawing in real-time on both the video feed and a separate canvas.

Clear button: Includes a clickable area to clear all drawings on the canvas.

On-screen UI buttons: All color options and the clear button are displayed at the top of the screen as part of the webcam interface.

HSV tuning: Trackbars are provided in a separate OpenCV window to manually fine-tune the HSV range for accurate color detection.

Smooth strokes: Drawing strokes are managed using deque buffers, ensuring clean and smooth line rendering as the object moves.

Technologies Used
Python: Core programming language for implementation.

OpenCV: For image processing, object detection, drawing, and real-time webcam handling.

NumPy: For array and numerical operations, particularly with image masks and matrix data.

How It Works
The webcam feed is captured using OpenCV.

The frame is converted from BGR to HSV color space.

A binary mask is generated using HSV threshold values to isolate the colored object.

Morphological operations like erosion and dilation clean up the mask.

Contours are detected to find the largest object matching the selected color.

The center of the contour is calculated and treated as the "pen tip" position.

If the pen tip is within the button bar region, the system interprets it as a button click (e.g., color switch or clear canvas).

Otherwise, it records the pen position and draws a line segment between consecutive positions using the currently selected color.

Use Cases
Interactive drawing and educational tools

Gesture-based creative applications

A foundation for developing touchless interfaces or virtual whiteboards

Basic introduction to real-time computer vision using OpenCV

Getting Started
To run this project:

Make sure Python, OpenCV, and NumPy are installed.

Clone the repository and run the Python script.

Use a colored object and adjust HSV sliders to ensure proper tracking.

Use the top button bar to switch colors or clear the canvas.

This project serves as a beginner-friendly yet practical application of image processing, and can be extended further by integrating features like shape recognition, gesture commands, brush thickness control, or saving the canvas.
