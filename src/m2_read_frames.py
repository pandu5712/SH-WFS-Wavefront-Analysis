import numpy as np
import matplotlib.pyplot as plt

# Load dataset
wavefronts = np.load("dataset/wavefront_dataset.npy")

# Print shape
print("Dataset Shape:", wavefronts.shape)

# Display first frame
plt.figure(figsize=(6,6))
plt.imshow(wavefronts[0], cmap='jet')
plt.colorbar()
plt.title("Wavefront Frame 1")
plt.show()