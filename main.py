#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author WayJun
# @date 2022/1/21
# @file test1.py
import os
import colorama
from PIL import Image, ImageDraw, ImageFont
from colorama import init,Fore,Back,Style
init(autoreset=True)

#################################
# 给图片加上水印
#################################

class Water:
    def __init__(self):
        # 颜色对应http://www.yuangongju.com/color
        self.color_dict = {
            'white': (255, 255, 255, 255),
            'black': (0, 0, 0, 255),
            'gray': (205, 201, 201, 255),
            'red': (255, 0, 0, 255),
            'yellow': (255, 215, 0, 255),
            'blue': (0, 0, 170, 255),
            'purple': (205, 105, 201, 255),
            'green': (0, 205, 0, 255)
        }
        self.position_list = [1, 2, 3, 4]

    def one_water(self, image, text, position=1, fontsize=20, fontcolor='black'):
        """
        普通照片水印
        params:
            image:图片
            text:水印文字
            position:水印位置
                    1：左上
                    2：右上
                    3：右下
                    4：左下
            fontsize:字体大小
            fontcolor:字体颜色
                    [white, black, gray, red, yellow, blue, purple, green]
        """
        if position not in self.position_list:
            position = 1
        h, w = image.size[:2]
        keys = self.color_dict.keys()
        if fontcolor not in keys:
            fontcolor = 'black'
        color = self.color_dict[fontcolor]
        fnt = ImageFont.truetype('./fonts/FZYTK.TTF', fontsize)
        im = image.convert('RGBA')
        mask = Image.new('RGBA', im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(mask)
        size_h, size_w = d.textsize(text, font=fnt)
        alpha = 5
        if position == 1:
            weizhi = (0 + alpha, 0 + alpha)
        elif position == 2:
            weizhi = (h - size_h - alpha, 0 + alpha)
        elif position == 3:
            weizhi = (h - size_h - alpha, w - size_w - alpha)
        else:
            weizhi = (0 + alpha, w - size_w - alpha)
        # position 为左上角位置
        d.text(weizhi, text, font=fnt, fill=color)
        out = Image.alpha_composite(im, mask)
        return out

    def fill_water(self, image, text, fontsize):
        """
        半透明水印，布满整张图，并且自动旋转45°
        params:
            image:图片
            text:文字
            fontsize:文字大小
        """
        font = ImageFont.truetype('./font/hwkt.ttf', fontsize)
        # 添加背景
        new_img = Image.new('RGBA', (image.size[0] * 3, image.size[1] * 3), (255, 255, 255, 255))
        new_img.paste(image, image.size)
        # 添加水印
        font_len = len(text)
        rgba_image = new_img.convert('RGBA')
        text_overlay = Image.new('RGBA', rgba_image.size, (0, 0, 0, 0))
        image_draw = ImageDraw.Draw(text_overlay)
        for i in range(0, rgba_image.size[0], font_len * 40 + 100):
            for j in range(0, rgba_image.size[1], 200):
                # print(f'i:{i}, j:{j}, text:{text}, font:{font}')
                image_draw.text((i, j), text, font=font, fill=(255, 0, 100, 100))
        text_overlay = text_overlay.rotate(30)
        image_with_text = Image.alpha_composite(rgba_image, text_overlay)
        image_with_text = image_with_text.crop((image.size[0], image.size[1], image.size[0] * 2, image.size[1] * 2))
        return image_with_text
if __name__ == '__main__':
    print('\033[1;31m---欢迎使用小胡牌图片批量加水印---\n---请确保该文件目录包含以下文件夹:images,ok,font---\n---原图片放入images文件夹下,执行本文件后查看ok文件夹是否成功添加水印---\033[0m \n')
    text = input('请输入文字水印内容:')
    print('\n程序执行中,请稍后......\n\033[1;32m处理日志:\033[0m')
    inputs="./images/"
    output="./ok/"
    count=0
    water = Water()
    filelist=os.listdir(inputs)
    for files in filelist:
        img = Image.open(os.path.join(inputs,files))
        fill_img = water.fill_water(img, text, fontsize=36)
        # 一定要保存为png格式
        img_path = os.path.join(output,files).replace('.jpg', '.png')
        fill_img.save(img_path)
        print('\033[1;32m'+str(files)+'=====>添加水印成功\033[0m')
        count+=1
    print('\n\033[1;37;46m本次共处理'+str(count)+'张图片\033[0m\n')
    input('请按任意键退出本程序')