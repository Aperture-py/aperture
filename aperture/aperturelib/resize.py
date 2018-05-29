def resize_image(image, tuple_wh, preserve_aspect=True):
    """Resizes an instance of a PIL Image.

    Args:
        image: An instance of a PIL Image.
        tuple_wh: A tuple containing the (width, height) for resizing.
        preserve_aspect: A boolean that determines whether or not the
            resizing should preserve the image's aspect ratio.

    Returns: An instance of a PIL Image.
    """
    if preserve_aspect:
        image.thumbnail(tuple_wh)
    else:
        image.resize(tuple_wh)

    return image
