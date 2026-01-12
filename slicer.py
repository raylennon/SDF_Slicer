# in command line: python -m pip install numpy
import numpy as np # numerical processing; arrays. 
# python -m pip install matplotlib; this is for plotting
import matplotlib.pyplot as plt

# processes images; just for output
from PIL import Image

# Printer resolution; this is machine-specific, not slice-specific!
xres = 299.73  # DPI
yres = 299.73  # DPI

# integer number of layers
n_layers = 100

# layer height,specific to printer [mm]
layer_height = 0.018

# droplet size in mm
d_size = (1/xres) * 25.4

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
print(f"1 Droplet = {1e3*bounds[0]/len(x_samp):0.4} um")


def circle(x, y, loc, r):
    return np.sqrt((x - loc[0]) ** 2 + (y - loc[1]) ** 2) - r

def box(x,y,loc,size):
    return np.maximum(x-loc[0], y-loc[1])-size/2

base = 3

# x,y in units of mm
def domain(x, y, z):
    # return circle(x,y,[15,15], 15)
    if z/layer_height < base:
        radius = 10
    else:
        radius = d_size*0.5


    x_space = 1 # mm
    y_space = 1.5 # mm

    # these following four lines repeat space with increment x_space

    ix_x = np.floor(x / x_space)
    ix_y = np.floor(y / y_space)
    x -= x_space * ix_x
    y -= y_space * ix_y


    cutoff = (ix_x < np.floor(bounds[0]/x_space)) * (ix_y < np.floor(bounds[1]/y_space))

    return box(x, y, 2*[radius], 2*radius) * cutoff

for i in range(n_layers):

    # current z coordinate corresponding to layer
    z = i * layer_height

    # Here, only a single color is used.
    # in plain terms: output 255 wherever domain is less than 0
    data = 255 * (domain(x, y, z) < 0).astype(np.uint8)

    # Creates a Nx3 color array
    data = np.repeat(data[:,:,None],1,axis=2)
    if i < base:
        data = np.dstack((data, ~data, ~data, 255*np.ones(data.shape[:-1], dtype=np.uint8)))
    else:
        data = np.dstack((np.uint8(0.5*data), ~data, ~data, 255*np.ones(data.shape[:-1], dtype=np.uint8)))

    im = Image.fromarray(data)
    im.save(f"outputs/slice_{i+1:03d}.png")


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
