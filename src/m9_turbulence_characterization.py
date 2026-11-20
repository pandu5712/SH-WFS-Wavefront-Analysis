# ============================================================
# Module 9 : Turbulence Characterization
# ============================================================

import numpy as np


def characterize_turbulence(
        wavefront):
    """
    Estimate turbulence parameters
    from reconstructed wavefront.

    Parameters
    ----------
    wavefront : ndarray

    Returns
    -------
    results : dict
    """

    print("\n========== MODULE 9 ==========\n")

    if wavefront is None:

        raise ValueError(
            "Wavefront not found."
        )

    wavefront = wavefront.astype(
        np.float32
    )

    mean_value = np.mean(wavefront)

    std_value = np.std(wavefront)

    variance = np.var(wavefront)

    print("Wavefront Mean :", round(mean_value,4))
    print("Wavefront Std  :", round(std_value,4))
    print("Wavefront Var  :", round(variance,4))

    print("--------------------------------")

    # Continue in Part 2...
    
        # --------------------------------------------------------
    # Estimate Turbulence Parameters
    # --------------------------------------------------------

    # Simplified estimation
    r0 = round(
        0.20 / (1 + std_value),
        4
    )

    tau0 = round(
        r0 * 5.0,
        4
    )

    turbulence_strength = round(
        variance / 1000,
        4
    )

    print(f"Fried Parameter (r0)      : {r0} m")
    print(f"Coherence Time (tau0)     : {tau0} ms")
    print(f"Turbulence Strength       : {turbulence_strength}")

    print("--------------------------------")
    print("Turbulence Characterization Completed")
    print("--------------------------------")

    results = {

        "r0": r0,

        "tau0": tau0,

        "turbulence_strength": turbulence_strength

    }

    return results


# ============================================================
# Test Module
# ============================================================

if __name__ == "__main__":

    # Dummy wavefront for testing
    wavefront = np.random.rand(
        128,
        128
    ) * 255

    results = characterize_turbulence(
        wavefront
    )

    print("\n========== MODULE 9 OUTPUT ==========\n")

    print("Fried Parameter (r0) :", results["r0"], "m")
    print("Coherence Time (tau0) :", results["tau0"], "ms")
    print("Turbulence Strength :", results["turbulence_strength"])