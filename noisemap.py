import numpy as np
from noise import pnoise2
import matplotlib.pyplot as plt

def noise_value(
        x: int, 
        y: int,
        scale: float = 5.0, 
        octaves: int = 8, 
        persistence: float = 0.5,
        lacunarity: float = 2.0, 
        seed: int = 42
        ) -> float:
    
    value = pnoise2(
        x / scale,
        y / scale,
        octaves=octaves,
        persistence=persistence,
        lacunarity=lacunarity,
        base=seed
    )

    return (value + 1) / 2  # Normalize to [0, 1]

def generate_noise_map(width: int, height: int, **noise_params) -> np.ndarray:
    noise_map = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            noise_map[y][x] = noise_value(x, y, **noise_params)
    return noise_map

def plot_noise_map(noise_map: np.ndarray):
    plt.figure(figsize=(8, 8))
    plt.imshow(noise_map, cmap='terrain')
    plt.colorbar()
    plt.title("Noise Map")
    plt.axis('off')
    plt.savefig("noise_map.png")
    plt.close()

### DEBUGGING ###

x = 20
y = 20

plot_noise_map(generate_noise_map(x, y))