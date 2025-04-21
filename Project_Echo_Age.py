from pyAudioAnalysis import audioTrainTest as aT

file_path = "C:/Users/DeokHwangbo/Downloads/Project_echo/LEE_voice_separated_Ref.wav"

# 모델 경로
gender_model = r"C:\Users\DeokHwangbo\Downloads\Project_echo\pyAudioAnalysis-master\pyAudioAnalysis-master\pyAudioAnalysis\data\models\svm_rbf_speaker_male_female"
age_model = r"C:\Users\DeokHwangbo\Downloads\Project_echo\pyAudioAnalysis-master\pyAudioAnalysis-master\pyAudioAnalysis\data\models\svm_rbf_4class"

# 성별 예측
res_gender, prob_gender, gender_classes = aT.file_classification(file_path, gender_model, "svm")
print(f"성별 예측: {gender_classes[int(res_gender)]} (확률: {prob_gender})")

# 연령대 예측
res_age, prob_age, age_classes = aT.file_classification(file_path, age_model, "svm")
print(f"연령대 예측: {age_classes[int(res_age)]} (확률: {prob_age})")
