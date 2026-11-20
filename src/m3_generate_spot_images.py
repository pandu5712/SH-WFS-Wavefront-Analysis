# 3.generate_spot_images.py

import numpy as np
import matplotlib.pyplot as plt
import os

# Load wavefront dataset
wavefronts = np.load("dataset/wavefront_dataset.npy")

# Create output folder
os.makedirs("data/spot_images", exist_ok=True)

# Generate spot images
for i in range(len(wavefronts)):

    frame = wavefronts[i]

    # Normalize values to range 0-255
    normalized = (frame - frame.min()) / (frame.max() - frame.min())

    image = (normalized * 255).astype(np.uint8)

    # File name
    filename = f"data/spot_images/spot_{i+1:03d}.bmp"

    # Save image
    plt.imsave(filename, image, cmap='gray')

print("Spot images generated successfully!")

# Display first image
plt.figure(figsize=(6,6))
plt.imshow(image, cmap='gray')
plt.title("Generated Spot Image")
plt.axis('off')
plt.show()