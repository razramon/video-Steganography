import sys
import os
import videoSteganography
import cv2


def main():
    vid_file_path = sys.argv[1]
    is_encode = False
    if len(sys.argv) > 2:
        text_file_path = sys.argv[2]
        is_encode = True

    cap = cv2.VideoCapture(vid_file_path)

    if is_encode:
        videoSteganography.encode_video(cap, os.path.basename(vid_file_path), text_file_path)
        print("finished encodeing.\nnew edited video in repository.\nexiting...\n")

    else:
        videoSteganography.decode_video(cap,  os.path.splitext(os.path.basename(vid_file_path))[0])
        print("finished decodeing..\nnew text file in repository.\nexiting...")


if __name__ == '__main__':
    main()
