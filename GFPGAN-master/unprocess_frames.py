import cv2
from tqdm import tqdm
from os import path

import os

basePath = ".."

wav2lipFolderName = "Wav2Lip-master"
gfpganFolderName = "GFPGAN-master"
wav2lipPath = basePath + "/" + wav2lipFolderName
gfpganPath = basePath + "/" + gfpganFolderName

outputPath = basePath + "/outputs"
inputAudioPath = basePath + "/inputs/kim_audio.mp3"
inputVideoPath = basePath + "/inputs/kimk_7s_raw.mp4"
lipSyncedOutputPath = basePath + "/outputs/result.mp4"

inputVideoPath = outputPath + "/result.mp4"
unProcessedFramesFolderPath = outputPath + "/frames"

print("inputVideoPath", inputVideoPath)

if not os.path.exists(unProcessedFramesFolderPath):
    print("makedirs:", unProcessedFramesFolderPath)
    os.makedirs(unProcessedFramesFolderPath)

print("unProcessedFramesFolderPath", unProcessedFramesFolderPath)

vidcap = cv2.VideoCapture(inputVideoPath)
print("vidcap", vidcap)

numberOfFrames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = vidcap.get(cv2.CAP_PROP_FPS)
print("FPS: ", fps, "Frames: ", numberOfFrames)

for frameNumber in tqdm(range(numberOfFrames)):
    _, image = vidcap.read()
    cv2.imwrite(
        path.join(unProcessedFramesFolderPath, str(frameNumber).zfill(4) + ".jpg"),
        image,
    )
