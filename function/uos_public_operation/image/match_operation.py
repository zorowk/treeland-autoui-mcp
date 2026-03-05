"""
匹配图片
"""
# -*- coding:utf-8 -*-


import os
import cv2 as cv


class ImageOperation:
    """
        图像相关操作
    """
    def __init__(self):
        pass

    def match_image(self, image, template_image, confidencevalue=0.7):
        '''
        模板匹配图片
        :param image:大图
        :param template_image: 模板图片
        :param confidencevalue: 识别精度
        :return: 字典 包含['rectangle']访问匹配到的图片左顶点图片宽高(left, top, width, height)  ['result']访问匹配到的图片中点 or None
        '''
        # 打开模板图片
        image.save(os.path.dirname(os.path.abspath(__file__))+'/screen.png')
        image = cv.imread(os.path.dirname(os.path.abspath(__file__))+'/screen.png')
        template_image = cv.imread(template_image)
        # 调用matchTemplate方法进行匹配
        result = cv.matchTemplate(image, template_image, cv.TM_CCOEFF_NORMED)
        pos_start = cv.minMaxLoc(result)[3]
        # 匹配对象的中心坐标x pos_y
        pos_x = int(pos_start[0]) + int(template_image.shape[1] / 2)
        pos_y = int(pos_start[1]) + int(template_image.shape[0] / 2)
        # 匹配度
        similarity = cv.minMaxLoc(result)[1]
        # print(similarity)
        if similarity < confidencevalue:
            return None
        return {'result' : (pos_x, pos_y), 'rectangle':(pos_start[0], pos_start[1], template_image.shape[1], template_image.shape[0])}
