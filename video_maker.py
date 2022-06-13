import cv2
import glob
from moviepy.editor import *
from datetime import datetime

from image_downloader import ImageDownloader
from image_resizer import ImageResizer

from moviepy.video.tools.subtitles import SubtitlesClip


class Image:
    def __init__(self, filename, time=300, size=1920):
        self.size = size
        self.time = time
        self.shifted = 0.0
        self.img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
        self.height, self.width, _ = self.img.shape
        self.converted_width = int(self.width * .85)
        self.height = 1080
        self.shift = self.width - self.converted_width
        self.img = cv2.resize(self.img, (self.converted_width, self.height))
        self.shift_height = False
        self.delta_shift = self.shift / self.time

    def get_frame(self):
        if self.shift_height:
            roi = self.img[int(self.shifted):int(self.shifted) + self.size, :, :]
        else:
            roi = self.img[:, int(self.shifted):int(self.shifted) + self.size, :]
        self.shifted += self.delta_shift
        if self.shifted > self.shift:
            self.shifted = self.shift
        if self.shifted < 0:
            self.shifted = 0
        return roi

def generate_video():
    path = os.getcwd() + "/resized_images/"
    filenames = glob.glob(os.path.join(path, "*"))
    images = []
    for filename in filenames:

        img = Image(filename=filename)
        images.append(img)

    image_frame = []
    for index in range(1, len(images)):
        if index == 1:
            for k in range(50):
                image_frame.append(images[index - 1].get_frame())
            for i in range(100):
                alpha = i / 100
                beta = 1.0 - alpha
                dst = cv2.addWeighted(images[index].get_frame(), alpha, images[index - 1].get_frame(), beta, 0.0)
                image_frame.append(dst)

        else:
            for i in range(100):
                alpha = i / 100
                beta = 1.0 - alpha
                dst = cv2.addWeighted(images[index].get_frame(), alpha, images[index - 1].get_frame(), beta, 0.0)
                image_frame.append(dst)
            for j in range(0, 50):
                image_frame.append(images[index].get_frame())

    directory = os.getcwd()
    pathOut = directory + '/video.mp4'
    fps = 30
    size = (1920, 1080)
    out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
    for i in range(len(image_frame)):
        out.write(image_frame[i])
    out.release()

def add_music_and_subtitle():

    video_clip = VideoFileClip("video.mp4")
    audio_clip = AudioFileClip("background_music.mp3").subclip(20, 185)

    generator = lambda txt: TextClip(txt, font='Arial', fontsize=50, color='white')
    subtitles = SubtitlesClip("sample.srt", generator)

    result = CompositeVideoClip([video_clip, subtitles.set_position(('center', 'bottom'))])

    final = result.set_audio(audio_clip)
    final.write_videofile("property_video_demo.mp4")

    os.remove("video.mp4")


if __name__ == "__main__":

    start_time = datetime.now().replace(microsecond=0)

    image_downloader = ImageDownloader()
    image_downloader.download_image()

    image_resizer = ImageResizer()
    image_resizer.resize_image()

    print("#######################################\n")
    print("          Generating Video          ")
    print("#######################################\n")

    generate_video()
    add_music_and_subtitle()

    end_time = datetime.now().replace(microsecond=0)
    execution_time = (end_time - start_time)
    print(f"End Time: {str(end_time)}")
    print(f"Total Execution Time: {str(execution_time)}")

