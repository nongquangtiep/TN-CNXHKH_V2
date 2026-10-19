import docx
import re
import json

doc = docx.Document('CNKHXH BAI6.docx')

parsed_qs = []
curr = None

for idx, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if not t: continue
    
    m = re.match(r'^Câu\s*(\d+)[:.]\s*(.*)', t, re.I)
    if m:
        if curr:
            parsed_qs.append(curr)
        curr = {
            'num': int(m.group(1)),
            'title': m.group(2).strip(),
            'lines': []
        }
    elif curr:
        curr['lines'].append(t)

if curr:
    parsed_qs.append(curr)

def parse_single_or_multi(q_dict):
    num = q_dict['num']
    title = q_dict['title']
    lines = q_dict['lines']
    
    # Check type
    if num == 41:
        # Match question
        pairs = [
            {"left": "Biến đổi về quy mô gia đình", "right": "Gia đình hạt nhân"},
            {"left": "Biến đổi về chức năng tái sản xuất", "right": "Giảm số con"},
            {"left": "Biến đổi về quan hệ gia đình", "right": "Mâu thuẫn giữa các thế hệ"},
            {"left": "Biến đổi về chức năng kinh tế", "right": "Kinh tế hàng hóa"}
        ]
        options_pool = ["Gia đình hạt nhân", "Giảm số con", "Mâu thuẫn giữa các thế hệ", "Kinh tế hàng hóa"]
        return {
            "lesson": "Bài 6",
            "lesson_num": 6,
            "type": "drag_drop_match",
            "question": f"Câu {num}: Ghép các khái niệm với các phát biểu về biến đổi gia đình Việt Nam trong thời kỳ quá độ lên chủ nghĩa xã hội:",
            "instruction": "Kéo hoặc chọn đáp án đúng ghép vào vế tương ứng",
            "pairs": pairs,
            "options_pool": options_pool
        }
    
    if num == 42:
        # True/False question
        # 1. Hiện nay, độ bền vững của gia đình không bị chi phối... -> Sai
        # 2. Hiện nay, kinh tế gia đình đang trở thành... -> Đúng
        # 3. Nội dung giáo dục trong gia đình hiện nay chỉ tập trung... -> Sai
        # 4. Giáo dục gia đình tiếp tục nhấn mạnh... -> Đúng
        items = [
            {"statement": "1. Hiện nay, độ bền vững của gia đình không bị chi phối bởi các mối quan hệ hòa hợp tình cảm giữa chồng và vợ, cha mẹ và con cái.", "correct": False},
            {"statement": "2. Hiện nay, kinh tế gia đình đang trở thành một bộ phận quan trọng trong nền kinh tế quốc dân.", "correct": True},
            {"statement": "3. Nội dung giáo dục trong gia đình hiện nay chỉ tập trung giáo dục đạo đức.", "correct": False},
            {"statement": "4. Giáo dục gia đình tiếp tục nhấn mạnh sự hy sinh của cá nhân cho cộng đồng.", "correct": True}
        ]
        return {
            "lesson": "Bài 6",
            "lesson_num": 6,
            "type": "true_false",
            "question": f"Câu {num}: Chọn đáp án Đúng hoặc Sai với từng phát biểu sau:",
            "instruction": "Chọn Đúng hoặc Sai cho mỗi phát biểu sau",
            "items": items
        }

    # Extract options and answers
    options = []
    ans_line = ""
    for l in lines:
        if l.startswith("Đáp án đúng:") or l.startswith("Đáp án:"):
            ans_line = l
        else:
            # Split by newline
            sub_lines = [p.strip() for p in l.split('\n') if p.strip()]
            for sl in sub_lines:
                if sl.startswith("Đáp án đúng:") or sl.startswith("Đáp án:"):
                    ans_line = sl
                elif re.match(r'^[A-D]\.', sl):
                    options.append(sl)
                elif options and not sl.startswith("Đáp án"):
                    # Check if next option or continuation
                    options.append(sl)

    # Clean options to ensure A. B. C. D.
    clean_opts = []
    for opt in options:
        opt_s = opt.strip()
        if opt_s:
            clean_opts.append(opt_s)

    # Determine correct answers
    ans_text = ans_line.replace("Đáp án đúng:", "").replace("Đáp án:", "").strip().upper()
    ans_letters = [a.strip() for a in re.findall(r'[A-D]', ans_text)]
    letter_to_idx = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    correct_indices = [letter_to_idx[l] for l in ans_letters if l in letter_to_idx]
    
    q_type = "multiple_choice" if len(correct_indices) > 1 else "single_choice"
    instr = f"Chọn {len(correct_indices)} đáp án đúng" if len(correct_indices) > 1 else "Chọn 1 đáp án đúng nhất"

    return {
        "lesson": "Bài 6",
        "lesson_num": 6,
        "type": q_type,
        "question": f"Câu {num}: {title}",
        "instruction": instr,
        "options": clean_opts,
        "correct_answers": correct_indices
    }

parsed_all_43 = []
for q in parsed_qs:
    obj = parse_single_or_multi(q)
    parsed_all_43.append(obj)

with open('parsed_bai6_43.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_all_43, f, ensure_ascii=False, indent=2)

print(f"Successfully converted all {len(parsed_all_43)} questions to JSON!")
