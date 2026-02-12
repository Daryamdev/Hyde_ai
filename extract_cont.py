import json

with open("sorted_dialogue.json", 'r', encoding="utf-8") as f:
    data = json.load(f)

data = data[:4500]


def is_valid_text(entry):
    text = entry["content"].strip().lower()
    return text and not (
        "uploaded image" in text or
        text.startswith("<<") or
        text.endswith(">>") or
        text.startswith("![") or
        text.startswith("http") or
        text.startswith("data:image") or
        len(text) < 3
    )


core_quotes = [
    {"text": entry["content"].strip(), "role": entry["role"]}
    for entry in data if is_valid_text(entry)
]

with open("core_quotes.json", 'w', encoding='utf-8') as f:
    json.dump(core_quotes, f, ensure_ascii=False, indent=2)

print("✅ Ready core_quotes.json.")
print(f"Your lines are: {len(core_quotes)}")
