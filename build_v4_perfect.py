import json
import re

with open('questions.json', 'r', encoding='utf-8') as f:
    old_questions = json.load(f)

# 1. Identify IDs to remove (duplicates)
# ID 36: duplicate of ID 33 in Bài 1
# ID 118: duplicate of ID 114 in Bài 3
# ID 234: duplicate of ID 32 in Bài 1
# ID 238: duplicate of ID 113 in Bài 3
# ID 239: duplicate of ID 151 in Bài 4
# ID 240: duplicate of ID 144 in Bài 4
# ID 242: duplicate of ID 166 in Bài 4
# ID 245: duplicate of ID 197 in Bài 5
remove_ids = {36, 118, 234, 238, 239, 240, 242, 245}

filtered = [q for q in old_questions if q['id'] not in remove_ids]

# 2. Fix text typos in existing questions
for q in filtered:
    # Fix ID 113: missing "nhà nước"
    if q['id'] == 113 or "dân chủ xã hội chủ nghĩa và  xã hội chủ nghĩa" in q.get('question', ''):
        q['question'] = q['question'].replace("dân chủ xã hội chủ nghĩa và  xã hội chủ nghĩa", "dân chủ xã hội chủ nghĩa và nhà nước xã hội chủ nghĩa")
        if 'options' in q:
            q['options'] = [o.replace("và hoạt động của  xã hội chủ nghĩa", "và hoạt động của nhà nước xã hội chủ nghĩa")
                             .replace("còn  xã hội chủ nghĩa", "còn nhà nước xã hội chủ nghĩa") for o in q['options']]
    
    # Fix ID 89 & 110: missing "nhà nước"
    if "quyền lực , chức năng của  được chia thành" in q.get('question', ''):
        q['question'] = q['question'].replace("quyền lực , chức năng của  được chia thành", "quyền lực nhà nước, chức năng của nhà nước được chia thành")

    # Fix ID 187: missing "Nhà nước"
    if "Câu 20. Vì sao Đảng,  Việt Nam chủ trương" in q.get('question', ''):
        q['question'] = q['question'].replace("Vì sao Đảng,  Việt Nam", "Vì sao Đảng, Nhà nước Việt Nam")

    # Fix pairs in ID 121 (Bài 3): missing "nhà nước"
    if 'pairs' in q:
        for p in q['pairs']:
            if 'left' in p:
                p['left'] = p['left'].replace("của  pháp quyền", "của nhà nước pháp quyền")
                p['left'] = p['left'].replace("trong  pháp quyền", "trong nhà nước pháp quyền")
                p['left'] = p['left'].replace("quyền làm chủ  và xã hội", "quyền làm chủ nhà nước và xã hội")

