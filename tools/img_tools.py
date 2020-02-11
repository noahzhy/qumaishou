import colorsys
from PIL import Image, ImageOps, ImageDraw, ImageFont
 
def get_dominant_color(image):
    #颜色模式转换，以便输出rgb颜色值
    image = image.convert('RGBA')
    #生成缩略图，减少计算量，减小cpu压力
    image.thumbnail((36, 36))
    #原来的代码此处为None
    max_score = 0
    # 原来的代码此处为None，但运行出错，改为0以后 运行成功，
    # 原因在于在下面的 score > max_score的比较中，
    # max_score的初始格式不定
    # dominant_color = 0
    
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        # 必须跳过纯黑色
        if a == 0:
            continue
        
        saturation = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)[1]
        y = min(abs(r*2104 + g*4130 + b*802 + 4096 + 131072) >> 13, 235)
        y = (y-16.0)/(235-16)
        # 忽略高亮色
        if y > 0.9:
            continue
        # Calculate the score, preferring highly saturated colors.
        # Add 0.1 to the saturation so we don't completely ignore grayscale
        # colors by multiplying the count by zero, but still give them a low
        # weight.
        score = (saturation + 0.1) * count
        if score > max_score:
            max_score = score
            # dominant_color = (r, g, b)
            hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b).upper()

    return hex_color


def add_border(input_image, border, color=0):
    # 先剪裁边框宽度，再扩展出边框来
    img = ImageOps.crop(input_image, border=border)
 
    if isinstance(border, int) or isinstance(border, tuple):
        bimg = ImageOps.expand(img, border=border, fill=color)
    else:
        raise RuntimeError('Border is not an integer or tuple!')
 
    return bimg


def add_text(img, text, font, size, color, position):
    draw = ImageDraw.Draw(img) #修改图片
    f = ImageFont.truetype('img_fusion/font/huangyouti.ttf', size)
    draw.text(position, text, color, font=f) #利用ImageDraw的内置函数，在图片上写入文字
    # img.show()
    return img


def text_border(im, x, y, text, font, fillcolor, shadowcolor, bs):
    draw = ImageDraw.Draw(im)
    # thin border
    draw.text((x - bs, y), text, font=font, fill=shadowcolor)
    draw.text((x + bs, y), text, font=font, fill=shadowcolor)
    draw.text((x, y - bs), text, font=font, fill=shadowcolor)
    draw.text((x, y + bs), text, font=font, fill=shadowcolor)
 
    # thicker border
    draw.text((x - bs, y - bs), text, font=font, fill=shadowcolor)
    draw.text((x + bs, y - bs), text, font=font, fill=shadowcolor)
    draw.text((x - bs, y + bs), text, font=font, fill=shadowcolor)
    draw.text((x + bs, y + bs), text, font=font, fill=shadowcolor)
 
    # now draw the text over it
    draw.text((x, y), text, font=font, fill=fillcolor)

    return im