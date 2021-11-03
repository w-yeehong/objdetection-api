from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

import math # ceil()

class ImageHandler:
    valid_image_set = { "JPEG", "PNG", "GIF" }
    colors = list(ImageColor.colormap.values())
    try:
        font = ImageFont.truetype("/code/app/fonts/OpenSans-Regular.ttf", 25)
    except IOError:
        font = ImageFont.load_default()

    def __init__(self, img_bytes):
        try:
            self.img = Image.open(img_bytes)
        except:
            self.img = ""

    def __del__(self):
        if self.is_valid():
            self.img.close()

    def is_valid(self):
        return self.img != "" and self.img.format in self.valid_image_set

    def resize(self, new_width=256, new_height=256, overwrite=True):
        img = ImageOps.fit(self.img, (new_width, new_height), Image.ANTIALIAS)

        if overwrite:
            self.img = img

        return img

    def draw_boxes(self, boxes, class_names, scores, max_boxes=10, min_score=0.2):
        for i in range(min(boxes.shape[0], max_boxes)):
            if scores[i] >= min_score:
                ymin, xmin, ymax, xmax = tuple(boxes[i])
                display_str = "{}: {}%".format(class_names[i].decode("ascii"),
                                int(100 * scores[i]))
                color = self.colors[hash(class_names[i]) % len(self.colors)]
                self.draw_bounding_box(
                    ymin,
                    xmin,
                    ymax,
                    xmax,
                    color,
                    display_str_list=[display_str])

        return self.img

    def draw_bounding_box(self, ymin, xmin, ymax, xmax, color, thickness=4, display_str_list=()):
        draw = ImageDraw.Draw(self.img)
        img_width, img_height = self.img.size

        (left, right, top, bottom) = (xmin * img_width, xmax * img_width,
                                        ymin * img_height, ymax * img_height)
        draw.line([(left, top), (left, bottom), (right, bottom), (right, top), (left, top)],
            width=thickness,
            fill=color)

        # If the total height of the display strings added to the top of the bounding
        # box exceeds the top of the image, stack the strings below the bounding box
        # instead of above.
        display_str_heights = [self.font.getsize(ds)[1] for ds in display_str_list]
        # Each display_str has a top and bottom margin of 0.05x.
        total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

        if top > total_display_str_height:
            text_bottom = top
        else:
            text_bottom = top + total_display_str_height

        # Reverse list and print from bottom to top.
        for display_str in display_str_list[::-1]:
            text_width, text_height = self.font.getsize(display_str)
            margin = math.ceil(0.05 * text_height)
            draw.rectangle([(left, text_bottom - text_height - 2 * margin),
                            (left + text_width, text_bottom)], fill=color)
            draw.text((left + margin, text_bottom - text_height - margin),
                      display_str,
                      fill="black",
                      font=self.font)
            text_bottom -= text_height - 2 * margin
