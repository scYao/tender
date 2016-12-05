# coding=utf8

from PIL import Image,ImageDraw,ImageFont
import StringIO,sys,random
#code param is int 随机字符串
#imglen Verification code length 随机字符串长度
#path The current path 系统路径
#base The default string 字符串元组
#fongimg png格式的透明图片,上面弄好自定义的字符
#codeimg 需要生成字符的图片 大小为imglen长度乘以单个字符宽度
#按照fontimg上单个字符宽度随机截取字符,这里字符大小为(19,18)

path=sys.path[0]
imglen=4
base=('0','1','2','3','4','5','6','7','8','9',
      'A','B','C','D','E','F','G','H','I','J',
      'K','L','M','N','O','P','Q','R','S','T',
      'U','V','W','X','Y','Z')
def getcode():
    code=''

    fontimg=Image.open("/home/yz/Desktop/tender/test/font_t.png")
    codeimg=Image.new('RGBA',(19*imglen,25))
    #默认循环粘贴图片次数为imglen大小
    for x in range(imglen):
        ran=random.randint(0,35)
        #添加随机生成的code在base元组中的字符
        code=''.join((code,base[ran]))
        #img_s 随机截取图片，并在（-45,45）度之间随机旋转，在粘贴上codeimg
        img_s=fontimg.crop((ran*19,0,(ran+1)*19,20))
        img_s=img_s.rotate(random.randint(-30,30))
        codeimg.paste(img_s,(x*19,2))
    #保存于字符流，打印给浏览器
    out=StringIO.StringIO()
    codeimg.save(out, "PNG")
    return (code,out.getvalue())

if __name__ == '__main__':
    (code, value) = getcode()
    print code, value