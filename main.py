import sys
import os
import videoSteganography
import cv2


def main():
    text_file_path = None

    # assert (len(sys.argv) < 1, "not enough files")
    vid_file_path = "cypheredlongVid.avi"  # sys.argv[1]
    #vid_file_path = "videos\\longVid.avi"
    is_cypher = False
    if len(sys.argv) > 1:
        text_file_path = "textfiles\\longText.txt"  # sys.argv[2]
        #is_cypher = True

    cap = cv2.VideoCapture(vid_file_path)
    # Check if opened successfully
    # assert (not cap.isOpened(), "Error opening video file")

    if is_cypher:
        videoSteganography.cypher_video(cap, os.path.basename(vid_file_path), text_file_path)

    else:
        videoSteganography.decypher_video(cap,  os.path.splitext(os.path.basename(vid_file_path))[0])
        #print(decyphered_txt)
        #text_file_save(decyphered_txt, os.path.basename(vid_file_path))


def text_file_save(binary_text, file_name):

    chars = []
    for b in range(int(len(binary_text) / 8)+1):
        byte = binary_text[b * 8:(b + 1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    text = ''.join(chars)
    print(text)
    #text = decode_binary_string(binary_text)
    new_file.write(text)
    new_file.close()
    return None




if __name__ == '__main__':
    main()
