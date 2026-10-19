import json
import re

with open('questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

for q in questions:
    qid = q['id']
    
    # ID 76: Bài 2 Q36
    if qid == 76:
        for p in q.get('pairs', []):
            if '_____  xã' in p.get('left', ''):
                p['left'] = p['left'].replace('_____  xã hội', '_____ xã hội')
                
    # ID 85: Bài 3 Q3
    elif qid == 85:
        if 'options' in q:
            q['options'] = [o.replace('bằng  pháp quyền', 'bằng Nhà nước pháp quyền') for o in q['options']]

    # ID 89: Bài 3 Q7
    elif qid == 89:
        q['question'] = 'Câu 7: Kiểu nhà nước nào sau đây được V.I. Lênin gọi là nhà nước "nửa nhà nước"?'
        q['options'] = [
            'A. Nhà nước chủ nô',
            'B. Nhà nước phong kiến',
            'C. Nhà nước tư sản',
            'D. Nhà nước xã hội chủ nghĩa'
        ]

    # ID 98: Bài 3 Q16
    elif qid == 98:
        if 'options' in q:
            q['options'] = [
                o.replace('hình thức tổ chức  thừa nhận', 'hình thức tổ chức nhà nước thừa nhận')
                 .replace('hình thức tổ chức  của giai cấp', 'hình thức tổ chức nhà nước của giai cấp')
                for o in q['options']
            ]

    # ID 100: Bài 3 Q18
    elif qid == 100:
        q['question'] = q['question'].replace('của  pháp quyền', 'của Nhà nước pháp quyền')

    # ID 101: Bài 3 Q19
    elif qid == 101:
        q['question'] = q['question'].replace('mô hình  khác', 'mô hình nhà nước khác')
        q['question'] = q['question'].replace('thì  pháp quyền', 'thì nhà nước pháp quyền')

    # ID 102: Bài 3 Q20
    elif qid == 102:
        q['question'] = q['question'].replace('của  xã hội chủ nghĩa', 'của nhà nước xã hội chủ nghĩa')
        if 'options' in q:
            q['options'] = [o.replace('lật đổ  của giai cấp', 'lật đổ nhà nước của giai cấp') for o in q['options']]

    # ID 106: Bài 3 Q24
    elif qid == 106:
        if 'options' in q:
            q['options'] = [o + ' nhà nước' if o.strip().endswith('không phụ thuộc vào') else o for o in q['options']]

    # ID 107: Bài 3 Q25
    elif qid == 107:
        if 'options' in q:
            q['options'] = [o.replace('D.  chủ yếu thực hiện', 'D. Nhà nước chủ yếu thực hiện') for o in q['options']]

    # ID 110: Bài 3 Q28
    elif qid == 110:
        q['question'] = q['question'].replace('Câu 28: pháp quyền', 'Câu 28: Nhà nước pháp quyền')
        if 'options' in q:
            q['options'] = [
                o.replace('Quyền lực  là', 'Quyền lực nhà nước là')
                 .replace('Đảng lãnh đạo  theo', 'Đảng lãnh đạo nhà nước theo')
                 .replace('Quyền lực  thống nhất', 'Quyền lực nhà nước thống nhất')
                 .replace('D.  quản lý xã hội', 'D. Nhà nước quản lý xã hội')
                for o in q['options']
            ]

    # ID 111: Bài 3 Q29
    elif qid == 111:
        if len(q.get('options', [])) == 3:
            q['options'].append('D. Chức năng đối nội và chức năng đối ngoại')

    # ID 115: Bài 3 Q33
    elif qid == 115:
        if 'items' in q:
            for it in q['items']:
                s = it.get('statement', '')
                s = s.replace('cho  trực tiếp bầu ra', 'cho cơ quan do mình trực tiếp bầu ra')
                s = s.replace('làm chủ  và xã hội', 'làm chủ nhà nước và xã hội')
                it['statement'] = s

    # ID 116: Bài 3 Q34
    elif qid == 116:
        if 'items' in q:
            for it in q['items']:
                s = it.get('statement', '')
                s = s.replace('quyền lực  cao nhất', 'quyền lực nhà nước cao nhất')
                s = s.replace('hoạt động của  pháp quyền', 'hoạt động của nhà nước pháp quyền')
                s = s.replace('cơ quan của  không được', 'cơ quan của nhà nước không được')
                it['statement'] = s

    # ID 117: Bài 3 Q35
    elif qid == 117:
        if 'items' in q:
            for it in q['items']:
                s = it.get('statement', '')
                s = s.replace('hình thái , một chế độ', 'hình thái nhà nước, một chế độ')
                it['statement'] = s

    # ID 118: Bài 3 Q36
    elif qid == 118:
        if 'items' in q:
            for it in q['items']:
                s = it.get('statement', '')
                if s.strip().endswith('phát triển của'):
                    s = s.strip() + ' nhà nước'
                it['statement'] = s

    # ID 147: Bài 4 Q25
    elif qid == 147:
        if 'options' in q:
            q['options'] = [o.replace('doanh nghiệp  và nông dân', 'doanh nghiệp nhà nước và nông dân') for o in q['options']]

    # ID 160: Bài 4 Q38
    elif qid == 160:
        if 'items' in q:
            for it in q['items']:
                s = it.get('statement', '')
                s = s.replace('Xây dựng  pháp quyền', 'Xây dựng Nhà nước pháp quyền')
                it['statement'] = s

    # ID 161: Bài 4 Q39
    elif qid == 161:
        if 'items' in q:
            for it in q['items']:
                s = it.get('statement', '')
                s = re.sub(r'(\d+\.)\s{2,}', r'\1 ', s)
                s = s.replace('Đảng, , mặt trận', 'Đảng, Nhà nước, Mặt trận')
                s = s.replace('Đảng, , Mặt trận', 'Đảng, Nhà nước, Mặt trận')
                it['statement'] = s

    # ID 201: Bài 5 Q34
    elif qid == 201:
        if 'options' in q:
            q['options'] = [
                'A. Do sự áp bức giai cấp của giai cấp thống trị' if o.strip().startswith('A. Do giai cấp của') else o
                for o in q['options']
            ]

    # Formatting Cleanups
    if qid == 36 and 'items' in q:
        for it in q['items']:
            it['statement'] = re.sub(r'(\d+\.)\s{2,}', r'\1 ', it['statement'])
            
    if qid == 60 and 'options' in q:
        q['options'] = [re.sub(r'([A-D]\.)\s{2,}', r'\1 ', o) for o in q['options']]

    if qid == 143 and 'options' in q:
        q['options'] = [re.sub(r'([A-D]\.)\s{2,}', r'\1 ', o) for o in q['options']]

    if qid in [154, 155]:
        q['question'] = re.sub(r'\?\s{2,}\(', '? (', q['question'])

    if qid == 260 and 'options' in q:
        q['options'] = [re.sub(r'([A-D]\.)\s{2,}', r'\1 ', o) for o in q['options']]

# Save updated questions.json
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

# Save updated questions-data.js for browser
js_content = 'window.QUESTIONS_DATA = ' + json.dumps(questions, ensure_ascii=False, indent=2) + ';\n'
with open('questions-data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Successfully applied fixes to questions.json and questions-data.js")
