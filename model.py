import torch
import streamlit as st

from data.Camera.information.base import valid_count_people

@st.cache(allow_output_mutation=True)
def load_model_yolov5():
    # Model
    model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # or yolov5n - yolov5x6, custom

    return model


model = load_model_yolov5()


def count_people_on_audit(imgs):

    # Работа с 2-мя изображениями
    imgs_valid = valid_count_people(imgs)

    datas = map(lambda img: model(img).pandas().xyxy[0], imgs_valid)
    left, middle_one, middle_two, right = [len(data[data.name == 'person']) for data in datas]

    return left + max(middle_one, middle_two) + right
