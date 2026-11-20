# ============================================================
# Module 10 : Actuator Map Generation
# ============================================================

import numpy as np
import cv2
import os


def generate_actuator_map(
        wavefront,
        num_actuators=10,
        output_folder="outputs"):
    """
    Generate actuator command map.

    Parameters
    ----------
    wavefront : ndarray

    num_actuators : int

    output_folder : str

    Returns
    -------
    actuator_map

    output_path
    """

    print("\n========== MODULE 10 ==========\n")

    if wavefront is None:

        raise ValueError(
            "Wavefront not found."
        )

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    rows, cols = wavefront.shape

    print("Wavefront Size :", rows, "x", cols)

    actuator_map = np.zeros(

        (num_actuators,
         num_actuators),

        dtype=np.float32

    )

    row_step = rows // num_actuators

    col_step = cols // num_actuators

    print("Actuator Grid :", actuator_map.shape)

    print("--------------------------------")

    # Continue in Part 2...
    
        # --------------------------------------------------------
    # Fill Actuator Grid
    # --------------------------------------------------------

    for i in range(num_actuators):

        for j in range(num_actuators):

            r_start = i * row_step
            r_end = min((i + 1) * row_step, rows)

            c_start = j * col_step
            c_end = min((j + 1) * col_step, cols)

            block = wavefront[
                r_start:r_end,
                c_start:c_end
            ]

            if block.size > 0:

                actuator_map[i, j] = np.mean(block)

    print("Actuator Map Generated")

    # --------------------------------------------------------
    # Normalize
    # --------------------------------------------------------

    actuator_normalized = cv2.normalize(
        actuator_map,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    actuator_normalized = actuator_normalized.astype(
        np.uint8
    )

    print("Normalization Completed")

    # --------------------------------------------------------
    # Apply Color Map
    # --------------------------------------------------------

    actuator_image = cv2.applyColorMap(
        actuator_normalized,
        cv2.COLORMAP_JET
    )

    # --------------------------------------------------------
    # Save Image
    # --------------------------------------------------------

    output_path = os.path.join(
        output_folder,
        "actuator_map.png"
    )

    cv2.imwrite(
        output_path,
        actuator_image
    )

    print("--------------------------------")
    print("Actuator Map Saved")
    print(output_path)
    print("--------------------------------")

    # --------------------------------------------------------
    # Return
    # --------------------------------------------------------

    return actuator_map, output_path


# ============================================================
# Test Module
# ============================================================

if __name__ == "__main__":

    # Dummy Wavefront
    wavefront = np.random.rand(
        128,
        128
    ) * 255

    actuator_map, output = generate_actuator_map(
        wavefront,
        num_actuators=10
    )

    print("\n========== MODULE 10 OUTPUT ==========\n")

    print("Actuator Map Shape :", actuator_map.shape)

    print("Saved Image :", output)