import json
import matplotlib.pyplot as plt
import os

# 체크포인트와 라벨
checkpoint_infos = [
    ("./gemma-lora-output/checkpoint-113", "Checkpoint 113"),
    ("./gemma-lora-output/checkpoint-226", "Checkpoint 226"),
    ("./gemma-lora-output/checkpoint-336", "Checkpoint 336"),
]

plt.figure(figsize=(10, 5))

# 개별 플롯
for path, label in checkpoint_infos:
    trainer_state_path = os.path.join(path, "trainer_state.json")
    if not os.path.exists(trainer_state_path):
        print(f"❌ 파일 없음: {trainer_state_path}")
        continue

    with open(trainer_state_path, "r", encoding="utf-8") as f:
        state = json.load(f)

    log_history = state.get("log_history", [])
    steps, train_losses, eval_steps, eval_losses = [], [], [], []
    
    for entry in log_history:
        if "loss" in entry:
            steps.append(entry["step"])
            train_losses.append(entry["loss"])
        if "eval_loss" in entry:
            eval_steps.append(entry["step"])
            eval_losses.append(entry["eval_loss"])

    # 학습 손실 플롯
    plt.plot(steps, train_losses, label=f"{label} - Train Loss", marker="o")
    # 검증 손실 플롯
    plt.plot(eval_steps, eval_losses, label=f"{label} - Eval Loss", marker="x")

# 그래프 꾸미기
plt.xlabel("Step")
plt.ylabel("Loss")
plt.title("Gemma LoRA Training Logs")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
