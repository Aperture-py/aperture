from PIL import Image


def watermark_image(image, wtrmrk_path, corner=2):
    padding = 2
    wtrmrk_img = Image.open(wtrmrk_path)

    #Need to perform size check in here rather than in options.py because this is
    # the only place where we know the size of the image that the watermark is
    # being placed onto
    if wtrmrk_img.width > (image.width - padding * 2) or wtrmrk_img.height > (
            image.height - padding * 2):
        res = (int(image.width / 8.0), int(image.height / 8.0))
        resize_in_place(wtrmrk_img, res)

    if (corner == 0):  #top left
        position = (padding, padding)
    elif (corner == 1):  #top right
        position = ((image.width - wtrmrk_img.width - padding), padding)
    elif (corner == 3):  #bottom left
        position = (padding, (image.height - wtrmrk_img.height - padding))
    else:  #bottom right (default)
        position = ((image.width - wtrmrk_img.width - padding),
                    (image.height - wtrmrk_img.height - padding))

    image.paste(wtrmrk_img, position, wtrmrk_img.convert('RGBA'))


def watermark_text(image, text, corner=3):
    raise NotImplementedError


def resize_in_place(image, res):
    image.thumbnail(res)