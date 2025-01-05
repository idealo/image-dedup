from pathlib import PurePath
from typing import List, Union, Tuple

import numpy as np
from PIL import Image

# enables Pillow HEIF support using https://github.com/bigcat88/pillow_heif
# pi-heif is the same codebase, but more light, HEIF decoder-only version

from pi_heif import register_heif_opener
register_heif_opener()

from imagededup.utils.logger import return_logger


IMG_FORMATS = ['JPEG', 'PNG', 'BMP', 'MPO', 'PPM', 'TIFF', 'GIF', 'WEBP', 'HEIF']
logger = return_logger(__name__)


def _check_3_dim(image_arr_shape: Tuple) -> None:
    """
    Checks that image array is represented in the (x, y, 3) format.

    Args:
        image_arr_shape: Shape of the image numpy array.
    """
    assert image_arr_shape[2] == 3, (
        f'Received image array with shape: {image_arr_shape}, expected image array shape is '
        f'(x, y, 3)'
    )


def _add_third_dim(image_arr_2dim: np.ndarray) -> np.ndarray:
    """
    Converts a 2-d image array to 3-d by repeating the array thrice along the 3rd dimension.

    Args:
        image_arr_2dim: 2-dimensional image array.

    Returns:
        An expanded 3-dimensional numpy image array with input 2-dimensional array repeated along the 3rd dimension.
    """
    image_arr_3dim = np.tile(
        image_arr_2dim[..., np.newaxis], (1, 1, 3)
    )  # convert (x, y) to (x, y, 3) (grayscale to rgb)
    return image_arr_3dim


def _raise_wrong_dim_value_error(image_arr_shape: Tuple) -> None:
    """
    Raises ValueError when image array shape is wrong.

    Args:
        image_arr_shape: Image array shape.
    """
    raise ValueError(
        f'Received image array with shape: {image_arr_shape}, expected number of image array dimensions are 3 for '
        f'rgb image and 2 for grayscale image!'
    )


def check_image_array_hash(image_arr: np.ndarray) -> None:
    """
    Checks the sanity of the input image numpy array for hashing functions.

    Args:
        image_arr: Image array.
    """
    image_arr_shape = image_arr.shape
    if len(image_arr_shape) == 3:
        _check_3_dim(image_arr_shape)
    elif len(image_arr_shape) > 3 or len(image_arr_shape) < 2:
        _raise_wrong_dim_value_error(image_arr_shape)


def expand_image_array_cnn(image_arr: np.ndarray) -> np.ndarray:
    """
    Checks the sanity of the input image numpy array for cnn and converts the grayscale numpy array to rgb by repeating
    the array thrice along the 3rd dimension if a 2-dimensional image array is provided.

    Args:
        image_arr: Image array.

    Returns:
        A 3-dimensional numpy image array.
    """
    image_arr_shape = image_arr.shape
    if len(image_arr_shape) == 3:
        _check_3_dim(image_arr_shape)
        return image_arr
    elif len(image_arr_shape) == 2:
        image_arr_3dim = _add_third_dim(image_arr)
        return image_arr_3dim
    else:
        _raise_wrong_dim_value_error(image_arr_shape)


def preprocess_image(
    image, target_size: Tuple[int, int] = None, grayscale: bool = False
) -> np.ndarray:
    """
    Take as input an image as numpy array or Pillow format. Returns an array version of optionally resized and grayed
    image.

    Args:
        image: numpy array or a pillow image.
        target_size: Size to resize the input image to.
        grayscale: A boolean indicating whether to grayscale the image.

    Returns:
        A numpy array of the processed image.
    """
    if isinstance(image, np.ndarray):
        image = image.astype('uint8')
        image_pil = Image.fromarray(image)

    elif isinstance(image, Image.Image):
        image_pil = image
    else:
        raise ValueError('Input is expected to be a numpy array or a pillow object!')

    if target_size:
        image_pil = image_pil.resize(target_size, Image.LANCZOS)

    if grayscale:
        image_pil = image_pil.convert('L')

    return np.array(image_pil).astype('uint8')


def load_image(
    image_file: Union[PurePath, str],
    target_size: Tuple[int, int] = None,
    grayscale: bool = False,
    img_formats: List[str] = IMG_FORMATS,
) -> np.ndarray:
    """
    Load an image given its path. Returns an array version of optionally resized and grayed image. Only allows images
    of types described by img_formats argument.

    Args:
        image_file: Path to the image file.
        target_size: Size to resize the input image to.
        grayscale: A boolean indicating whether to grayscale the image.
        img_formats: List of allowed image formats that can be loaded.
    """
    try:
        img = Image.open(image_file)

        # validate image format
        if img.format not in img_formats:
            logger.warning(f'Invalid image format {img.format}!')
            return None

        else:
            if img.mode != 'RGB':
                # convert to RGBA first to avoid warning
                # we ignore alpha channel if available
                img = img.convert('RGBA').convert('RGB')

            img = preprocess_image(img, target_size=target_size, grayscale=grayscale)

            return img

    except Exception as e:
        logger.warning(f'Invalid image file {image_file}:\n{e}')
        return None
