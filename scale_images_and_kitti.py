import os
import sys
try:
    from PIL import Image
except ImportError:
    print("PIL is not installed. Please install with: pip install Pillow")
    sys.exit(1)
verbose = True
try:
    from tqdm import tqdm
except ImportError:
    print("tqdm is not installed. Progress will not be shown. Please install with: pip install tqdm")
    verbose = False

def create_and_clear_dir(dir_path):
    '''
    Creates a directory if it doesn't exist, and clears it if it does
    '''
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        print("Created directory: {}".format(dir_path))
    else:
        #Delete all files in the directory
        for file in os.listdir(dir_path):
            os.remove(os.path.join(dir_path, file))
        print("Cleared directory: {}".format(dir_path))

def main(img_dir, kitti_dir, desired_width, desired_height):
    
    #We get the parent directory of the images directory, and create a new directory for the scaled images and kitti files
    parent_dir = os.path.dirname(os.path.abspath(img_dir))
    print("Parent directory: {}".format(parent_dir))
    img_output_dir = os.path.join(parent_dir, "scaled_images")
    kitti_output_dir = os.path.join(parent_dir, "scaled_annotations")
    create_and_clear_dir(img_output_dir)
    create_and_clear_dir(kitti_output_dir)
    
    #We use scandir instead of listdir because it is safer for large directories, sice
    # it returns an iterator object instead of a list. So for computer vision applications
    # where we have a lot of images, it's safer.
    print("Resizing images and kitti files...")
    with os.scandir(img_dir) as images:
        #If tqdm is installed, we show a progress bar or iterations per second. Otherwise, we just iterate over the images
        if verbose:
            images = tqdm(images)
        # For each image in the directory
        for image in images:
            #We open the image with PIL
            tmp = Image.open(image.path)
            #We get the original width and height of the image
            original_width, original_height = tmp.size
            #We resize the image to the desired width and height
            tmp = tmp.resize((desired_width, desired_height))
            #We save the image in the output directory
            tmp.save(os.path.join(img_output_dir, image.name))
            #We open the corresponding kitti file
            with open(os.path.join(kitti_dir, image.name[:-3] + "txt"), "r") as kitti_file:
                kitti_data = kitti_file.readlines()
                kitti_data_out = []
                #For each line in the kitti file
                for line in kitti_data:
                    #We split the kitti data into a list
                    kitti_data_list = line.split(" ")
                    #line format: class truncation occlusion alpha x1 y1 x2 y2 h w l x y z ry
                    # We need to change the x1, y1, x2, y2 values so that they are relative to the new image size
                    #Since https://docs.nvidia.com/tao/tao-toolkit/text/data_annotation_format.html#object-detection-kitti-format
                    # states that the x1, y1, x2, y2 values are floats, we dont need to round them, and can save them as floats
                    # So we just multiply them by the ratio of the new image size to the old image size
                    kitti_data_list[4] = str(float(kitti_data_list[4]) * desired_width / original_width)
                    kitti_data_list[5] = str(float(kitti_data_list[5]) * desired_height / original_height)
                    kitti_data_list[6] = str(float(kitti_data_list[6]) * desired_width / original_width)
                    kitti_data_list[7] = str(float(kitti_data_list[7]) * desired_height / original_height)
                    kitti_data_out.append(" ".join(kitti_data_list))
            #We save the kitti file in the output directory
            with open(os.path.join(kitti_output_dir, image.name[:-3] + "txt"), "w") as kitti_file_out:
                kitti_file_out.writelines(kitti_data_out)


#Usage (from the root directory of the project): python scale_images_and_kitti.py images kitti_annotations 284 284

if __name__  == "__main__":
    args = sys.argv[1:]
    if len(args) != 4:
        print("Usage: python scale_images_and_kitti.py <img_dir> <kitti_dir> <width> <height>")
        sys.exit(1)
    img_dir = args[0]
    kitti_dir = args[1]
    desired_width = int(args[2])
    desired_height = int(args[3])
    main(img_dir, kitti_dir, desired_width, desired_height)