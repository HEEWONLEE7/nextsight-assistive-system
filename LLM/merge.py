from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

# 1. base 모델을 4bit 없이 다시 로드 (FP16)
base_model = AutoModelForCausalLM.from_pretrained(
    "D:/gemma-3-4b-it",
    torch_dtype=torch.float16,
    device_map="auto"
)

# 2. 가장 최신 LoRA checkpoint 불러오기
lora_model = PeftModel.from_pretrained(
    base_model,
    "D:/gemma_finetunnig/gemma-lora-output/checkpoint-336"
)

# 3. 병합
merged_model = lora_model.merge_and_unload()

# 4. 저장
save_path = "D:/gemma_finetunnig/merged-gemma3-4b"
merged_model.save_pretrained(save_path)

tokenizer = AutoTokenizer.from_pretrained("D:/gemma-3-4b-it")
tokenizer.save_pretrained(save_path)

print("✅ 병합 및 저장 완료!")