# 3. Define the 15 new high-quality questions from CNKHXH BAI6.docx
new_15 = [
    # --- BÀI 5: Dân tộc & Tôn giáo (9 câu) ---
    {
        "lesson": "Bài 5",
        "lesson_num": 5,
        "type": "single_choice",
        "question": "Theo quan điểm duy vật lịch sử, tôn giáo là sản phẩm của yếu tố nào?",
        "instruction": "Chọn 1 đáp án đúng nhất",
        "options": [
            "A. Con người",
            "B. Thượng đế",
            "C. Lực lượng siêu nhiên",
            "D. Tự nhiên huyền bí"
        ],
        "correct_answers": [0]
    },
    {
        "lesson": "Bài 5",
        "lesson_num": 5,
        "type": "single_choice",
        "question": "Nhóm yếu tố nào sau đây phản ánh đầy đủ nguồn gốc hình thành và tồn tại của tôn giáo?",
        "instruction": "Chọn 1 đáp án đúng nhất",
        "options": [
            "A. Hệ thống tín đồ, tổ chức giáo phẩm và nghi lễ",
            "B. Cơ sở thờ tự, kinh sách và giáo luật",
            "C. Nguồn gốc nhận thức, tâm lý và kinh tế - xã hội",
            "D. Sự can thiệp của các đấng sáng tạo siêu nhiên"
        ],
        "correct_answers": [2]
    },
    {
        "lesson": "Bài 5",
        "lesson_num": 5,
        "type": "single_choice",
        "question": "Khái niệm dân tộc theo nghĩa hẹp được dùng để chỉ khái niệm nào?",
        "instruction": "Chọn 1 đáp án đúng nhất",
        "options": [
            "A. Dân tộc quốc gia",
            "B. Dân tộc tộc người",
            "C. Cộng đồng đa quốc gia",
            "D. Liên hiệp các quốc gia"
        ],
        "correct_answers": [1]
    },
    {
        "lesson": "Bài 5",
        "lesson_num": 5,
        "type": "single_choice",
        "question": "Tiêu chí nào mang tính thiêng liêng nhất đối với một dân tộc quốc gia và mỗi thành viên dân tộc?",
        "instruction": "Chọn 1 đáp án đúng nhất",
        "options": [
            "A. Lãnh thổ",
            "B. Thị trường nội địa",
            "C. Mức sống thu nhập",
            "D. Ý thức cá nhân"
        ],
        "correct_answers": [0]
    },
    {
        "lesson": "Bài 5",
        "lesson_num": 5,
        "type": "single_choice",
        "question": "Nhận định nào sau đây là SAI khi nói về quyền tự quyết dân tộc trong Cương lĩnh dân tộc Mác – Lênin?",
        "instruction": "Chọn 1 đáp án đúng nhất",
        "options": [
            "A. Quyền tự quyết bao gồm quyền tự do tách ra thành quốc gia độc lập",
            "B. Quyền tự quyết dân tộc không bao gồm nội dung tự nguyện liên hiệp các dân tộc lại",
            "C. Dân tộc tộc người có đặc trưng về ngôn ngữ riêng",
            "D. Cương lĩnh dân tộc khẳng định nguyên tắc bình đẳng giữa các dân tộc"
        ],
        "correct_answers": [1]
    },
    {
        "lesson": "Bài 5",
        "lesson_num": 5,
        "type": "single_choice",
        "question": "Hình thái ý thức xã hội phản ánh một cách hoang đường, hư ảo hiện thực khách quan là khái niệm của hiện tượng nào?",
        "instruction": "Chọn 1 đáp án đúng nhất",
        "options": [
            "A. Nghệ thuật dân gian",
            "B. Tôn giáo",
            "C. Đạo đức xã hội",
            "D. Triết học khoa học"
        ],
        "correct_answers": [1]
    },
    {
        "lesson": "Bài 5",
        "lesson_num": 5,
        "type": "single_choice",
        "question": "Phát biểu nào sau đây là SAI về sự khác biệt giữa tín ngưỡng và tôn giáo?",
        "instruction": "Chọn 1 đáp án đúng nhất",
        "options": [
            "A. Tín ngưỡng có hệ thống giáo lý, giáo luật và tổ chức chặt chẽ như tôn giáo",
            "B. Nguồn gốc kinh tế - xã hội dẫn đến sự ra đời của tôn giáo",
            "C. Mê tín dị đoan là niềm tin mù quáng gây hậu quả xấu cần loại bỏ",
            "D. Tôn giáo phản ánh hiện thực một cách hoang đường, hư ảo"
        ],
        "correct_answers": [0]
    },
    {
        "lesson": "Bài 5",
        "lesson_num": 5,
        "type": "single_choice",
        "question": "Đâu là các đặc trưng cơ bản thuộc về dân tộc tộc người?",
        "instruction": "Chọn 1 đáp án đúng nhất",
        "options": [
            "A. Lãnh thổ quốc gia, nền kinh tế chung, nhà nước chung",
            "B. Ngôn ngữ tộc người, văn hóa đặc thù và ý thức tự giác tộc người",
            "C. Quân đội riêng, hiến pháp riêng, tài chính độc lập",
            "D. Hệ thống chính trị riêng biệt và tiền tệ riêng"
        ],
        "correct_answers": [1]
    },
    {
        "lesson": "Bài 5",
        "lesson_num": 5,
        "type": "single_choice",
        "question": "Hai nguyên nhân chủ yếu khiến tôn giáo vẫn tiếp tục tồn tại lâu dài trong thời kỳ quá độ là gì?",
        "instruction": "Chọn 1 đáp án đúng nhất",
        "options": [
            "A. Do quy định bắt buộc của nhà nước và do các giáo hội nước ngoài thúc đẩy",
            "B. Do khoa học chưa giải thích hết mọi hiện tượng và xã hội vẫn còn phân hóa, áp bức",
            "C. Do các thế lực siêu nhiên thực sự tồn tại can thiệp vào đời sống",
            "D. Do sự phát triển của công nghệ truyền thông"
        ],
        "correct_answers": [1]
    },

    # --- BÀI 3: Dân chủ XHCN & Nhà nước XHCN (4 câu) ---
    {
        "lesson": "Bài 3",
        "lesson_num": 3,
        "type": "single_choice",
        "question": "Việc thực hiện chế độ công hữu về tư liệu sản xuất chủ yếu và phân phối lợi ích theo kết quả lao động là bản chất kinh tế của nền dân chủ nào?",
        "instruction": "Chọn 1 đáp án đúng nhất",
        "options": [
            "A. Nền dân chủ tư sản",
            "B. Nền dân chủ chủ nô",
            "C. Nền dân chủ xã hội chủ nghĩa",
            "D. Nền dân chủ nguyên thủy"
        ],
        "correct_answers": [2]
    },
    {
        "lesson": "Bài 3",
        "lesson_num": 3,
        "type": "single_choice",
        "question": "Khác biệt căn bản về chất của Nhà nước pháp quyền xã hội chủ nghĩa ở Việt Nam so với các nhà nước bóc lột trong lịch sử là gì?",
        "instruction": "Chọn 1 đáp án đúng nhất",
        "options": [
            "A. Chỉ đại diện duy nhất cho bộ phận giai cấp công nhân",
            "B. Là nhà nước phi giai cấp, phi chính trị",
            "C. Mang bản chất của giai cấp công nhân, tính nhân dân sâu sắc và tính dân tộc rộng rãi",
            "D. Chỉ tập trung thực hiện chức năng trấn áp quân sự"
        ],
        "correct_answers": [2]
    },
    {
        "lesson": "Bài 3",
        "lesson_num": 3,
        "type": "single_choice",
        "question": "Hình thức dân chủ nào là hình thức mà nhân dân trực tiếp bày tỏ ý chí, trực tiếp tham gia quản lý nhà nước và xã hội?",
        "instruction": "Chọn 1 đáp án đúng nhất",
        "options": [
            "A. Dân chủ gián tiếp",
            "B. Dân chủ đại diện",
            "C. Dân chủ trực tiếp",
            "D. Dân chủ ủy quyền"
        ],
        "correct_answers": [2]
    },
    {
        "lesson": "Bài 3",
        "lesson_num": 3,
        "type": "single_choice",
        "question": "Khẳng định nào sau đây về tổ chức quyền lực nhà nước ở Việt Nam là SAI?",
        "instruction": "Chọn 1 đáp án đúng nhất",
        "options": [
            "A. Bản chất dân chủ XHCN được thực hiện qua hình thức trực tiếp và gián tiếp",
            "B. Quốc hội là cơ quan quyền lực nhà nước cao nhất hoạt động theo nhiệm kỳ 3 năm",
            "C. Nhà nước Việt Nam là nhà nước của nhân dân, do nhân dân, vì nhân dân làm chủ",
            "D. Trong hoạt động nhà nước có sự phân công, phối hợp và kiểm soát giữa các cơ quan quyền lực"
        ],
        "correct_answers": [1]
    },

    # --- BÀI 4: Cơ cấu xã hội - giai cấp & Liên minh (2 câu) ---
    {
        "lesson": "Bài 4",
        "lesson_num": 4,
        "type": "single_choice",
        "question": "Trong cơ cấu xã hội – giai cấp ở Việt Nam thời kỳ quá độ, đội ngũ trí thức giữ vai trò là lực lượng gì?",
        "instruction": "Chọn 1 đáp án đúng nhất",
        "options": [
            "A. Lực lượng sáng tạo đặc biệt",
            "B. Lực lượng lãnh đạo sự nghiệp cách mạng",
            "C. Lực lượng sản xuất nông nghiệp nòng cốt",
            "D. Đội ngũ quản lý doanh nghiệp độc lập"
        ],
        "correct_answers": [0]
    },
    {
        "lesson": "Bài 4",
        "lesson_num": 4,
        "type": "single_choice",
        "question": "Phát biểu nào sau đây về khối liên minh giai cấp, tầng lớp ở Việt Nam là ĐÚNG?",
        "instruction": "Chọn 1 đáp án đúng nhất",
        "options": [
            "A. Nội dung tôn giáo là nội dung nòng cốt của liên minh",
            "B. Xây dựng Nhà nước pháp quyền là nội dung văn hóa của liên minh",
            "C. Đồng thuận xã hội là một mục tiêu quan trọng của liên minh giai cấp, tầng lớp",
            "D. Đội ngũ doanh nhân bị loại trừ, không tham gia khối liên minh"
        ],
        "correct_answers": [2]
    }
]

