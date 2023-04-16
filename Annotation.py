import napari
import glob
import aicsimageio
from tifffile import imsave
from napari.utils import nbscreenshot

def save_roi_callback(viewer, filepath, output_directory):
    roi_image = viewer.layers.selection.active.data
    region_name = input("Enter the region name: ")
    output_file_path = f"{output_directory}/{filepath}_{region_name}.tif"
    imsave(output_file_path, roi_image)

# Replace with the path to your .czi files
input_directory = "/path/to/your/czi/files"

# Replace with the path to save the output .tif files
output_directory = "/path/to/output/screenshots"

# Read the .czi files
filepaths = glob.glob(input_directory + "/*.czi")

# Launch napari viewer
viewer = napari.Viewer()

for filepath in filepaths:
    # Load .czi image
    image = aicsimageio.imread(filepath)

    # Add image to the napari viewer
    layer = viewer.add_image(image, name=filepath, scale=(1, 1, 1))

    print(f"Annotate the region of interest for the image {filepath} and press 's' to save the ROI as a .tif file.")
    viewer.bind_key('s', save_roi_callback, filepath=filepath, output_directory=output_directory)

    # Wait for user input before moving on to the next image
    input("Press Enter to continue to the next image...")

    # Remove the current image layer before loading the next one
    viewer.layers.remove(layer)

napari.run()
