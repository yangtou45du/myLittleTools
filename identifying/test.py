#!/usr/bin/env python
# -*- coding: cp936 -*-
from time import  sleep
from pytesseract import *
from selenium import webdriver
from PIL import Image, ImageEnhance
driver=webdriver.Firefox()
driver.get("http://amstest4.phkjcredit.com/ams_web/")#����ҳ
driver.maximize_window()
driver.save_screenshot('verifyCode.png')#��ȡ��ǰ��ҳ������ҳ��������Ҫ����֤��
sleep(2)
#��λ��֤��
imgelement = driver.find_element_by_xpath("//*[@id=\"loginFrom\"]/div[3]/div/i/img")
#��ȡ��֤��x��y����
location=imgelement.location
print(location)
#��ȡ��֤��ĳ���
size=imgelement.size
print(size)
#driver.quit()
#д��������Ҫ�Ľ�ȡ��λ�õ�����
rangle=(int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height']))
print(rangle)
#�򿪽�ͼ
img=Image.open('verifyCode.png')
#ʹ��Image��crop�������ӽ�ͼ���ٴν�ȡ������Ҫ������
imgry=img.crop(rangle)
imgry.save('getVerifyCode.png')
img1=Image.open('getVerifyCode.png')
img2=img1.convert('L')#ͼ���ǿ����ֵ��
sharpness =ImageEnhance.Contrast(img2)#�Աȶ���ǿ
sharp_img = sharpness.enhance(2.0)
sharp_img.save("newVerifyCode.png")
newVerify = Image.open('newVerifyCode.png')
# ʹ��image_to_stringʶ����֤��
text=image_to_string(newVerify).strip() #ʹ��image_to_stringʶ����֤��
#text1 = image_to_string('newVerifyCode.png').strip()
print (text)