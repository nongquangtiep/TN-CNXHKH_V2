import json
import re
import sys
from test_parse_gop import all_parsed

sys.stdout.reconfigure(encoding='utf-8')

print(f"Loaded {len(all_parsed)} questions from GỘP file.")

# Assign sequential IDs 1..233
merged_questions = []
for idx, q in enumerate(all_parsed):
    q_copy = dict(q)
    q_copy['id'] = idx + 1
    merged_questions.append(q_copy)

# Load existing TX questions
with open('questions.json', 'r', encoding='utf-8') as f:
    old_qs = json.load(f)

tx_questions = [q for q in old_qs if q.get('is_thuong_xuyen')]
print(f"Loaded {len(tx_questions)} TX questions from previous bank.")

# Append TX questions with sequential IDs 234..
start_id = len(merged_questions) + 1
for idx, tq in enumerate(tx_questions):
    tq_copy = dict(tq)
    tq_copy['id'] = start_id + idx
    merged_questions.append(tq_copy)

total = len(merged_questions)
print(f"Total merged questions: {total}")

# Save questions.json
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(merged_questions, f, ensure_ascii=False, indent=2)
print("Saved questions.json successfully.")

# Save questions-data.js
with open('questions-data.js', 'w', encoding='utf-8') as f:
    f.write(f"// Dữ liệu câu hỏi trắc nghiệm Chủ Nghĩa Xã Hội Khoa Học ({total} câu chuẩn từ file GỘP)\n")
    f.write("window.QUIZ_QUESTIONS = ")
    json.dump(merged_questions, f, ensure_ascii=False, indent=2)
    f.write(";\n")
print("Saved questions-data.js successfully.")
