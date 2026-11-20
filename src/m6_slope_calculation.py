# ============================================================
# Module 6 : Wavefront Slope Calculation
# ============================================================

import numpy as np


def calculate_slopes(
        spot_shifts,
        focal_length=20.0):
    """
    Calculate wavefront slopes
    from spot shifts.

    Parameters
    ----------
    spot_shifts : list

    [
        {
            "spot":1,
            "dx":2,
            "dy":1
        }
    ]

    focal_length : float

    Returns
    -------
    slopes

    [
        {
            "spot":1,
            "sx":0.10,
            "sy":0.05
        }
    ]
    """

    print("\n========== MODULE 6 ==========\n")

    if len(spot_shifts) == 0:

        raise ValueError(
            "No spot shifts received."
        )

    slopes = []

    print(
        "Total Spot Shifts :",
        len(spot_shifts)
    )

    print("--------------------------------")

    # Continue in Part 2...
    
        # --------------------------------------------------------
    # Calculate Slopes for Every Spot
    # --------------------------------------------------------

    for shift in spot_shifts:

        # Read spot information
        spot = shift["spot"]
        dx = shift["dx"]
        dy = shift["dy"]

        # Calculate slopes
        sx = dx / focal_length
        sy = dy / focal_length

        # Store slope information
        slopes.append({

            "spot": spot,

            "sx": sx,

            "sy": sy

        })

        # Display result
        print(
            f"Spot {spot:03d}"
            f" | dx={dx:6.2f}"
            f" | dy={dy:6.2f}"
            f" | sx={sx:8.4f}"
            f" | sy={sy:8.4f}"
        )

    print("--------------------------------")
    print("Slope Calculation Completed")
    print("Total Slopes :", len(slopes))
    print("--------------------------------")

    # Return all slopes
    return slopes


# ============================================================
# Test Module
# ============================================================

if __name__ == "__main__":

    # Example spot shifts
    spot_shifts = [

        {
            "spot": 1,
            "reference": (20, 20),
            "current": (22, 21),
            "dx": 2,
            "dy": 1,
            "distance": 2.236
        },

        {
            "spot": 2,
            "reference": (45, 20),
            "current": (47, 20),
            "dx": 2,
            "dy": 0,
            "distance": 2.000
        },

        {
            "spot": 3,
            "reference": (70, 20),
            "current": (69, 19),
            "dx": -1,
            "dy": -1,
            "distance": 1.414
        }

    ]

    slopes = calculate_slopes(
        spot_shifts,
        focal_length=20.0
    )

    print("\nReturned Slopes\n")

    for slope in slopes:
        print(slope)