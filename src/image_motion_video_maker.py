import os

import cv2
import glob

import numpy as np
from datetime import datetime

from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.tools.subtitles import SubtitlesClip

from image_downloader import ImageDownloader
from image_resizer import ImageResizer


class Image:
    def __init__(self, filename, time=100, size=1920):
        self.size = size
        self.time = time
        self.shifted = 0.0
        self.img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
        self.height, self.width, _ = self.img.shape
        # self.converted_width = int(self.width * .85)
        # self.height = 1080
        self.shift = self.width - self.size
        # self.img = cv2.resize(self.img, (self.converted_width, self.height))
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

    directory = os.getcwd()
    pathOut = directory + '/video.mp4'
    fps = 30
    size = (1920, 1080)
    out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
    out.get(0)

    blank_image = np.zeros((1080, 2200, 3), np.uint8)
    property_name = "La Quinta Resort & Club, Curio Collection"
    state = "California"
    country = "USA"
    property_description = "This luxury resort features 41 pools, 53 hot tubs, 23 tennis courts, and spacious rooms " \
                           "with a flat-screen TV. It is 2 miles from downtown La Quinta and 20 miles from Palm " \
                           "Springs International Airport. Guests of La Quinta Resort & Club, Curio Collection have " \
                           "access to a variety of recreation facilities, including 5 championship golf courses, " \
                           "tennis courts and a state-of-the-art fitness center. Spa La Quinta offers massage and facials. " \
                           "Dining options at La Quinta Resort & Club, Curio Collection range from fine dining at " \
                           "Morgan’s in the Desert to authentic Mexican cuisine at the Adobe Grill. Ernie’s Sports " \
                           "Bar and Twenty6 also have full bar menus. Free Wi-Fi and a refrigerator are standard in " \
                           "every room at the La Quinta Resort & Club, Curio Collection. All rooms are decorated " \
                           "with 1920s-inspired décor and include air conditioning. Free parking is available at the " \
                           "resort, which is a 4-minute drive from the La Quinta Museum. Shopping is available on " \
                           "site or in Old Town La Quinta, 1.2 miles away."
    location = f"{state}, {country}"
    text = f"{property_name} \n{location}"

    # setup text
    font = cv2.FONT_HERSHEY_SIMPLEX
    # get boundary of this text
    text_size = cv2.getTextSize(text, font, 1, 0)[0]

    # get coords based on boundary
    textX = round((blank_image.shape[1] - text_size[0]) / 2)
    textY = round((blank_image.shape[0] + text_size[1]) / 2)

    x, y0 = textX, textY
    line_height = text_size[1] + 70

    for i, line in enumerate(text.split('\n')):
        y = y0 + i * line_height
        cv2.putText(blank_image, line, (x, y), font, 2, (255, 255, 255), 3, cv2.LINE_AA)
    cv2.imwrite(os.getcwd() + "/" + "title.jpg", blank_image)

    title_image = Image(os.getcwd() + "/" + "title.jpg")
    for i in range(70):
        out.write(title_image.get_frame())

    for index in range(0, len(images)):
        if index == 0:
            for k in range(0, 50):
                out.write(images[index].get_frame())

        else:
            for i in range(0, 30):
                alpha = i / 30
                beta = 1.0 - alpha
                dst = cv2.addWeighted(images[index].get_frame(), alpha, images[index - 1].get_frame(), beta, 0.0)
                out.write(dst)

            for j in range(0, 30):
                out.write(images[index].get_frame())

    out.release()


def add_music_and_subtitle():
    video_clip = VideoFileClip("video.mp4")
    audio_clip = AudioFileClip("background_music.mp3").subclip(20, 82)

    generator = lambda txt: TextClip(txt, font='Arial', fontsize=70, color='white')
    subtitles = SubtitlesClip("sample.srt", generator)

    result = CompositeVideoClip([video_clip, subtitles.set_position(('center', 'bottom'))])

    final = result.set_audio(audio_clip)
    final.write_videofile("image_motion_video.mp4")

    video_clip.close()
    audio_clip.close()
    subtitles.close()
    result.close()

    os.remove("video.mp4")


if __name__ == "__main__":
    start_time = datetime.now().replace(microsecond=0)

    image_downloader = ImageDownloader()
    image_downloader.download_image()

    image_resizer = ImageResizer()
    image_resizer.resize_image()

    print("\n#######################################")
    print("          Generating Video          ")
    print("#######################################\n")

    generate_video()
    add_music_and_subtitle()

    end_time = datetime.now().replace(microsecond=0)
    execution_time = (end_time - start_time)
    print(f"End Time: {str(end_time)}")
    print(f"Total Execution Time: {str(execution_time)}")
