from moviepy.editor import *
def  main(in_file,out_file):
    clip = VideoFileClip(in_file, audio=False).subclip(5, 10).add_mask()
    image_clip = ImageClip('./a.png').set_start(0).set_duration(5)
    image_clip.set_position(("left", "top"))
    final = CompositeVideoClip([clip, image_clip])
    final.write_videofile(out_file)
main('a.mp4','b.mp4')
