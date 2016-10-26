from PIL import Image, ImageQt,ImageFilter
from PyQt5.QtGui import QPixmap
import copy
import struct

class processor():


    def __init__(self):

        self.smilee=Image.open("/Users/jino/Desktop/image.jpg")

    def brightness(self,image,param): # 밝기
        image=Image.eval(image,lambda x:x+param)
        pixmap = QPixmap.fromImage(ImageQt.ImageQt(image))
        pixmap.detach()
        return (image, pixmap)

    def shade(self,image,param): # 명암

        image = Image.eval(image, lambda x: 128+param*(x-128))
        pixmap = QPixmap.fromImage(ImageQt.ImageQt(image))
        pixmap.detach()
        return (image, pixmap)

        pass

    def blackwhite(self,image): # 흑백
        image=image.convert("L")
        image=image.convert("RGB")
        pixmap=QPixmap.fromImage(ImageQt.ImageQt(image))
        pixmap.detach()
        return (image,pixmap)

    def combine(self,image): # 합성 TODO
        # combineDialog 클래스 참고
        pass


    def blur(self,image): # 흐리게 clear!
        m=1/6
        mat=ImageFilter.Kernel((3,3),(m,m,m,m,m,m,m,m,m))
        image=image.filter(mat)
        pixmap=QPixmap.fromImage((ImageQt.ImageQt(image)))
        pixmap.detach()
        return (image,pixmap)

    def vivid(self,image): # 선명하게 clear!
        mat = ImageFilter.Kernel((3, 3), (0,-1/2,0,-1/2,3,-1/2,0,-1/2,0))
        image = image.filter(mat)
        pixmap = QPixmap.fromImage((ImageQt.ImageQt(image)))
        pixmap.detach()
        return (image, pixmap)

        pass
    def rotate(self): # 회전
        pass
    def symmetry(self): # 대칭
        pass



    def smile(self,image,x,y,w,h): # TODO : 투명색은 어떻게 하나..

        img=copy.deepcopy(image)
        a=img.load()

        tempSmile=self.smilee.resize((w,h),Image.ANTIALIAS)
        tempLoad=tempSmile.load()
        for i in range(x,x+w):
            for j in range(y,y+h):
                if(tempLoad[i-x,j-y][3]!=0):
                    a[i,j]=tempLoad[i-x,j-y]

        pixmap = QPixmap.fromImage(ImageQt.ImageQt(img))
        pixmap.detach()
        del a
        return (img, pixmap)

    pass

    def painting(self,image,x,y,w,h,color):
        img = copy.deepcopy(image)
        a = img.load()

        b=color.name()[1:]
        h1, h2, h3 = '0x'+b[0:2], '0x' + b[2:4], '0x' + b[4:6]
        b=(int(h1, 16), int(h2, 16), int(h3, 16))

        for i in range(x, x + w):
            for j in range(y, y + h):
                a[i, j] = b

        pixmap = QPixmap.fromImage(ImageQt.ImageQt(img))
        pixmap.detach()
        del a
        return (img, pixmap)



