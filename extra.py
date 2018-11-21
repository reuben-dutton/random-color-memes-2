from PIL import Image, ImageDraw, ImageFilter
import math
import string


def text_center(text, font, fill, bounds, image):
    x1, y1, x2, y2 = bounds
    W, H = (x2 - x1, y2 - y1)
    offset = (3, 3)

    shadow = Image.new("RGBA", image.size)
    canvas = ImageDraw.Draw(shadow)
    w, h = canvas.textsize(text, font=font)
    shadow_fill = (0, 0, 0, 255)
    for i in range(1, -1, -2):
        for j in range(1, -1, -2):
            pos = (x1 + (W - w) / 2 + i * offset[0], 
                y1 + (H - h) / 2 + j * offset[1])
            canvas.multiline_text(pos,
                                text,
                                font=font,
                                fill=shadow_fill,
                                spacing=10,
                                align="center")
    for i in range(5):
        shadow = shadow.filter(ImageFilter.BLUR)
    image = Image.alpha_composite(image, shadow)
    canvas = ImageDraw.Draw(image)
    w, h = canvas.textsize(text, font=font)
    pos = (x1 + (W - w) / 2, y1 + (H - h) / 2)
    canvas.multiline_text(pos,
                          text,
                          font=font,
                          fill=fill,
                          spacing=10,
                          align="center")
    return image

def convert_hsv(r, g, b):
    '''
        Converts a color in RGB format to HSV format.

        Args:
            r: The red content of the color.
            g: The green content of the color.
            b: The blue content of the color.

        Returns:
            A tuple containing the hue, shade and value
            of the given color.
    '''
    # Scale the r, g, b values between 0 and 1.
    r_inv = r / 255
    g_inv = g / 255
    b_inv = b / 255

    # Find the maximum and minimum value, and the
    # difference between the two.
    c_max = max(r_inv, g_inv, b_inv)
    c_min = min(r_inv, g_inv, b_inv)
    delta = c_max - c_min

    # Calculate the hue value scaled from 0 to 6.
    if delta == 0:
        h = 0
    elif c_max == r_inv:
        h = ((g_inv - b_inv) / delta) % 6
    elif c_max == g_inv:
        h = ((b_inv - r_inv) / delta) + 2
    elif c_max == b_inv:
        h = ((r_inv - g_inv) / delta) + 4

    # Calculate the shade value scaled from 0 to 1.
    if c_max == 0:
        s = 0
    else:
        s = delta / c_max

    # Return the values scaled properly (to degrees and percentage).
    return (h * 60, s * 100, c_max * 100)

def convert_cmyk(r, g, b):
    '''
        Converts a color in the RGB color space to one in the
        CMYK color space.

        Args:
            r: The red content of the color.
            g: The green content of the color.
            b: The blue content of the color.

        Returns:
            A tuple containing the cyan, magenta, yellow and
            key content of the given color.
    '''

    # Scale the r, g, b values between 0 and 1.
    r_inv = r/255
    g_inv = g/255
    b_inv = b/255

    # Find the key content of the color.
    k = 1 - max(r_inv, g_inv, b_inv)

    # Find the cyan, magenta and yellow content of
    # the color and return.
    if k == 1:
        return (0, 0, 0, 1)
    else:
        c = (1 - r_inv - k)/(1 - k)
        m = (1 - g_inv - k)/(1 - k)
        y = (1 - b_inv - k)/(1 - k)
        return (c, m, y, k)

def conv_color_name(r, g, b, colors):
    min_diff = math.sqrt(3 * 255**2)
    for color, rgb in colors.items():
        p = [r-rgb[0], g-rgb[1], b-rgb[2]]
        dist = math.sqrt(p[0]**2 + p[1]**2 + p[2]**2)
        if dist < min_diff:
            min_diff = dist
            if "PMS" in color:
                NAMEtext = color.upper()
            else:
                NAMEtext = string.capwords(color)
    newNAMEtext = ""
    for word in NAMEtext.split():
        if len(newNAMEtext) > 15:
            newNAMEtext += "\n"
        newNAMEtext += word + " "
    NAMEtext = newNAMEtext[:-1]

    if min_diff == 0:
        DIFFtext = ""
    elif min_diff < 5:
        DIFFtext = "Identical to"
    elif min_diff < 10:
        DIFFtext = "Very close to"
    elif min_diff < 15:
        DIFFtext = "Similiar to"
    elif min_diff < 20:
        DIFFtext = "Looks like"
    else:
        DIFFtext = "Somewhat like"

    return [NAMEtext, DIFFtext]

def get_info(r, g, b, colors):
    hexa = "#%02X%02X%02X" % (r, g, b)
    rgb = "({}, {}, {})".format(r, g, b)
    h, s, v = convert_hsv(r, g, b)
    hsv = "(%.1f°, %.1f%%, %.1f%%)" % (h, s, v)
    c, m, y, k = convert_cmyk(r, g, b)
    cmyk = "(%.2f, %.2f, %.2f, %.2f)" % (c, m, y, k)
    approx_wavelength = -6.173261112*(10**-11)*(h**6) \
    + 5.515102757*(10**-8)*(h**5) \
    - 1.890868343*(10**-5)*(h**4) \
    + 3.063661184*(10**-3)*(h**3) \
    - 0.2277357517*(h**2) \
    + 4.885819756*h + 650
    if not (380 < approx_wavelength < 720):
        wave = "N/A"
    else:
        wave = '%.2fnm' % approx_wavelength
    name, diff = conv_color_name(r, g, b, colors)
    message = "{} {}".format(diff, name)
    message += "\n RGB: {}".format(rgb)
    message += "\n HEX: {}".format(hexa)
    message += "\n HSV: {}".format(hsv)
    message += "\n CMYK: {}".format(cmyk)
    message += "\n Approximate Wavelength: {}".format(wave)
    return message
