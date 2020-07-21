import cv2
import random


def encode_video(vid_file, vid_name, filename):
    # We convert the resolutions from float to integer.
    frame_width = int(vid_file.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(vid_file.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(vid_file.get(cv2.CAP_PROP_FPS))

    # Define the codec and create VideoWriter object.
    # The output is stored in 'outpy.avi' file.
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    new_vid = cv2.VideoWriter('cyphered' + vid_name, fourcc,
                              fps, (frame_width, frame_height))
    letter_generator = reader(filename)
    # Read until video is completed
    i = 0
    first_frames = True
    while vid_file.isOpened():
        # Not including first 2 frames
        if first_frames:
            for j in range(2):
                ret, frame = vid_file.read()
                if ret:
                    new_vid.write(frame)
                else:
                    break
            first_frames = False
        if i % 2 == 0:
            ret, frame = vid_file.read()
        else:
            ret, temp = vid_file.read()
            if ret:
                try:
                    # Try to get the next letter from the file
                    letter = next(letter_generator)
                except StopIteration:
                    pass
                else:
                    # If success, encode the letter (1 byte) to the frame
                    encode_frame(frame, letter, frame_width, frame_height)
        if ret:
            # Write the frame into the file
            new_vid.write(frame)
        else:
            # Break the loop
            break
        i += 1

    # When everything done, release the video capture object
    vid_file.release()
    new_vid.release()

    # Closes all the frames
    cv2.destroyAllWindows()
    return None


def encode_frame(frame, byte_letter, width, height):
    offset_width = 0
    # Iterating over the byte -
    #   width/8      = bit length
    #   height*bit/2 = which side of the frame we will put noise
    for bit in byte_letter:
        for j in range(int(offset_width * width / 8), int((offset_width + 1) * width / 8)):
            for i in range(int(int(bit)*height/2), int((int(bit) + 1)*height/2)):
                # Only 0.005% of each section will be noised, so the frame will not be seen as damaged.
                if random.random() < 0.005:
                    color = frame[i, j]
                    red = random.randint(1, 5)
                    green = random.randint(1, 5)
                    blue = random.randint(1, 5)
                    frame[i, j] = (color[0]+red, color[1]+green, color[2]+blue)
        offset_width += 1
    return frame


def reader(filename):
    with open(filename,'rb') as f:
        while True:
            # read next character
            char = f.read(1)
            # if not EOF, then at least 1 character was read, and
            # this is not empty
            if char:
                print(char)
                char = ''.join(map(bin, bytearray(char, encoding='utf-8')))[2:]
                char = (-len(char) % 8) * '0' + char
                yield char
            else:
                break


def decode_video(vid_file, file_name):
    new_file = open(file_name + ".txt", 'w+')
    end_of_text = False
    first_frames = True
    width = int(vid_file.get(3) / 8)
    height = int(vid_file.get(4) / 2)

    while vid_file.isOpened():
        # Not including first 2 frames
        if first_frames:
            for j in range(2):
                ret, original_frame = vid_file.read()
                if not ret:
                    break
            first_frames = False

        # Capture frame-by-frame
        ret, original_frame = vid_file.read()
        if not ret:
            # Break the loop
            break
        ret, edit_frame = vid_file.read()
        word = ""
        if ret:
            # Each frame width is cyphered to a byte -> 1/8 is bit, and so we need to extract the bit.
            # If the noise was on the top half, it is 0, otherwise 1.
            for i in range(8):
                diff_top = cv2.subtract(original_frame[0:height, int(i*width): int((i+1)*width)], edit_frame[0: height, int(i*width): int((i+1)*width)])
                b_top, g_top, r_top = cv2.split(diff_top)
                diff_bot = cv2.subtract(original_frame[height: int(height*2), int(i*width): int((i+1)*width)], edit_frame[height: int(height*2), int(i*width): int((i+1)*width)])
                b_bot, g_bot, r_bot = cv2.split(diff_bot)
                b = cv2.countNonZero(b_top) - cv2.countNonZero(b_bot)
                g = cv2.countNonZero(g_top) - cv2.countNonZero(g_bot)
                r = cv2.countNonZero(r_top) - cv2.countNonZero(r_bot)
                if (b + g + r) > 0:
                    word = word + str(0)
                else:
                    word = word + str(1)
            # Haven't found a single byte, we stop iterate to save time.
            if word == "11111111":
                end_of_text = True
                break
            else:
                new_file.write(chr(int(word, 2)))

        else:
            break
        if end_of_text:
            break

    # When everything done, release the video capture object
    vid_file.release()

    # Closes all the frames
    cv2.destroyAllWindows()

    return None
