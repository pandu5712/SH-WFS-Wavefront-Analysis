from hcipy import *
import numpy as np
import matplotlib.pyplot as plt

# Create pupil grid
pupil_grid = make_pupil_grid(128)

# Atmospheric parameters
Cn_squared = 1e-14
outer_scale = 20

# Create atmospheric layer
layer = InfiniteAtmosphericLayer(
    pupil_grid,
    Cn_squared,
    outer_scale,
    velocity=10
)

# Generate Time-Series Frames
wavefronts = []

time_steps = 100

for i in range(time_steps):

    # Change turbulence with time
    layer.evolve_until(i * 0.01)

    # Generate wavefront phase map
    wf = layer.phase_for(500e-9)

    # Store frame
    wavefronts.append(wf.shaped)

# Convert to NumPy array
wavefronts = np.array(wavefronts)

print(wavefronts.shape)

# Save dataset
np.save("dataset/wavefront_dataset.npy", wavefronts)

print("Dataset saved successfully!")

plt.imshow(wavefronts[0], cmap='jet')
plt.colorbar()
plt.title("Wavefront Frame 1")
plt.show()

import os

np.save("dataset/wavefront_dataset.npy", wavefronts)

print("Dataset saved successfully!")
print("Location:", os.path.abspath("dataset/wavefront_dataset.npy"))