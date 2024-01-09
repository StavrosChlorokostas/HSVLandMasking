import cv2 as cv
import os

def is_fourcc_available(codec):
    try:
        fourcc = cv.VideoWriter_fourcc(*codec)
        temp_video = cv.VideoWriter('temp.mkv', fourcc, 30, (640, 480), isColor=True)
        temp_video.release()
        os.remove('temp.mkv')
        return True
    except:
        return False

def get_installed_fourcc_codecs():
    codecs_to_test = ["DIVX", "XVID", "MJPG", "X264", "WMV1", "WMV2", "FMP4",
                      "mp4v", "avc1", "I420", "IYUV", "mpg1", "H264"]
    available_codecs = []
    for codec in codecs_to_test:
        available_codecs.append((codec, is_fourcc_available(codec)))
    installed_codecs = [i for i,x in available_codecs if x]
    return installed_codecs

# if __name__ == "__main__":
#     codecs = get_installed_fourcc_codecs()
#     print(codecs)
