from PIL import Image, ImageFont # noqa
import facebook # noqa
import json
import sys
import themes as th # noqa
import extra as ex # noqa
import grad_gen as grad

text_center = ex.text_center

'''
    This file contains the main mechanisms for posting to the
    facebook page. It creates the images as well as calculates
    the relevant information regarding the random color.
'''

# Import the details for the page and link to the Facebook API.

env = json.loads(open(sys.path[0] + '/env.json').read())
page_id = env['page_id']
_access_token = env['page_token']
graph = facebook.GraphAPI(access_token=_access_token)

# Import the color dictionary and themes files.
colors = json.loads(open(sys.path[0] + '/json/colors.json').read())
themes = json.loads(open(sys.path[0] + '/json/themes.json').read())

font_path = sys.path[0] + "/fonts/TitilliumWeb-SemiBold.ttf"
font = ImageFont.truetype(font_path, 60)
font_path = sys.path[0] + "/fonts/Inconsolata-Bold.ttf"
name_font = ImageFont.truetype(font_path, 80)
diff_font = ImageFont.truetype(font_path, 60)

image_size = (2500, 2500)
imsw, imsh = image_size

icon_color = (255, 255, 255, 255)

pos = [[[int(imsw/2), int(1.5*imsh/25)]],
       [[int(imsw/2), int(1.5*imsh/25)], 
        [int(imsw/2), int(21*imsh/25)]],
       [[int(imsw/2), int(1.5*imsh/25)],
        [int(imsw/5), int(21*imsh/25)],
        [int(4*imsw/5), int(21*imsh/25)]],
       [[int(imsw/5), int(1.5*imsh/25)],
        [int(4*imsw/5), int(1.5*imsh/25)],
        [int(imsw/5), int(21*imsh/25)],
        [int(4*imsw/5), int(21*imsh/25)]]]

offset = (90, 240)



def label_image(image, num, cols):
    title_pos = pos[num-1]
    for i in range(num):
        r, g, b = cols[i]

        NAMEtext, DIFFtext = ex.conv_color_name(r, g, b, colors)

        HEXtext = "#%02X%02X%02X" % (r, g, b)

        RGBtext = "({}, {}, {})".format(r, g, b)

        diff_size = (300, 70)
        diff_pos = (title_pos[i][0], title_pos[i][1])
        dw, dh = diff_size
        dpw, dph = diff_pos

        diff_bounds = [int(dpw - dw / 2),
                       int(dph - dh / 2),
                       int(dpw + dw / 2),
                       int(dph + dh / 2)]

        name_size = (500, 90)
        name_pos = (title_pos[i][0], title_pos[i][1] + offset[0])
        nw, nh = name_size
        npw, nph = name_pos

        name_bounds = [int(npw - nw / 2),
                       int(nph - nh / 2),
                       int(npw + nw / 2),
                       int(nph + nh / 2)]

        hex_size = (300, 240)
        hex_pos = (title_pos[i][0], title_pos[i][1] + offset[1])
        hw, hh = hex_size
        hpw, hph = hex_pos

        hex_bounds = [int(hpw - hw / 2),
                      int(hph - hh / 2),
                      int(hpw + hw / 2),
                      int(hph + hh / 2)]

        base_image = text_center(DIFFtext,
                                 diff_font,
                                 icon_color,
                                 diff_bounds,
                                 base_image)

        base_image = text_center(NAMEtext,
                                 name_font,
                                 icon_color,
                                 name_bounds,
                                 base_image)

        base_image = text_center(HEXtext,
                                 font,
                                 icon_color,
                                 hex_bounds,
                                 base_image)
    return base_image

def get_base_image(num, cols):
    base_image = grad.get_image(cols, num, image_size)
    return base_image

def get_message(num, cols):
    message = ""
    for i in range(num):
        r, g, b = cols[i]
        message += ex.get_info(r, g, b, colors)
        message += "\n\n"
    return message[:-2]

def retrieve_theme():
    '''
        Retrieves the current theme from the themes subdirectory
        and returns a ColorTheme object with the colors contained
        within that theme.

        Returns:
            A ColorTheme object representing the current theme.
    '''
    # Read what the current theme is.
    with open(sys.path[0] + "/themes/current.txt", "r") as f:
        theme_name = f.readline()
        
    # Get the colors associated with the theme from the themes.json
    # file imported at the start of this script.
    theme = themes[theme_name]

    # Create an empty ColorTheme object with the correct name.
    result = th.ColorTheme(theme_name)

    # Import the colors associated with the theme into the ColorTheme
    # object and return it.
    result.importTheme(theme)
    return result

def post(num):
    current_theme = retrieve_theme()
    cols = [current_theme.getRandom() for j in range(4)]

    theme = "Theme: %s" % current_theme.getName()

    message = get_message(num, cols)

    plain = get_base_image(num, cols)
    plain.save(sys.path[0] + '/plain.png', 'PNG')

    labelled = label_image(plain, num, cols)
    labelled.save(sys.path[0] + '/labelled.png', 'PNG')

    post_id = graph.put_photo(image=open(sys.path[0] + '/labelled.png', 'rb'),
                             message=theme)['post_id']

    with open(sys.path[0] + '/postids/postids.txt', 'a') as f:
        f.write(str(post_id) + '\n')

    graph.put_photo(image=open(sys.path[0] + '/plain.png', 'rb'),
                    message = message, album_path=str(post_id) + '/comments')

    print(message)


def custom(num):
    current_theme = retrieve_theme()
    cols = [current_theme.getRandom() for j in range(4)]

    plain = get_base_image(num, cols)
    plain.save(sys.path[0] + '/plain.png', 'PNG')

    labelled = label_image(plain, num, cols)
    labelled.save(sys.path[0] + '/labelled.png', 'PNG')

    message = get_message(num, cols)
    print(message)