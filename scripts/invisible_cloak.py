import cv2
import numpy as np
import os

def create_invisibility_cloak():
    """
    Main function to create the invisibility cloak effect using a red cloth.
    This function detects red colored cloth and replaces it with the background
    to create the magical invisibility effect.
    """
    
    # Check if background image exists
    if not os.path.exists('background.jpg'):
        print("Error: Background image not found!")
        print("Please run 'background.py' first to capture the background.")
        return False
    
    # Load the background image
    background = cv2.imread('background.jpg')
    
    # Try camera indices 0, 1, 2
    cap = None
    for cam_index in [0, 1, 2]:
        temp_cap = cv2.VideoCapture(cam_index)
        if temp_cap.isOpened():
            cap = temp_cap
            print(f"Using camera index: {cam_index}")
            break
        temp_cap.release()
    if cap is None:
        print("Error: Could not open any camera (tried indices 0, 1, 2)")
        return False
    print("=== Invisibility Cloak Active ===")
    print("Instructions:")
    print("- Use a red colored cloth as your 'invisibility cloak'")
    print("- Move the cloth around to see the magic!")
    print("- Press 'q' to quit")
    print("- Press 's' to save a screenshot")
    print("- Press 'h' to show/hide this help message")
    # Define the range for red color in HSV
    # Lower and upper bounds for red color detection
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])
    screenshot_count = 0
    
    while True:
        # Capture frame from camera
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame from camera")
            break
        
        # Flip the frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Resize background to match frame size if needed
        if background.shape != frame.shape:
            background_resized = cv2.resize(background, (frame.shape[1], frame.shape[0]))
        else:
            background_resized = background.copy()
        
        # Convert frame to HSV color space for better color detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create masks for red color detection
        # Red color wraps around in HSV, so we need two ranges
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        
        # Combine both masks
        mask = mask1 + mask2
        
        # Apply morphological operations to clean up the mask
        # Remove noise and fill gaps
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Dilate the mask to make it smoother
        mask = cv2.dilate(mask, kernel, iterations=2)
        
        # Create inverse mask
        mask_inv = cv2.bitwise_not(mask)
        
        # Apply Gaussian blur to the mask for smoother edges
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        mask_inv = cv2.GaussianBlur(mask_inv, (5, 5), 0)
        
        # Normalize masks to 0-1 range for blending
        mask_norm = mask.astype(float) / 255
        mask_inv_norm = mask_inv.astype(float) / 255
        
        # Create the final output
        # Where mask is white (red cloth detected), use background
        # Where mask is black (no red cloth), use current frame
        result = np.zeros_like(frame)
        
        for i in range(3):  # For each color channel
            result[:, :, i] = (mask_norm * background_resized[:, :, i] + 
                              mask_inv_norm * frame[:, :, i])
        
        result = result.astype(np.uint8)
        
        # Display the result
        cv2.imshow('Invisibility Cloak', result)
        
        # Optional: Show the mask for debugging
        # cv2.imshow('Mask', mask)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("Exiting invisibility cloak...")
            break
        elif key == ord('s'):
            # Save screenshot
            screenshot_count += 1
            filename = f'invisibility_screenshot_{screenshot_count}.jpg'
            cv2.imwrite(filename, result)
            print(f"Screenshot saved as '{filename}'")
        elif key == ord('h'):
            # Show/hide help
            print("\nControls:")
            print("q - Quit")
            print("s - Save screenshot")
            print("h - Show this help")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    return True

def adjust_color_range():
    """
    Helper function to adjust the red color detection range.
    Use this if the default red detection doesn't work well with your cloth.
    """
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    print("=== Color Range Adjustment ===")
    print("Use this tool to find the best HSV range for your red cloth")
    print("Press 'q' to quit")
    
    # Create trackbars for HSV range adjustment
    cv2.namedWindow('HSV Adjustment')
    cv2.createTrackbar('Lower H', 'HSV Adjustment', 0, 180, lambda x: None)
    cv2.createTrackbar('Lower S', 'HSV Adjustment', 50, 255, lambda x: None)
    cv2.createTrackbar('Lower V', 'HSV Adjustment', 50, 255, lambda x: None)
    cv2.createTrackbar('Upper H', 'HSV Adjustment', 10, 180, lambda x: None)
    cv2.createTrackbar('Upper S', 'HSV Adjustment', 255, 255, lambda x: None)
    cv2.createTrackbar('Upper V', 'HSV Adjustment', 255, 255, lambda x: None)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Get trackbar values
        lower_h = cv2.getTrackbarPos('Lower H', 'HSV Adjustment')
        lower_s = cv2.getTrackbarPos('Lower S', 'HSV Adjustment')
        lower_v = cv2.getTrackbarPos('Lower V', 'HSV Adjustment')
        upper_h = cv2.getTrackbarPos('Upper H', 'HSV Adjustment')
        upper_s = cv2.getTrackbarPos('Upper S', 'HSV Adjustment')
        upper_v = cv2.getTrackbarPos('Upper V', 'HSV Adjustment')
        
        # Create mask with current values
        lower = np.array([lower_h, lower_s, lower_v])
        upper = np.array([upper_h, upper_s, upper_v])
        mask = cv2.inRange(hsv, lower, upper)
        
        # Show original and mask
        cv2.imshow('Original', frame)
        cv2.imshow('Mask', mask)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print(f"\nOptimal HSV range found:")
            print(f"Lower: [{lower_h}, {lower_s}, {lower_v}]")
            print(f"Upper: [{upper_h}, {upper_s}, {upper_v}]")
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("=== Harry Potter Invisibility Cloak ===")
    print("Choose an option:")
    print("1. Start invisibility cloak")
    print("2. Adjust color detection range")
    print("3. Exit")
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == '1':
        create_invisibility_cloak()
    elif choice == '2':
        adjust_color_range()
    elif choice == '3':
        print("Goodbye!")
    else:
        print("Invalid choice. Starting invisibility cloak...")
        create_invisibility_cloak()
