#!/usr/bin/env python
# -*- coding: cp936 -*-
from time import  sleep
from pytesseract import *
from selenium import webdriver
from PIL import Image, ImageEnhance
driver=webdriver.Firefox()
driver.get("http://amstest4.phkjcredit.com/ams_web/")#打开网页
driver.maximize_window()
driver.save_screenshot('verifyCode.png')#截取当前网页，该网页有我们需要的验证码
sleep(2)
#定位验证码
imgelement = driver.find_element_by_xpath("//*[@id=\"loginFrom\"]/div[3]/div/i/img")
#获取验证码x，y坐标
location=imgelement.location
print(location)
#获取验证码的长宽
size=imgelement.size
print(size)
#driver.quit()
#写成我们需要的截取的位置的坐标
rangle=(int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height']))
print(rangle)
#打开截图
img=Image.open('verifyCode.png')
#使用Image的crop函数，从截图中再次截取我们需要的区域
imgry=img.crop(rangle)
imgry.save('getVerifyCode.png')
img1=Image.open('getVerifyCode.png')
img2=img1.convert('L')#图像加强，二值化
sharpness =ImageEnhance.Contrast(img2)#对比度增强
sharp_img = sharpness.enhance(2.0)
sharp_img.save("newVerifyCode.png")
newVerify = Image.open('newVerifyCode.png')
# 使用image_to_string识别验证码
text=image_to_string(newVerify).strip() #使用image_to_string识别验证码
#text1 = image_to_string('newVerifyCode.png').strip()
print (text)