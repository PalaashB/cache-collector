from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_DIR = r"d:/CSE/models/distilgpt2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForCausalLM.from_pretrained(MODEL_DIR)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

print("Chat with distilgpt2. Type 'exit' to quit.\n")

while True:
    user = input("You: ")
    if user.strip().lower() == "exit":
        break

    inputs = tokenizer(user, return_tensors="pt").to(device)

    output_ids = model.generate(
        **inputs,
        max_new_tokens=80,
        do_sample=True,
        temperature=0.8,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id,
    )

    full_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    # If the model echoed the prompt, cut it off, otherwise keep everything
    if full_text.startswith(user):
        reply = full_text[len(user):]
    else:
        reply = full_text

    reply = reply.strip()
    if not reply:
        reply = "[model only produced whitespace 🤷]"

    print(f"Bot: {reply}\n")