# 4. Group by lesson and organize
# Lessons 1 to 6
lessons_data = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
tx_list = []

for q in filtered:
    ln = q.get('lesson_num', 1)
    if ln in lessons_data:
        lessons_data[ln].append(q)

# Add the 15 new questions into their lessons
for q in new_15:
    ln = q['lesson_num']
    lessons_data[ln].append(q)

# Re-number and build final ordered list
final_questions = []
current_id = 1

for ln in range(1, 7):
    qs_in_lesson = lessons_data[ln]
    for idx, q in enumerate(qs_in_lesson):
        q_num = idx + 1
        q['id'] = current_id
        q['lesson_num'] = ln
        q['lesson'] = f"Bài {ln}"
        q['q_num'] = q_num
        
        # Standardize question title prefix
        title_body = re.sub(r'^(Câu\s*\d+[\.\:\–\-\s]*|Câu\s*[\:\–\-\s]*)', '', q['question'], flags=re.I).strip()
        q['question'] = f"Câu {q_num}: {title_body}"
        
        final_questions.append(q)
        current_id += 1

print(f"Total standard questions across Bài 1 - Bài 6: {len(final_questions)}")
breakdown = {f"Bài {i}": len(lessons_data[i]) for i in range(1, 7)}
print("Breakdown:", breakdown)

# Save questions.json
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(final_questions, f, ensure_ascii=False, indent=2)

# Save questions-data.js
js_content = f"// Du lieu cau hoi trac nghiem Chu Nghia Xa Hoi Khoa Hoc (V4 - {len(final_questions)} cau chuan, khong trung lap)\nwindow.QUIZ_QUESTIONS = " + json.dumps(final_questions, ensure_ascii=False, indent=2) + ";\n"
with open('questions-data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Saved questions.json and questions-data.js successfully!")
