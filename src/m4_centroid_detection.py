# ============================================================
# Module 4 : SH-WFS Spot Centroid Detection
# Detect ALL Bright Spots
# ============================================================

import cv2
import numpy as np
import os
import glob


def detect_centroids(
    image_path,
    output_folder="outputs",
    min_area=5,
    max_area=5000,
    blur_size=5,
    threshold_value=180
):
    """
    Detect all spot centroids from a SH-WFS image.

    Parameters
    ----------
    image_path : str
        Input SH-WFS image.

    output_folder : str
        Folder to save output image.

    min_area : int
        Minimum contour area.

    max_area : int
        Maximum contour area.

    blur_size : int
        Gaussian blur kernel size.

    threshold_value : int
        Binary threshold.

    Returns
    -------
    centroids : list
        [(x1,y1), (x2,y2), ...]

    output_path : str
        Saved centroid image.
    """

    # ----------------------------------------------------
    # Create Output Folder
    # ----------------------------------------------------

    os.makedirs(output_folder, exist_ok=True)

    # ----------------------------------------------------
    # Read Image
    # ----------------------------------------------------

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(
            f"Image not found : {image_path}"
        )

    output = image.copy()

    # ----------------------------------------------------
    # Convert to Gray
    # ----------------------------------------------------

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # ----------------------------------------------------
    # Gaussian Blur
    # ----------------------------------------------------

    blurred = cv2.GaussianBlur(
        gray,
        (blur_size, blur_size),
        0
    )

    # ----------------------------------------------------
    # Threshold
    # ----------------------------------------------------

    _, binary = cv2.threshold(
        blurred,
        threshold_value,
        255,
        cv2.THRESH_BINARY
    )

    # ----------------------------------------------------
    # Morphological Opening
    # Remove Noise
    # ----------------------------------------------------

    kernel = np.ones((3,3), np.uint8)

    opened = cv2.morphologyEx(
        binary,
        cv2.MORPH_OPEN,
        kernel
    )

    # ----------------------------------------------------
    # Morphological Closing
    # Fill Small Holes
    # ----------------------------------------------------

    cleaned = cv2.morphologyEx(
        opened,
        cv2.MORPH_CLOSE,
        kernel
    )

    # ----------------------------------------------------
    # Find Contours
    # ----------------------------------------------------

    contours, _ = cv2.findContours(
        cleaned,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # ----------------------------------------------------
    # Storage
    # ----------------------------------------------------

    centroids = []

    spot_number = 1

    print("\n========== MODULE 4 ==========")
    print("Total Contours Found :", len(contours))

    # Continue in Part 2...
    
        # ----------------------------------------------------
    # Process Every Contour
    # ----------------------------------------------------

    for contour in contours:

        # Calculate contour area
        area = cv2.contourArea(contour)

        # Ignore very small or very large objects
        if area < min_area or area > max_area:
            continue

        # Calculate image moments
        M = cv2.moments(contour)

        # Skip invalid contours
        if M["m00"] == 0:
            continue

        # Calculate centroid
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        # Store centroid
        centroids.append((cx, cy))

        # Draw contour
        cv2.drawContours(
            output,
            [contour],
            -1,
            (255, 0, 0),
            1
        )

        # Draw centroid
        cv2.circle(
            output,
            (cx, cy),
            4,
            (0, 0, 255),
            -1
        )

        # Draw centroid coordinates
        cv2.putText(
            output,
            f"({cx},{cy})",
            (cx + 6, cy - 6),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.35,
            (0, 255, 255),
            1
        )

        # Draw spot number
        cv2.putText(
            output,
            str(spot_number),
            (cx - 8, cy - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (0, 255, 0),
            1
        )

        print(
            f"Spot {spot_number:03d} : "
            f"X = {cx}   "
            f"Y = {cy}"
        )

        spot_number += 1

    print("\nDetected Spots :", len(centroids))

    # Continue in Part 3...
    
        # ----------------------------------------------------
    # Sort Centroids
    # Top-to-Bottom, Left-to-Right
    # ----------------------------------------------------

    centroids = sorted(
        centroids,
        key=lambda p: (p[1], p[0])
    )

    # ----------------------------------------------------
    # Save Output Image
    # ----------------------------------------------------

    output_path = os.path.join(
        output_folder,
        "centroid_detection.png"
    )

    cv2.imwrite(
        output_path,
        output
    )

    print("--------------------------------------")
    print("Centroid Detection Completed")
    print("Detected Spots :", len(centroids))
    print("Saved Output :", output_path)
    print("--------------------------------------")

    # ----------------------------------------------------
    # Return Results
    # ----------------------------------------------------

    return centroids, output_path


# ============================================================
# Test Module
# ============================================================

if __name__ == "__main__":

    image_path = "data/spot_images/spot_001.bmp.png"

    centroids, output = detect_centroids(image_path)

    print("\n========== MODULE 4 OUTPUT ==========")

    print("Total Spots :", len(centroids))

    for i, (x, y) in enumerate(centroids):

        print(
            f"Spot {i+1:03d} : "
            f"X = {x}   "
            f"Y = {y}"
        )

    print("\nSaved Image :")

    print(output)