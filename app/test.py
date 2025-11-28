import time
import chat 





i = 1
while True:
    prompt = f"Summarize season {i} of Game of Thrones"
    start = time.time()
    reply = chat.reply
    end = time.time()
    print(f"Prompt: {prompt} | Time: {end-start:.3f}s")
    i += 1
