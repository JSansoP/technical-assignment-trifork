# Image and Kitti Scaler

This project allows you to scale images and their according bounding boxes in KITTI format.


## External Dependencies
This script uses [PIL](https://pillow.readthedocs.io/en/stable/) to resize the images, and [tqdm](https://tqdm.github.io/) (optional) for the progress and iterations per second.

To install PIL:

```bash
pip install Pillow
```

To install tqdm (optional):
```bash
pip install tqdm
```


## Usage

```bash
python scale_images_and_kitti.py <img_dir> <kitti_dir> <width> <height>
```

Example usage:
```bash
python scale_images_and_kitti.py images kitti_annotations 284 284
```
## More info
This script was done as a technical assignment for [TRIFORK](https://trifork.com/).
