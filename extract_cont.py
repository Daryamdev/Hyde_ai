import json

with open("sorted_dialogue.json", 'r', encoding="utf-8") as f:
    data = json.load(f)

# Максимум 4500 строк до фильтрации (чтоб было с запасом)
data = data[:4500]

# Функция фильтрации
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

# Очищаем и сохраняем
core_quotes = [
    {"text": entry["content"].strip(), "role": entry["role"]}
    for entry in data if is_valid_text(entry)
]

with open("core_quotes.json", 'w', encoding='utf-8') as f:
    json.dump(core_quotes, f, ensure_ascii=False, indent=2)

print("✅ Готово! Сохранил чистый core_quotes.json.")
print(f"Всего строк после фильтра: {len(core_quotes)}")
