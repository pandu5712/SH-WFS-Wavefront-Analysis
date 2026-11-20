# ============================================================
# Module 8 : Zernike Coefficient Calculation
# ============================================================

import numpy as np


def compute_zernike_coefficients(
        wavefront,
        num_modes=15):
    """
    Calculate simplified
    Zernike coefficients.

    Parameters
    ----------
    wavefront : ndarray

    num_modes : int

    Returns
    -------
    coefficients : dict
    """

    print("\n========== MODULE 8 ==========\n")

    if wavefront is None:

        raise ValueError(
            "Wavefront not found."
        )

    coefficients = {}

    # Normalize wavefront

    wavefront = wavefront.astype(
        np.float32
    )

    mean_value = np.mean(wavefront)

    std_value = np.std(wavefront)

    print("Wavefront Mean :", round(mean_value,4))

    print("Wavefront Std  :", round(std_value,4))

    print("--------------------------------")

    # Continue in Part 2...
    
        # --------------------------------------------------------
    # Compute Simplified Zernike Coefficients
    # --------------------------------------------------------

    for mode in range(1, num_modes + 1):

        coefficient = round(
            mean_value / mode,
            4
        )

        coefficients[f"Z{mode}"] = coefficient

    print("Calculated Zernike Coefficients\n")

    for mode, value in coefficients.items():

        print(
            f"{mode:>4} : {value:.4f}"
        )

    print("--------------------------------")
    print("Total Modes :", len(coefficients))
    print("Zernike Calculation Completed")
    print("--------------------------------")

    # --------------------------------------------------------
    # Return Results
    # --------------------------------------------------------

    return coefficients


# ============================================================
# Test Module
# ============================================================

if __name__ == "__main__":

    # Dummy Wavefront

    wavefront = np.random.rand(
        128,
        128
    ) * 255

    coefficients = compute_zernike_coefficients(
        wavefront,
        num_modes=15
    )

    print("\n========== MODULE 8 OUTPUT ==========\n")

    for mode, value in coefficients.items():

        print(
            f"{mode} : {value}"
        )