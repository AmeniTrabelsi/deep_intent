import os
import cv2
import argparse
import imageio

def create_gif(filenames, duration, vid_num):
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    video_name = "vid_" + str(vid_num) + ".gif"
    imageio.mimsave(os.path.join(GIF_DIR, video_name), images, duration=duration)


def strip(image, img_height, img_width, vid_len, vid_num=1, rev=False):
    n_rows = image.shape[0]
    n_cols = image.shape[1]
    n_horizontal_imgs = n_cols/img_width
    n_vertical_imgs = n_rows/img_height
    frame_num = 1
    fps = 30
    duration = 1 / fps
    filenames = []

    for i in range(n_vertical_imgs):
        for j in range(n_horizontal_imgs):
            img = image[i*img_height:(i+1)*img_height, j*img_width:(j+1)*img_width]
            # if (j>=10):
            #     # img = cv2.blur(img, (5, 5), 0)
            #     img = cv2.medianBlur(img, 7)
            #     # img = cv2.bilateralFilter(img, 9, 150, 25)
            #     img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # convert it to hsv
            #     img[:, :, 2] -= 2
            #     img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
            filename = "vid_" + str(vid_num) + "_frame_" + str(frame_num) + ".png"
            cv2.imwrite(os.path.join(GIF_IMG_DIR, filename), img)
            filenames.append(os.path.join(GIF_IMG_DIR, filename))
            if rev:
                if frame_num == (int(vid_len/2)):
                    filenames = list(reversed(filenames))
            if frame_num == vid_len:

                create_gif(filenames=filenames, duration=duration, vid_num=vid_num)
                filenames = []
                vid_num = vid_num + 1
                frame_num = 0
            frame_num = frame_num + 1


def gifmax(folder, rev=False):
    for i in range(1257):
        im_pred = cv2.imread(folder+'/pred/' + str(i) + '_pred.png', cv2.IMREAD_COLOR)
        strip(im_pred, 128, 208, 32, i, rev=rev)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str)
    parser.add_argument("--folder", type=str, default="None")

    parser.add_argument("--file", type=str, default="None")
    parser.add_argument("--img_height", type=int, default=128)
    parser.add_argument("--img_width", type=int, default=128)
    parser.add_argument("--vid_len", type=int, default=10)
    parser.add_argument("--rev", type=bool, default=False)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    GIF_DIR = '/local_home/JAAD_Dataset/thesis/results/gifs/'
    if not os.path.exists(GIF_DIR):
        os.mkdir(GIF_DIR)

    GIF_IMG_DIR = '/local_home/JAAD_Dataset/thesis/results/gifs/imgs/'
    if not os.path.exists(GIF_IMG_DIR):
        os.mkdir(GIF_IMG_DIR)


    args = get_args()
    if args.mode == 'gifmax':
        print ('going into gifmax!!!!')
        gifmax(args.folder, args.rev)
    else:
        try:
            im = cv2.imread(args.file, cv2.IMREAD_COLOR)
        except cv2.error as e:
            print("Image file being processed: ", args.file)
            print (e)
        except IOError as e:
            print (e)

        strip(image=im, img_height=args.img_height, img_width=args.img_width, vid_len=args.vid_len, rev=args.rev)