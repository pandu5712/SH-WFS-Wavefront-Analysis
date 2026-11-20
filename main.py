# ============================================================
# SH-WFS Main Pipeline
# ============================================================

from src.m4_centroid_detection import detect_centroids
from src.m5_spot_shift import calculate_shift
from src.m6_slope_calculation import calculate_slopes
from src.m7_wavefront_reconstruction import reconstruct_wavefront
from src.m8_zernike_coefficients import compute_zernike_coefficients
from src.m9_turbulence_characterization import characterize_turbulence
from src.m10_actuator_map import generate_actuator_map
from src.m11_deformable_mirror import apply_deformable_mirror


# ============================================================
# Run Complete SH-WFS Pipeline
# ============================================================

def run_pipeline(reference_image,
                 current_image):

    print("\n==========================================")
    print("     SH-WFS PROCESSING STARTED")
    print("==========================================")

    # =======================================================
    # MODULE 4
    # =======================================================

    print("\nRunning Module 4...")

    reference_centroids, ref_output = detect_centroids(
        reference_image
    )

    current_centroids, cur_output = detect_centroids(
        current_image
    )

    print("Module 4 Completed")

    print("Reference Spots :", len(reference_centroids))
    print("Current Spots   :", len(current_centroids))

    # =======================================================
    # MODULE 5
    # =======================================================

    print("\nRunning Module 5...")

    spot_shifts = calculate_shift(

        reference_centroids,

        current_centroids

    )

    print("Module 5 Completed")

    print("Total Spot Shifts :", len(spot_shifts))

    # =======================================================
    # MODULE 6
    # =======================================================

    print("\nRunning Module 6...")

    slopes = calculate_slopes(

        spot_shifts,

        focal_length=20.0

    )

    print("Module 6 Completed")

    print("Total Slopes :", len(slopes))

    # =======================================================
    # MODULE 7
    # =======================================================

    print("\nRunning Module 7...")

    wavefront, phase_map = reconstruct_wavefront(

        slopes,

        grid_size=128

    )

    print("Module 7 Completed")

    print("Phase Map Saved :", phase_map)

    # Continue in Part 2...
    
        # =======================================================
    # MODULE 8
    # =======================================================

    print("\nRunning Module 8...")

    zernike = compute_zernike_coefficients(
        wavefront
    )

    print("Module 8 Completed")

    print("Total Zernike Modes :", len(zernike))

    # =======================================================
    # MODULE 9
    # =======================================================

    print("\nRunning Module 9...")

    turbulence = characterize_turbulence(
        wavefront
    )

    print("Module 9 Completed")

    print("Fried Parameter (r0) :", turbulence["r0"])

    print("Coherence Time (tau0) :", turbulence["tau0"])

    # =======================================================
    # MODULE 10
    # =======================================================

    print("\nRunning Module 10...")

    actuator_map, actuator_image = generate_actuator_map(
        wavefront
    )

    print("Module 10 Completed")

    print("Actuator Image :", actuator_image)

    # =======================================================
    # MODULE 11
    # =======================================================

    print("\nRunning Module 11...")

    corrected_wavefront, corrected_image = apply_deformable_mirror(

        wavefront,

        actuator_map

    )

    print("Module 11 Completed")

    print("Corrected Image :", corrected_image)

    print("\n==========================================")
    print("      SH-WFS PROCESSING COMPLETED")
    print("==========================================")

    # =======================================================
    # Return Results
    # =======================================================

    return {

        "reference_centroids": reference_centroids,

        "current_centroids": current_centroids,

        "spot_shifts": spot_shifts,

        "slopes": slopes,

        "phase_map": phase_map,

        "wavefront": wavefront,

        "zernike": zernike,

        "r0": turbulence["r0"],

        "tau0": turbulence["tau0"],

        "turbulence_strength":
            turbulence["turbulence_strength"],

        "actuator_map": actuator_image,

        "corrected_wavefront": corrected_image

    }


# ============================================================
# Test Main Pipeline
# ============================================================

if __name__ == "__main__":

    reference_image = "data/spot_images/sample_reference.png"
    current_image = "data/spot_images/sample_current.png"

    results = run_pipeline(

        reference_image,

        current_image

    )

    print("\n========== FINAL RESULTS ==========\n")

    print("Detected Reference Spots :",
          len(results["reference_centroids"]))

    print("Detected Current Spots :",
          len(results["current_centroids"]))

    print("Spot Shifts :",
          len(results["spot_shifts"]))

    print("Slopes :",
          len(results["slopes"]))

    print("\nZernike Coefficients")

    for mode, value in results["zernike"].items():

        print(mode, ":", value)

    print("\nFried Parameter (r0) :",
          results["r0"])

    print("Coherence Time (tau0) :",
          results["tau0"])

    print("Turbulence Strength :",
          results["turbulence_strength"])

    print("\nSaved Images")

    print("Phase Map :",
          results["phase_map"])

    print("Actuator Map :",
          results["actuator_map"])

    print("Corrected Wavefront :",
          results["corrected_wavefront"])