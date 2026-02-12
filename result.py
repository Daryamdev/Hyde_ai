result = []
with open('alltext.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

current_role = None
current_content = []

for line in lines:
    line = line.strip()

    if line.startswith("You said:"):
        if current_role and current_content:
            result.append({"role": current_role, "content": "\n".join(current_content).strip()})
        current_role = "user"
        current_content = []
    elif line.startswith("ChatGPT said:"):
        if current_role and current_content:
            result.append({"role": current_role, "content": "\n".join(current_content).strip()})
        current_role = "assistant"
        current_content = []
    elif "Uploaded image" in line or "Uploaded file" in line:
        if current_role and current_content:
            result.append({"role": current_role, "content": "\n".join(current_content).strip()})
            current_role = None
            current_content = []
        result.append({"role": "event", "content": line})
    else:
        current_content.append(line)

# Добавляем последнюю реплику
if current_role and current_content:
    result.append({"role": current_role, "content": "\n".join(current_content).strip()})

# Сохраняем в JSON
import json
with open('sorted_dialogue.json', 'w', encoding='utf-8') as out_file:
    json.dump(result, out_file, ensure_ascii=False, indent=2)
