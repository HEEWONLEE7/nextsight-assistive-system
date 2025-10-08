from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# ✅ 모델 경로 (파인튜닝 + 병합된 LoRA 모델)
MODEL_PATH = r"D:\gemma-3-4b-it"

# ✅ 디바이스 설정
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# ✅ 토크나이저 및 모델 로드
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
tokenizer.pad_token = tokenizer.eos_token  # 필수 설정

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float32  # 안정성 위해 float32 사용
).to(device)

# ✅ 종료 토큰 ID (반복 방지용으로 <end_of_turn> 사용)
eos_token_id = tokenizer.convert_tokens_to_ids("<end_of_turn>")

# ✅ 테스트 프롬프트 (Gemma 스타일)
prompt = "<start_of_turn>user\n안녕?\n<end_of_turn>\n<start_of_turn>model\n"

# ✅ 토크나이즈 및 디바이스 이동
inputs = tokenizer(prompt, return_tensors="pt").to(device)

# ✅ 입력 토큰 디버깅 (필요 시 출력)
print("입력 토큰:", inputs.input_ids)

# ✅ 추론 (반복 차단 및 종료 토큰 설정 포함)
outputs = model.generate(
    **inputs,
    max_new_tokens=256,
    do_sample=True,
    temperature=0.8,          # 약간 줄여서 자연스러움 유지
    top_p=0.9,                # 조금 더 집중된 출력
    top_k=50,
    repetition_penalty=1.2,   # 반복 억제 강도 증가
    eos_token_id=eos_token_id
)

# ✅ 디코딩 (특수 토큰 포함하여 <end_of_turn> 탐지 가능하게)
decoded = tokenizer.decode(outputs[0], skip_special_tokens=False)

# ✅ 응답 추출 (<start_of_turn>model 이후, <end_of_turn> 이전까지만)
response = decoded.split("<start_of_turn>model\n")[-1].strip()
response = response.split("<end_of_turn>")[0].strip()

# ✅ 출력
print("모델 응답:\n", response)
