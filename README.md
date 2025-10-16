# Hand-Gesture-Virtual-Mouse
A computer-vision-based virtual mouse built using Python, OpenCV, and Mediapipe that allows users to control the cursor and perform click operations through real-time hand gestures. Integrated with PyAutoGUI for system-level automation and optimized for smooth, low-latency performance.
The Hand Gesture Virtual Mouse is a computer-vision-based project that allows users to control the mouse pointer and perform click actions using real-time hand gestures — completely touch-free.
Built using OpenCV for video processing, Mediapipe for hand landmark detection, and PyAutoGUI for system-level mouse control, this project demonstrates how computer vision and automation can together enhance Human–Computer Interaction (HCI).

⚙️ Features

👆 Cursor Movement: Control mouse pointer using index finger movements in front of the webcam.

✌️ Click Gestures: Perform left/right clicks using predefined finger gestures.

⚡ Optimized Performance: Achieved smooth real-time operation (30+ FPS) through frame-rate tuning and efficient landmark mapping.

🧠 Modular Code Design: Separate modules for gesture detection, event mapping, and cursor control — following clean software engineering practices.

💻 Cross-Platform: Works seamlessly on Windows, macOS, and Linux.

🚀 How It Works

The webcam captures the video feed.

Mediapipe detects hand landmarks in real time.

The position of the index and middle fingers determines cursor position and click actions.

PyAutoGUI maps gestures to actual mouse movements and clicks.

🧩 Future Enhancements

Add gesture-based volume and brightness control.

Integrate AI model for more advanced gesture classification.

Include GUI overlay for user feedback and calibration.
