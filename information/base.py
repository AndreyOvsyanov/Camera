import cv2

def valid_count_people(imgs):
    img_one, img_two = imgs

    img_one = cv2.resize(img_one, (640, 360))
    img_two = cv2.resize(img_two, (640, 360))

    # Разделение изображения на 2 area
    left = img_one[:, :img_one.shape[1] // 3 * 2]
    middle_one = img_one[:, img_one.shape[1] // 3 * 2:]
    middle_two = img_two[:, :img_two.shape[1] // 3 * 1]
    right = img_two[:, img_two.shape[1] // 3 * 1:]

    return left, middle_one, middle_two, right

    