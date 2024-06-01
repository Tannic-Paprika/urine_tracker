import cv2
import numpy as np
from matplotlib import pyplot as plt

def identify_color_blocks(image_path, hsv_ranges):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert to HSV (OpenCV loads images in BGR format)
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Extract HSV ranges
    lower_hsv = np.array(hsv_ranges['lower'])
    upper_hsv = np.array(hsv_ranges['upper'])
    
    # Create a mask using the HSV range
    mask = cv2.inRange(image_hsv, lower_hsv, upper_hsv)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter out small contours and those that are not square-like
    min_contour_area = 100  # Adjust this value as needed
    contours = [c for c in contours if cv2.contourArea(c) > min_contour_area]
    
    # Sort contours from top to bottom based on their y-coordinate
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[1])
    
    # Copy the original image for visualization
    output_image = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2RGB)
    
    # Extract the RGB values for each block
    rgb_values = []
    for i, c in enumerate(contours[:10]):  # Limit to 10 blocks
        x, y, w, h = cv2.boundingRect(c)
        
        # Make sure we have square-like blocks
        if 0.8 < w / h < 1.2:
            block = output_image[y:y+h, x:x+w]
            
            # Compute the mean RGB values of the block
            mean_rgb = block.mean(axis=0).mean(axis=0)
            rgb_values.append({
                'block': i+1,
                'R': int(mean_rgb[0]),
                'G': int(mean_rgb[1]),
                'B': int(mean_rgb[2])
            })
            
            # Draw a rectangle around each block (for visualization)
            cv2.rectangle(output_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Show the images
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.title('Mask')
    plt.imshow(mask, cmap='gray')
    plt.subplot(1, 2, 2)
    plt.title('Detected Color Blocks')
    plt.imshow(output_image)
    plt.show()
    
    return rgb_values

# Path to the image
image_path = "strip_images\image1.jpg"

# Desired HSV ranges (example values)
hsv_ranges = {
    'lower': [16, 30, 26],
    'upper': [208, 180, 246]
}

# Identify color blocks and extract RGB values
rgb_values = identify_color_blocks(image_path, hsv_ranges)
rgb_values
