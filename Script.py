from PIL import ImageDraw, ImageFont, Image
import cv2
import numpy as np
import math
from moviepy.editor import VideoFileClip, ImageSequenceClip
import os

fileName = "sample.mp4"
outputFileName = "output.mp4"
outputFolder = "output"
frameRate = 25

chars = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
charlist = list(chars)
charlen = len(charlist)
interval = charlen / 256
scale_factor = 0.09  # anything above 0.15 is gonna make things worse
charwidth = 10
charheight = 10


def get_char(i):
    return charlist[math.floor(i * interval)]


cap = cv2.VideoCapture(fileName)
font_path = 'C:\\Windows\\Fonts\\lucon.ttf'
font_size = 15
font = ImageFont.truetype(font_path, font_size)

frames = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = Image.fromarray(frame)
    width, height = frame.size
    resized_width = int(scale_factor * width)
    resized_height = int(scale_factor * height * (charwidth / charheight))
    resized_frame = frame.resize((resized_width, resized_height), Image.NEAREST)

    pixel = resized_frame.convert("RGB")
    outputImage = Image.new("RGB", (charwidth * resized_width, charheight * resized_height), color=(0, 0, 0))
    dest = ImageDraw.Draw(outputImage)

    for i in range(resized_height):
        for j in range(resized_width):
            r, g, b = pixel.getpixel((j, i))
            intensity = int(0.299 * r + 0.587 * g + 0.114 * b)
            char = get_char(intensity)
            dest.text((j * charwidth, i * charheight), char, font=font, fill=(b, g, r))  # Swap R and B channels

    open_cv_image = np.array(outputImage)
    frames.append(open_cv_image)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# Create a video clip from the frames and set the audio
ascii_clip = ImageSequenceClip(frames, fps=frameRate)
ascii_clip = ascii_clip.set_audio(VideoFileClip(fileName).audio)

# Create the output folder if it doesn't exist
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

# Save the video clip as an MP4 file
outputPath = os.path.join(outputFolder, outputFileName)
ascii_clip.write_videofile(outputPath, codec="libx264")

# Open the folder where the video was saved
os.startfile(outputFolder)
