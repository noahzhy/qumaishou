from pymatting import cutout

cutout(
    # input image path
    r"img_fusion\image_matting\data\input\20000759811_1.png",
    # input trimap path
    r"img_fusion\image_matting\data\trimap\20000759811_1.png",
    # output cutout path
    "cutout.png"
)