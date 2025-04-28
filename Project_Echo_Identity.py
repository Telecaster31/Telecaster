from speechbrain.inference.speaker import SpeakerRecognition

file1 = "C:/Users/DeokHwangbo/Downloads/Project_echo/Case_제이와이제이/김종찬 기준2(분리).wav"
file2 = "C:/Users/DeokHwangbo/Downloads/Project_echo/Case_제이와이제이/디스커넥트 직원 김경민(분리).wav"

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