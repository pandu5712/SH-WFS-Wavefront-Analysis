# ============================================================
# Module 7 : Wavefront Reconstruction
# ============================================================

import numpy as np
import cv2
import os


def reconstruct_wavefront(
        slopes,
        grid_size=128,
        output_folder="outputs"):
    """
    Reconstruct wavefront from slopes.

    Parameters
    ----------
    slopes : list

    [
        {
            "spot":1,
            "sx":0.10,
            "sy":0.05
        }
    ]

    Returns
    -------
    wavefront

    output_path
    """

    print("\n========== MODULE 7 ==========\n")

    if len(slopes) == 0:

        raise ValueError(
            "No slopes received."
        )

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    # Create slope grids

    sx_grid = np.zeros(
        (grid_size, grid_size),
        dtype=np.float32
    )

    sy_grid = np.zeros(
        (grid_size, grid_size),
        dtype=np.float32
    )

    print(
        "Total Slopes :",
        len(slopes)
    )

    print("--------------------------------")

    # Continue in Part 2...
    
        # --------------------------------------------------------
    # Fill Slope Grid
    # --------------------------------------------------------

    total_slopes = len(slopes)

    grid_side = int(np.ceil(np.sqrt(total_slopes)))

    index = 0

    for row in range(grid_side):

        for col in range(grid_side):

            if index >= total_slopes:
                break

            sx_grid[row, col] = slopes[index]["sx"]
            sy_grid[row, col] = slopes[index]["sy"]

            index += 1

    print("Slope Grid Created")

    # --------------------------------------------------------
    # Wavefront Integration
    # --------------------------------------------------------

    wavefront = np.zeros(
        (grid_size, grid_size),
        dtype=np.float32
    )

    # Integrate X direction
    wavefront += np.cumsum(
        sx_grid,
        axis=1
    )

    # Integrate Y direction
    wavefront += np.cumsum(
        sy_grid,
        axis=0
    )

    print("Wavefront Integrated")

    # --------------------------------------------------------
    # Normalize Wavefront
    # --------------------------------------------------------

    wavefront = cv2.normalize(
        wavefront,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    wavefront = wavefront.astype(
        np.uint8
    )

    print("Wavefront Normalized")

    # Continue in Part 3...
    
        # --------------------------------------------------------
    # Apply Color Map
    # --------------------------------------------------------

    phase_map = cv2.applyColorMap(
        wavefront,
        cv2.COLORMAP_JET
    )

    # --------------------------------------------------------
    # Save Output Image
    # --------------------------------------------------------

    output_path = os.path.join(
        output_folder,
        "phase_map.png"
    )

    cv2.imwrite(
        output_path,
        phase_map
    )

    print("--------------------------------")
    print("Wavefront Reconstruction Completed")
    print("Saved :", output_path)
    print("--------------------------------")

    # --------------------------------------------------------
    # Return Results
    # --------------------------------------------------------

    return wavefront, output_path


# ============================================================
# Test Module
# ============================================================

if __name__ == "__main__":

    # Example slopes
    slopes = [

        {
            "spot": 1,
            "sx": 0.10,
            "sy": 0.05
        },

        {
            "spot": 2,
            "sx": 0.12,
            "sy": 0.06
        },

        {
            "spot": 3,
            "sx": 0.08,
            "sy": 0.04
        },

        {
            "spot": 4,
            "sx": 0.11,
            "sy": 0.07
        }

    ]

    wavefront, output = reconstruct_wavefront(
        slopes
    )

    print("\n========== MODULE 7 OUTPUT ==========\n")

    print("Wavefront Shape :", wavefront.shape)

    print("Saved Image :", output)