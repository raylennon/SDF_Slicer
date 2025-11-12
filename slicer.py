import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

a = np.array([1, 2, 3])

# Printer resolution; this is machine-specific, not slice-specific!
xres = 299.73  # DPI
yres = 299.73  # DPI
n_layers = 10
layer_height = 0.018

# File prefix for outputted slices.
prefix = "slice_"


# Bounding area size in [mm]
bounds = np.array([30, 30])

# The bounding area maps to...  [mm -> in] [ in -> px]
mapx = lambda x: xres * 0.0393701 * x
mapy = lambda y: yres * 0.0393701 * y
x_samp = np.linspace(0, bounds[0], int(np.ceil(mapx(bounds[0]))))
y_samp = np.linspace(0, bounds[1], int(np.ceil(mapy(bounds[1]))))
x, y = np.meshgrid(x_samp, y_samp)
print(f"Max value of x_samp: {np.max(x_samp)}")


def circle(x, y, loc, r):
    return np.sqrt((x - loc[0]) ** 2 + (y - loc[1]) ** 2) - r


# x,y in units of mm
def domain(x, y, z):
    radius = 12.7

    nx = 

    return circle(x, y, [15, 15], radius)

for i in range(n_layers):
    z = i * layer_height

    # Here, only a single color is used. 
    data = 255 * (domain(x, y, z) < 0).astype(np.uint8)
    
    # Tiling into RGBA format. This means - for now - the file has white, opaque features on a background of (0,0,0,0) (transparent)
    data = np.repeat(data[:,:,None],4,axis=2)

    print (f"Data shape -> {data.shape}")
    im = Image.fromarray(data)
    im.save(f"outputs/slice_{i+1:02d}.png")


fig, ax = plt.subplots()
plt.imshow(
   data, extent=[0, bounds[0], 0, bounds[1]], interpolation="nearest"
)

# plt.imshow(domain(x,y)>0)
plt.xlabel("X [mm]")
plt.ylabel("Y [mm]")
plt.colorbar()
plt.savefig("domain_graph.png")

print(len(x_samp))
print(len(y_samp))
