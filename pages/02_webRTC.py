import streamlit as st
import pandas as pd
from utils.auth import Login_authentication
from streamlit_webrtc import webrtc_streamer
import mediapipe as mp
import cv2
import av
import math

# セッション状態の初期化
if "login_auth" not in st.session_state:
    st.session_state["login_auth"] = False

thickness = 5
circle_radius = 5
min_detection_confidence = 0.3
min_tracking_confidence = 0.9
mp_drawing_styles = mp.solutions.drawing_styles


def callback(frame):
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    image = frame.to_ndarray(format="bgr24")
    with mp_hands.Hands(
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    ) as hands:
        image = cv2.flip(image, 1)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(
                    image,
                    hand,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style(),
                )
        return av.VideoFrame.from_ndarray(image, format="bgr24")


st.sidebar.header("ログイン画面")

with st.sidebar.form(key="login_form"):
    username = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")
    submitted = st.form_submit_button("Submit")

    if submitted:
        auth_result = Login_authentication(target_name=username, valid_pasword=password)
        if isinstance(auth_result, bool) and auth_result:
            st.success("ログイン成功")
            st.session_state["login_auth"] = True
        elif isinstance(auth_result, str):
            st.error(auth_result)
            st.session_state["login_auth"] = False

# check_session_state
# st.write(st.session_state)

if st.session_state["login_auth"] == True:
    st.write("secret page")
    webrtc_streamer(
        key="hand-pose",
        video_frame_callback=callback,
        async_processing=True,
        media_stream_constraints={"video": True, "audio": False},
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    )
else:
    st.info("ログインをしてください")
