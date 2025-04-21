import whisper
import os

# FFmpeg 경로를 시스템 PATH에 강제로 추가
os.environ["PATH"] += os.pathsep + r"C:\Users\DeokHwangbo\Downloads\work\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin"

# Whisper 모델 로드 (정확도 향상용 medium 모델 사용)
model = whisper.load_model("medium")

# 📁 녹취 파일들이 들어있는 폴더 경로
input_folder = r"C:\Users\DeokHwangbo\Downloads\녹취\기록대상"
output_folder = r"C:\Users\DeokHwangbo\Downloads\녹취\녹취 저장(txt)"

# 📄 폴더 내 모든 .wav 파일 반복 처리
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".wav"):
        filepath = os.path.join(input_folder, filename)
        print(f"🎧 변환 중: {filename}...")

        # Whisper로 음성 파일 변환
        result = model.transcribe(filepath, language="ko", fp16=False)

        base_name = os.path.splitext(filename)[0]  # 확장자 제거한 파일명
        dialog_txt_path = os.path.join(output_folder, f"{base_name}_conversation.txt")

        # 타임스탬프 포함 대화형 저장만!
        with open(dialog_txt_path, "w", encoding="utf-8") as f:
            for segment in result["segments"]:
                start = segment["start"]
                end = segment["end"]
                text = segment["text"].strip()
                f.write(f"[{start:.1f} ~ {end:.1f}초] {text}\n")

        print(f"✅ 완료: {base_name}_대화형.txt 저장됨\n")

print("🎉 모든 파일 처리 완료 (대화형 형식만 저장됨)!")