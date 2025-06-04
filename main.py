import streamlit as st
import cv2
import os
import tempfile

def extract_frames(video_path, output_folder):
    cap = cv2.VideoCapture(video_path)
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_filename = os.path.join(output_folder, f"frame_{count:03d}.jpg")
        cv2.imwrite(frame_filename, frame)
        count += 1
    cap.release()
    return count

st.title("🎥 تقسيم الفيديو إلى فريمات")

video_file = st.file_uploader("ارفع فيديو بصيغة MP4 أو AVI", type=["mp4", "avi", "mov"])

if video_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
        tmp_file.write(video_file.read())
        temp_video_path = tmp_file.name

    output_dir = tempfile.mkdtemp()
    st.info("جاري استخراج الفريمات، يرجى الانتظار...")
    frame_count = extract_frames(temp_video_path, output_dir)
    st.success(f"تم استخراج {frame_count} فريم ✅")

    # عرض أول 5 فريمات
    st.subheader("📸 أول 5 فريمات:")
    for i in range(min(5, frame_count)):
        frame_path = os.path.join(output_dir, f"frame_{i:03d}.jpg")
        st.image(frame_path, caption=f"Frame {i}", use_column_width=True)
