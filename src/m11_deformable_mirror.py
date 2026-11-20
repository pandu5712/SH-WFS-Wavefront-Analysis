# ============================================================
# Module 11 : Deformable Mirror Correction
# ============================================================

import numpy as np
import cv2
import os


def apply_deformable_mirror(
        wavefront,
        actuator_map,
        output_folder="outputs"):
    """
    Simulate deformable mirror correction.

    Parameters
    ----------
    wavefront : ndarray
        Reconstructed wavefront

    actuator_map : ndarray
        Actuator command map

    output_folder : str

    Returns
    -------
    corrected_wavefront : ndarray

    output_path : str
    """

    print("\n========== MODULE 11 ==========\n")

    # --------------------------------------------------------
    # Input Validation
    # --------------------------------------------------------

    if wavefront is None:

        raise ValueError(
            "Wavefront not found."
        )

    if actuator_map is None:

        raise ValueError(
            "Actuator map not found."
        )

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    rows, cols = wavefront.shape

    print(
        "Wavefront Size :",
        rows,
        "x",
        cols
    )

    print(
        "Actuator Map Size :",
        actuator_map.shape
    )

    print("--------------------------------")

    # --------------------------------------------------------
    # Resize Actuator Map
    # --------------------------------------------------------

    actuator_resized = cv2.resize(

        actuator_map,

        (cols, rows),

        interpolation=cv2.INTER_CUBIC

    )

    print("Actuator Map Resized")

    # --------------------------------------------------------
    # Convert to Float
    # --------------------------------------------------------

    wavefront = wavefront.astype(
        np.float32
    )

    actuator_resized = actuator_resized.astype(
        np.float32
    )

    print("Data Converted to Float")

    print("--------------------------------")

    # Continue in Part 2...
    
        # --------------------------------------------------------
    # Apply Deformable Mirror Correction
    # --------------------------------------------------------

    corrected_wavefront = wavefront - actuator_resized

    print("Wavefront Correction Applied")

    # --------------------------------------------------------
    # Normalize Corrected Wavefront
    # --------------------------------------------------------

    corrected_normalized = cv2.normalize(

        corrected_wavefront,

        None,

        0,

        255,

        cv2.NORM_MINMAX

    )

    corrected_normalized = corrected_normalized.astype(
        np.uint8
    )

    print("Normalization Completed")

    # --------------------------------------------------------
    # Apply Color Map
    # --------------------------------------------------------

    corrected_image = cv2.applyColorMap(

        corrected_normalized,

        cv2.COLORMAP_JET

    )

    print("Color Map Applied")

    # --------------------------------------------------------
    # Save Output Image
    # --------------------------------------------------------

    output_path = os.path.join(

        output_folder,

        "corrected_wavefront.png"

    )

    cv2.imwrite(

        output_path,

        corrected_image

    )

    print("--------------------------------")
    print("Corrected Wavefront Saved")
    print(output_path)
    print("--------------------------------")

    # --------------------------------------------------------
    # Return Results
    # --------------------------------------------------------

    return corrected_wavefront, output_path


# ============================================================
# Test Module
# ============================================================

if __name__ == "__main__":

    # Dummy Wavefront

    wavefront = np.random.rand(

        128,

        128

    ) * 255

    # Dummy Actuator Map

    actuator_map = np.random.rand(

        10,

        10

    ) * 255

    corrected_wavefront, output = apply_deformable_mirror(

        wavefront,

        actuator_map

    )

    print("\n========== MODULE 11 OUTPUT ==========\n")

    print("Corrected Wavefront Shape :")

    print(corrected_wavefront.shape)

    print("\nSaved Image :")

    print(output)
    
    