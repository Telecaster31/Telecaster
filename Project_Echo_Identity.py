from speechbrain.inference.speaker import SpeakerRecognition

file1 = "C:/Users/DeokHwangbo/Downloads/Project_echo/LEE_voice_separated_Ref.wav"
file2 = "C:/Users/DeokHwangbo/Downloads/Project_echo/KangSY_Lee_separate.wav"

# Load the model
model = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="pretrained_models/spkrec-ecapa-voxceleb"
)

# Investigation
score, prediction = model.verify_files(file1, file2)

# Print
print("=" * 40)
print(f"🧠 화자 유사도 (cosine similarity): {score.item():.4f}")

# Print the score
if score.item() >= 0.45:
    print("✅ 동일한 화자일 가능성이 높음")
else:
    print("❌ 서로 다른 화자일 가능성이 높음")

print("=" * 40)