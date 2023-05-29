from PIL import Image
import os
def get_size(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
    return size / 1024
def get_outfile(infile, outfile):
    if outfile:
        return outfile
    dir, suffix = os.path.splitext(infile)
    outfile = '{}-out{}'.format(dir, suffix)
    return outfile
def compress_image(infile, outfile='', mb=150, step=10, quality=80):
    o_size = get_size(infile)
    if o_size <= mb:
        return infile
    outfile = get_outfile(infile, outfile)
    while o_size > mb:
        im = Image.open(infile)
        im.save(outfile, quality=quality)
        if quality - step < 0:
            break
        quality -= step
        o_size = get_size(outfile)
    return outfile, get_size(outfile)
if __name__ == '__main__':
    compress_image(r'C:\Users\Administrator\Desktop\101x101.png')

    
#图片宽高大小    
from  PIL import Image
img=Image.open("a.png")
img.resize((192,192),Image.ANTIALIAS).save('b.png','png')



#gif图片宽高大小
from PIL import Image, ImageSequence
gifPath = '635x150.gif'
oriGif = Image.open(gifPath)
lifeTime = oriGif.info['duration']
imgList = []
imgNew = []
for i in ImageSequence.Iterator(oriGif):
    print(i.copy())
    imgList.append(i.copy())
for index, f in enumerate(imgList):
    f.save("%d.png" % index)
    img = Image.open("%d.png" % index)
    img.resize((640,150), Image.ANTIALIAS).save("%daa.png" % index,'png')
    img = Image.open("%daa.png" % index)
    imgNew.append(img)
imgNew[0].save("640x150.gif", 'gif', save_all=True, append_images=imgNew[1:], loop=0,

               duration=lifeTime)
