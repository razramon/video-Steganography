import sys
import os
import videoSteganography
import cv2


def main():
    vid_file_path = sys.argv[1]
    is_cypher = False
    if len(sys.argv) > 2:
        text_file_path = sys.argv[2]
        is_cypher = True

    cap = cv2.VideoCapture(vid_file_path)

    if is_cypher:
        videoSteganography.encode_video(cap, os.path.basename(vid_file_path), text_file_path)
    else:
        videoSteganography.decode_video(cap,  os.path.splitext(os.path.basename(vid_file_path))[0])


if __name__ == '__main__':
    main()
