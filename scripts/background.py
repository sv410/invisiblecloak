import cv2
import numpy as np
import time
def capture_background():
    """
    Capture and save the background frame for the invisibility cloak effect.
    This function captures the static background that will be used to replace
    the red cloth pixels in the main invisibility cloak script.
    """
    # Initialize the camera in this code 
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return False
    print("Setting up camera...")
    time.sleep(2)  # Give camera time to adjust-code line 
    print("Capturing background in 3 seconds...")
    print("Make sure there's no red cloth in the frame!")
    # Countdown
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # Capture multiple frames and average them for a stable background
    background_frames = []
    
    for i in range(30):  # Capture 30 frames
        ret, frame = cap.read()
        if ret:
            background_frames.append(frame)
        time.sleep(0.1)  # Small delay between captures
    
    if background_frames:
        # Average all frames to get a stable background
        background = np.mean(background_frames, axis=0).astype(np.uint8)
        
        # Save the background image
        cv2.imwrite('background.jpg', background)
        print("Background captured and saved as 'background.jpg'")
        
        # Display the captured background
        cv2.imshow('Captured Background', background)
        cv2.waitKey(2000)  # Show for 2 seconds
        cv2.destroyAllWindows()
        
        success = True
    else:
        print("Error: Could not capture background frames")
        success = False
    
    # Release the camera
    cap.release()
    return success

if __name__ == "__main__":
    print("=== Invisibility Cloak - Background Capture ===")
    print("This script will capture the background for the invisibility effect.")
    print("Make sure:")
    print("1. You are not in the frame")
    print("2. There is no red cloth visible")
    print("3. The lighting is good and stable")
    print()
    
    input("Press Enter when ready to start...")
    
    if capture_background():
        print("\nBackground capture successful!")
        print("You can now run 'invisible_cloak.py' to start the invisibility effect.")
    else:
        print("\nBackground capture failed. Please try again.")
