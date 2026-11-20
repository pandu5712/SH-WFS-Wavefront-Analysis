# ============================================================
# Module 5 : Spot Shift Calculation
# ============================================================

import math


def calculate_shift(reference_centroids,
                    current_centroids):
    """
    Calculate spot shifts.

    Parameters
    ----------
    reference_centroids : list
        [(x1,y1),(x2,y2),...]

    current_centroids : list
        [(x1,y1),(x2,y2),...]

    Returns
    -------
    shifts : list

    [
        (dx,dy),
        ...
    ]
    """

    print("\n========== MODULE 5 ==========")

    if len(reference_centroids) == 0:

        raise ValueError(
            "Reference centroids not found."
        )

    if len(current_centroids) == 0:

        raise ValueError(
            "Current centroids not found."
        )

    total_spots = min(
        len(reference_centroids),
        len(current_centroids)
    )

    print("Reference Spots :", len(reference_centroids))
    print("Current Spots   :", len(current_centroids))
    print("Processing      :", total_spots)

    shifts = []

    for i in range(total_spots):

        ref_x, ref_y = reference_centroids[i]

        cur_x, cur_y = current_centroids[i]

        dx = cur_x - ref_x
        dy = cur_y - ref_y

        distance = math.sqrt(
            dx**2 + dy**2
        )

        shifts.append(

            {

                "spot": i + 1,

                "reference":

                    (ref_x, ref_y),

                "current":

                    (cur_x, cur_y),

                "dx": dx,

                "dy": dy,

                "distance": round(distance, 3)

            }

        )

    print("---------------------------------------")

    for shift in shifts:

        print(

            f"Spot {shift['spot']:03d}"

            f" | Ref {shift['reference']}"

            f" | Cur {shift['current']}"

            f" | dx={shift['dx']}"

            f" | dy={shift['dy']}"

            f" | Shift={shift['distance']} px"

        )

    print("---------------------------------------")

    print("Spot Shift Completed")

    return shifts


# ============================================================
# Test Module
# ============================================================

if __name__ == "__main__":

    reference_centroids = [

        (20,20),
        (45,20),
        (70,20),
        (95,20)

    ]

    current_centroids = [

        (22,21),
        (47,20),
        (69,19),
        (96,23)

    ]

    shifts = calculate_shift(

        reference_centroids,

        current_centroids

    )

    print("\nReturned Data\n")

    for s in shifts:

        print(s)