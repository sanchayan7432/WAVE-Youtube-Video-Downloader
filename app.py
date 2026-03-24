import streamlit as st
import yt_dlp
import os
import tempfile
import base64

st.set_page_config(
    page_title="WAVE",
    page_icon="🎬",
    layout="centered"
)

# ---------------- Video Background ----------------
def get_base64_video(video_file):
    with open(video_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

video_path = r"bg.mp4"
video_base64 = get_base64_video(video_path)

st.markdown(f"""
<style>

#bgvideo {{
    position: fixed;
    right: 0;
    bottom: 0;
    min-width: 100%;
    min-height: 100%;
    z-index: -1;
}}

.stApp {{
    background: transparent;
}}

h1, h2, h3, h4 {{
    color: #8ef5c4;
}}

[data-testid="metric-container"] {{
    background-color: rgba(0,0,0,0.55);
    border: 1px solid #1e5b42;
    padding: 15px;
    border-radius: 10px;
}}

div[data-testid="stMetricLabel"] {{
    color: #8ef5c4;
}}

div[data-testid="stMetricValue"] {{
    color: #a8ffd6;
}}

</style>

<video autoplay muted loop id="bgvideo">
<source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
</video>
""", unsafe_allow_html=True)

# ---------------- Cinematic Title ----------------
st.markdown("""
<style>

.cinematic-title {
    font-size:60px;
    font-weight:800;
    text-align:center;
    letter-spacing:4px;
    background:linear-gradient(90deg,#8ef5c4,#00ffcc,#8ef5c4);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    animation: gradientFlow 8s ease infinite, neonPulse 4s ease-in-out infinite;
}

.subtitle {
    text-align:center;
    font-size:18px;
    color:#a8ffd6;
    margin-top:-10px;
    margin-bottom:30px;
    opacity:0;
    animation:fadeIn 4s forwards;
}

@keyframes glow {
    from {text-shadow:0 0 10px #00ffcc,0 0 20px #00ffcc;}
    to {text-shadow:0 0 25px #00ffaa,0 0 40px #00ffaa;}
}

@keyframes fadeIn {
    to {opacity:1;}
}

</style>

<div class="cinematic-title">🎬 WAVE - YouTube Video Downloader</div>
<div class="subtitle">"Your Gateway to Instant YouTube Downloads"</div>

""", unsafe_allow_html=True)


# ---------------- DASHBOARD UI ---------------- #
with st.container():
    st.markdown('<div class="ui-container">', unsafe_allow_html=True)

    # st.title("🎬 YouTube Video Downloader")
    # st.write("Download videos or audio directly from YouTube.")

    url = st.text_input("Paste YouTube URL")

    # ---------------- VIDEO INFO ---------------- #
    def get_video_info(url):
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return info

    # ---------------- DOWNLOAD ---------------- #
    def download_video(url, format_type):
        temp_dir = tempfile.mkdtemp()
        progress_bar = st.progress(0)
        progress_text = st.empty()

        def progress_hook(d):
            if d['status'] == 'downloading':
                if 'total_bytes' in d and d['total_bytes']:
                    percent = d['downloaded_bytes'] / d['total_bytes']
                    progress_bar.progress(percent)
                    progress_text.markdown(
                        f'<div class="progress-text">Downloading: {int(percent*100)}%</div>', unsafe_allow_html=True
                    )
            elif d['status'] == 'finished':
                progress_bar.progress(1.0)
                progress_text.markdown(
                    '<div class="progress-text">Download complete. Processing...</div>', unsafe_allow_html=True
                )

        if format_type == "video":
            ydl_opts = {
                'format': 'best',
                'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
                'progress_hooks': [progress_hook]
            }
        else:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
                'progress_hooks': [progress_hook],
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3'
                }]
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
            filename = ydl.prepare_filename(info)

        return filename

    # ---------------- UI ---------------- #
    if url:
        try:
            info = get_video_info(url)
            st.image(info['thumbnail'])
            st.subheader(info['title'])

            col1, col2 = st.columns(2)
            col1.write(f"👁 Views: {info['view_count']}")
            col2.write(f"⏱ Duration: {info['duration']} sec")

            st.write(f"📺 Channel: {info['uploader']}")

            option = st.radio(
                "Select format",
                ["Video (MP4)", "Audio (MP3)"]
            )

            if st.button("⬇ Download"):
                with st.spinner("Downloading..."):
                    if option == "Video (MP4)":
                        file = download_video(url, "video")
                    else:
                        file = download_video(url, "audio")

                with open(file, "rb") as f:
                    st.download_button(
                        label="📥 Click to Save File",
                        data=f,
                        file_name=os.path.basename(file)
                    )
                st.success("Download ready!")

        except Exception as e:
            st.error("Invalid YouTube link or download failed.")

    st.markdown('</div>', unsafe_allow_html=True)
