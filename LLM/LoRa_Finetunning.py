from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training, PeftModel
import torch
import os

# [0] 경로 설정
BASE_MODEL_PATH = "D:/gemma-3-4b-it"
DATASET_PATH = "D:/gemma3_format_dataset.jsonl"
OUTPUT_DIR = "./gemma-lora-output"
MERGED_DIR = "./merged-gemma3-4b"

# [1] Load tokenizer & model
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_PATH)
tokenizer.pad_token = tokenizer.eos_token

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL_PATH,
    torch_dtype=torch.float16,
    device_map="auto",
    load_in_4bit=True  # QLoRA
)

# [2] Prepare for LoRA training
model = prepare_model_for_kbit_training(base_model)

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# [3] Load and tokenize dataset
dataset = load_dataset("json", data_files=DATASET_PATH)["train"]
dataset = dataset.train_test_split(test_size=0.1)
train_dataset = dataset["train"]
eval_dataset = dataset["test"]

def tokenize(example):
    return tokenizer(example["text"], truncation=True, max_length=1024)
train_dataset = train_dataset.map(tokenize, batched=True)
eval_dataset = eval_dataset.map(tokenize, batched=True)

# [4] TrainingArguments
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    logging_steps=10,
    num_train_epochs=3,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="loss",
    greater_is_better=False,
    learning_rate=2e-4,
    fp16=True,
    report_to="none"
)

data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)

# [5] Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=data_collator,
)

trainer.train()

# [6] 병합 및 저장
print("🧩 LoRA 모델 병합 중...")
merged_model = model.merge_and_unload()
os.makedirs(MERGED_DIR, exist_ok=True)
merged_model.save_pretrained(MERGED_DIR)
tokenizer.save_pretrained(MERGED_DIR)
print(f"✅ 병합 완료! → {MERGED_DIR}")

# [7] 병합된 모델로 실행 예시
print("\n🤖 병합된 모델 테스트 실행")
from transformers import pipeline

pipe = pipeline("text-generation", model=MERGED_DIR, tokenizer=tokenizer, torch_dtype=torch.float16, device_map="auto")

prompt = "<start_of_turn>user\n너의 목적은 뭐야?\n<end_of_turn>\n<start_of_turn>model\n"
result = pipe(prompt, max_new_tokens=128, do_sample=True, temperature=0.7, top_p=0.9)[0]["generated_text"]

print("\n🧠 응답:\n", result.split("<start_of_turn>model\n")[-1].strip())
