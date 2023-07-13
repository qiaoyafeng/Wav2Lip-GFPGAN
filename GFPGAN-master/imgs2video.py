import os


basePath = ".."

wav2lipFolderName = "Wav2Lip-master"
gfpganFolderName = "GFPGAN-master"
wav2lipPath = basePath + "/" + wav2lipFolderName
gfpganPath = basePath + "/" + gfpganFolderName

inputAudioPath = basePath + '/inputs/du-audio.m4a'
inputVideoPath = basePath + '/inputs/test-video.avi'
lipSyncedOutputPath = basePath + '/outputs/result.mp4'

outputPath = basePath + "/outputs"

restoredFramesPath = outputPath + '/restored_imgs/'
processedVideoOutputPath = outputPath

dir_list = os.listdir(restoredFramesPath)
dir_list.sort()

import cv2
import numpy as np

batch = 0
batchSize = 300
from tqdm import tqdm

for i in tqdm(range(0, len(dir_list), batchSize)):
    img_array = []
    start, end = i, i + batchSize
    print("processing ", start, end)
    for filename in tqdm(dir_list[start:end]):
        filename = restoredFramesPath + filename;
        img = cv2.imread(filename)
        if img is None:
            continue
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter(processedVideoOutputPath + '/batch_' + str(batch).zfill(4) + '.avi',
                          cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
    batch = batch + 1

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()


concatTextFilePath = outputPath + "/concat.txt"
concatTextFile=open(concatTextFilePath,"w")
for ips in range(batch):
  concatTextFile.write("file batch_" + str(ips).zfill(4) + ".avi\n")
concatTextFile.close()

concatedVideoOutputPath = outputPath + "/concated_output.avi"
print(f"concatedVideoOutputPath:{concatedVideoOutputPath}")
print(f"ffmpeg -y -f concat -i {concatTextFilePath} -c copy {concatedVideoOutputPath}")

finalProcessedOuputVideo = processedVideoOutputPath+'/final_with_audio.avi'
print(f"finalProcessedOuputVideo:{finalProcessedOuputVideo}")

print(f"ffmpeg -y -i {concatedVideoOutputPath} -i {inputAudioPath} -map 0 -map 1:a -c:v copy -shortest {finalProcessedOuputVideo}")

