from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from cache_db import get_cached_response, save_to_cache

MODEL_DIR = r"C:/Users/admin/Desktop/UMass/summer_project/distilgpt2_local"   


tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForCausalLM.from_pretrained(MODEL_DIR)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

print("Chat here. Type 'exit' to quit.\n")

while True:
    user_question = input("You: ")

    if user_question.strip().lower() == "exit":
        break

    cached = get_cached_response(user_question)
    if cached:
        print(f"Bot (cached): {cached}\n")
        continue

    inputs = tokenizer(user_question, return_tensors="pt").to(device)

    output_ids = model.generate(
        **inputs,
        max_new_tokens=80,
        do_sample=True,
        temperature=0.8,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id,
    )

    full_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)


    if full_text.startswith(user_question):
        reply = full_text[len(user_question):]
    else:
        reply = full_text

    reply = reply.strip()

    if not reply:
        reply = "[model produced only whitespace]"

    print(f"Bot: {reply}\n")

    save_to_cache(user_question, reply)
