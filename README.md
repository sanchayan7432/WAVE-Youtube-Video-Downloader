# 🌊 Wave – YouTube Video Downloader

## 📌 Description
**Wave** is a lightweight Python application that allows users to download YouTube videos quickly and easily. With a simple interface and minimal setup, Wave makes it effortless to save videos for offline viewing, archiving, or personal use.

---

## 🚀 Features
- Download YouTube videos in multiple resolutions  
- Save videos as MP4 files locally  
- Simple and clean Python implementation  
- Easy dependency management via `requirements.txt`  
- Customizable for integration into larger projects  

---

## 🛠️ Installation
1. Clone the repository:
```
git clone https://github.com/sanchayan7432/WAVE-Youtube-Video-Downloader.git
cd WAVE-Youtube-Video-Downloader
```
2. - Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```
3. Install dependencies:
```
pip install -r requirements.txt
```
---

## 📂 UsageRun the application with:python app.py
By default, the app will prompt for a YouTube video URL and download the video into the project directory.📑 Examplefrom pytube import YouTube
```
url = "https://www.youtube.com/watch?v=example"
yt = YouTube(url)
stream = yt.streams.get_highest_resolution()
stream.download(output_path="downloads")
print("Download complete!")
```
---
## ⚠️ Notes- This project is intended for personal use only.
- Respect YouTube’s Terms of Service — downloading videos may violate their policies if used improperly.
- Ensure you have sufficient storage space for large video files.
---
## 📜 LicenseThis project is licensed under the MIT License. See the LICENSE file for details.
This gives your repo a professional look with clear instructions, usage examples, and disclaimers.  
---
## Author
Sanchayan Ghosh. Email me at sanchayan.ghosh2022@uem.edu.in
