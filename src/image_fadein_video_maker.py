import os
import glob
import cv2
from datetime import datetime

import numpy as np
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.tools.subtitles import SubtitlesClip

from image_downloader import ImageDownloader
from image_resizer import ImageResizer

start_time = datetime.now().replace(microsecond=0)


def generate_video():
    image_downloader = ImageDownloader()
    image_downloader.download_image()

    image_resizer = ImageResizer()
    image_resizer.resize_image()

    directory = os.getcwd()
    pathOut = directory + '/video.mp4'
    fps = 30
    size = (1920, 1080)
    out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    path = os.getcwd() + "/resized_images/"
    filenames = glob.glob(os.path.join(path, "*"))

    blank_image = np.zeros((1080, 1920, 3), np.uint8)
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

    title_image = cv2.imread(os.getcwd() + "/" + "title.jpg")
    for i in range(60):
        out.write(title_image)

    for index in range(len(filenames)):
        img = cv2.imread(filenames[index])
        param = 199
        for i in range(60):
            if i <= 24:
                out.write(cv2.GaussianBlur(img, (param, param), 0))
                param -= 8
            else:
                out.write(img)

    out.release()


generate_video()


def add_music_and_subtitle():
    video_clip = VideoFileClip("video.mp4")
    audio_clip = AudioFileClip("background_music.mp3").subclip(20, 79)

    generator = lambda txt: TextClip(txt, font='Arial', fontsize=70, color='white')
    subtitles = SubtitlesClip("sample_1.srt", generator)

    result = CompositeVideoClip([video_clip, subtitles.set_position(('center', 'bottom'))])

    final = result.set_audio(audio_clip)
    final.write_videofile("image_fadein_video.mp4")

    video_clip.close()
    audio_clip.close()
    subtitles.close()
    result.close()

    os.remove("video.mp4")


add_music_and_subtitle()

print("\n#######################################")
print("#######################################\n")
end_time = datetime.now().replace(microsecond=0)
execution_time = (end_time - start_time)
print(f"End Time: {str(end_time)}")
print(f"Total Execution Time: {str(execution_time)}")
