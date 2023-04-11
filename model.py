import torch
import streamlit as st


@st.cache(allow_output_mutation=True)
def load_model_yolov5():
    # Model
    model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # or yolov5n - yolov5x6, custom

    return model


model = load_model_yolov5()


def count_people_on_frame(imgs):
    datas = [model(img).pandas().xyxy[0] for img in imgs]

    return [len(data[data.name == 'person']) for data in datas]

# Results
