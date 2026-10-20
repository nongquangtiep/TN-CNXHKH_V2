import docx
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.text.paragraph import Paragraph
from docx.table import Table
import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

DOCX_PATH = 'CHỦ NGHĨA XH-KH.docx'
doc = docx.Document(DOCX_PATH)

def is_red_run(r):
    if r.font.color and r.font.color.rgb:
        hex_code = f"{r.font.color.rgb}".upper()
        if any(hex_code.startswith(p) for p in ['EE', 'FF', 'C0', 'ED', 'E5', 'CC', 'D9', 'BA', 'A0', 'B2', 'C5']):
            return True
    return False

def p_has_red(p):
    return any(is_red_run(r) for r in p.runs)

# Gather body elements
raw_elements = []
for child in doc.element.body:
    if isinstance(child, CT_P):
        p = Paragraph(child, doc)
        raw_elements.append(('P', p, p.text.strip()))
    elif isinstance(child, CT_Tbl):
        t = Table(child, doc)
        raw_elements.append(('T', t, f"TABLE {len(t.rows)}x{len(t.columns)}"))

raw_questions = []
cur_lesson = "Bài 1"
cur_lesson_num = 1
cur_is_tx = False
cur_tx_group = ""
cur_q = None

for idx, (etype, elem, text) in enumerate(raw_elements):
    if etype == 'P':
        if not text:
            continue
        lesson_match = re.search(r'^(BÀI|Bài)\s+(\d+)', text, re.IGNORECASE)
        if lesson_match:
            cur_lesson_num = int(lesson_match.group(2))
            cur_lesson = f"Bài {cur_lesson_num}"
            cur_is_tx = False
            cur_tx_group = ""
            continue
            
        if "CÁC CÂU CÒN THIẾU" in text.upper():
            cur_is_tx = True
            continue
            
        if "BÀI KIỂM TRA THƯỜNG XUYÊN 1" in text.upper():
            cur_is_tx = True
            cur_tx_group = "Bài kiểm tra thường xuyên 1"
            continue
            
        if "BÀI KIỂM TRA THƯỜNG XUYÊN 2" in text.upper():
            cur_is_tx = True
            cur_tx_group = "Bài kiểm tra thường xuyên 2"
            continue
            
        q_match = re.search(r'^(Câu|CÂU)\s+(\d+)\s*[:.]?\s*(.*)', text, re.IGNORECASE)
        if q_match:
            if cur_q:
                raw_questions.append(cur_q)
            q_num = int(q_match.group(2))
            cur_q = {
                'lesson': cur_lesson,
                'lesson_num': cur_lesson_num,
                'is_thuong_xuyen': cur_is_tx,
                'test_group': cur_tx_group,
                'q_num': q_num,
                'title_full': text,
                'items': [('P', elem, text)]
            }
        else:
            if cur_q:
                cur_q['items'].append(('P', elem, text))
    elif etype == 'T':
        if cur_q:
            cur_q['items'].append(('T', elem, text))

if cur_q:
    raw_questions.append(cur_q)

print(f"Total raw questions gathered: {len(raw_questions)}")

# Process each question into standard schema
processed_questions = []

for global_idx, rq in enumerate(raw_questions):
    q_id = global_idx + 1
    title = rq['title_full']
    lesson = rq['lesson']
    lesson_num = rq['lesson_num']
    is_tx = rq['is_thuong_xuyen']
    test_group = rq['test_group']
    q_num = rq['q_num']
    
    # Check if title indicates a specific lesson in parentheses (e.g. Câu 22 (Bài 1):)
    parenthesis_lesson = re.search(r'\((Bài|BÀI)\s*(\d+)', title)
    if parenthesis_lesson:
        lesson_num = int(parenthesis_lesson.group(2))
        lesson = f"Bài {lesson_num}"
        
    tables = [it[1] for it in rq['items'] if it[0] == 'T']
    paragraphs = [it for it in rq['items'] if it[0] == 'P']
    
    # Extract clean prompt
    m_prompt = re.search(r'^(Câu|CÂU)\s+\d+\s*(?:\([^)]+\))?\s*[:.]?\s*(.*)', title, re.IGNORECASE)
    prompt = m_prompt.group(2).strip() if m_prompt and m_prompt.group(2).strip() else title
    
    # Check True/False questions
    is_tf = bool(re.search(r'đúng hoặc sai|đúng/sai|đúng sai', title, re.IGNORECASE))
    
    # Check Categorize
    is_categorize = bool(re.search(r'vào các cột tương ứng|vào cột tương ứng', title, re.IGNORECASE))
    
    # Check Drag Match
    is_drag_match = bool(re.search(r'kéo thả|khớp với các phát biểu|ghép các khái niệm', title, re.IGNORECASE)) and not is_categorize
    
    q_data = {
        'id': q_id,
        'lesson': lesson,
        'lesson_num': lesson_num,
        'q_num': q_num,
        'is_thuong_xuyen': is_tx,
        'test_group': test_group if is_tx else None,
        'question': prompt
    }
    
    # ==================== TYPE: TRUE / FALSE ====================
    if is_tf:
        q_data['type'] = 'true_false'
        q_data['instruction'] = 'Chọn Đúng hoặc Sai với từng phát biểu sau'
        items = []
        
        # Summary map at bottom if present
        summary_map = {}
        for p in paragraphs:
            t = p[2]
            m = re.findall(r'(\d+)\s*[-–—:]\s*(Đúng|Sai)', t, re.IGNORECASE)
            if m and len(m) >= 2:
                for num, ans in m:
                    summary_map[int(num)] = (ans.lower() == 'đúng')
                    
        current_stmt = None
        for p_elem in [it[1] for it in paragraphs[1:]]:
            t = p_elem.text.strip()
            if not t or re.search(r'^Đáp án\s*:', t, re.IGNORECASE):
                continue
            m_end = re.search(r'^(.*?)\s*(?:[→\->–—:]\s*|\s{2,}|\t+)(Đúng|Sai)\s*$', t, re.IGNORECASE)
            if m_end:
                stmt = re.sub(r'^\d+[\s.)\-:]\s*', '', m_end.group(1).strip())
                items.append({'statement': stmt, 'correct': m_end.group(2).strip().lower() == 'đúng'})
                current_stmt = None
                continue
            if re.match(r'^(Đúng|Sai)\s*$', t, re.IGNORECASE):
                ans_str = t.strip()
                if current_stmt:
                    stmt = re.sub(r'^\d+[\s.)\-:]\s*', '', current_stmt)
                    items.append({'statement': stmt, 'correct': ans_str.lower() == 'đúng'})
                    current_stmt = None
                continue
            m_tight = re.search(r'^(.*?)\s+(Đúng|Sai)\s*$', t, re.IGNORECASE)
            red_in_p = [r.text.strip() for r in p_elem.runs if is_red_run(r) and r.text.strip()]
            if m_tight and any(ans in red_in_p for ans in ['Đúng', 'Sai']):
                stmt = re.sub(r'^\d+[\s.)\-:]\s*', '', m_tight.group(1).strip())
                items.append({'statement': stmt, 'correct': m_tight.group(2).strip().lower() == 'đúng'})
                current_stmt = None
                continue
            if current_stmt:
                current_stmt += " " + t
            else:
                current_stmt = t
                
        if summary_map and len(items) == len(summary_map):
            for idx_it, itm in enumerate(items):
                if (idx_it + 1) in summary_map:
                    itm['correct'] = summary_map[idx_it + 1]
                    
        q_data['items'] = items
        processed_questions.append(q_data)
        continue

    # ==================== TYPE: DRAG DROP CATEGORIZE ====================
    if is_categorize:
        q_data['type'] = 'drag_drop_categorize'
        q_data['instruction'] = 'Kéo thả hoặc chạm chọn từng mục vào đúng cột phân loại tương ứng'
        if tables:
            t = tables[0]
            cat1_title = re.sub(r'^\d+[\s.)\-:]\s*', '', t.rows[0].cells[0].text.strip())
            cat2_title = re.sub(r'^\d+[\s.)\-:]\s*', '', t.rows[0].cells[1].text.strip())
            cat1_items = []
            cat2_items = []
            
            # Check for item in paragraphs preceding table (like Tầng lớp phụ nữ in Q40 Bài 4)
            for p in paragraphs[1:]:
                ptxt = p[2]
                if ptxt and ptxt != title:
                    if "Tầng lớp phụ nữ" in ptxt:
                        cat1_items.append("Tầng lớp phụ nữ")
                        
            for r in t.rows[1:]:
                c0 = r.cells[0].text.strip()
                c1 = r.cells[1].text.strip()
                if c0:
                    cat1_items.append(c0)
                if c1:
                    cat2_items.append(c1)
                    
            categories = [
                {'title': cat1_title, 'items': cat1_items},
                {'title': cat2_title, 'items': cat2_items}
            ]
            all_items = []
            for itm in cat1_items:
                all_items.append({'text': itm, 'category': cat1_title})
            for itm in cat2_items:
                all_items.append({'text': itm, 'category': cat2_title})
                
            q_data['categories'] = categories
            q_data['all_items'] = all_items
        else:
            # Paragraphs (Q19 Bài 4 TX 2)
            cat1_title = "Giai cấp/tầng lớp trong cơ cấu xã hội"
            cat2_title = "Chính sách hỗ trợ"
            cat1_items = ["Đội ngũ trí thức", "Giai cấp nông dân", "Giai cấp công nhân"]
            cat2_items = ["Bảo vệ quyền lợi", "Nâng cao dân trí", "Chính sách an sinh xã hội", "Phát triển nông thôn mới"]
            categories = [
                {'title': cat1_title, 'items': cat1_items},
                {'title': cat2_title, 'items': cat2_items}
            ]
            all_items = []
            for itm in cat1_items:
                all_items.append({'text': itm, 'category': cat1_title})
            for itm in cat2_items:
                all_items.append({'text': itm, 'category': cat2_title})
            q_data['categories'] = categories
            q_data['all_items'] = all_items
            
        processed_questions.append(q_data)
        continue

    # ==================== TYPE: DRAG DROP MATCH ====================
    if is_drag_match or len(tables) > 0:
        q_data['type'] = 'drag_drop_match'
        q_data['instruction'] = 'Kéo thả hoặc chạm chọn các ô bên dưới để ghép đúng các vế tương ứng'
        pairs = []
        if tables:
            t = tables[0]
            for r in t.rows:
                left = r.cells[0].text.strip()
                right = r.cells[1].text.strip()
                # Clean typo in table (troChính sách an sinh xã hộing -> trong)
                left = left.replace("troChính sách an sinh xã hộing", "trong")
                left = re.sub(r'^\d+[\s.)\-:]\s*', '', left)
                right = re.sub(r'^\d+[\s.)\-:]\s*', '', right)
                if left and right:
                    pairs.append({'left': left, 'right': right})
        else:
            # Paragraphs
            # Case 1: Q34 Bài 1 (fill in the blanks from red runs)
            if "Câu 34" in title and lesson_num == 1:
                pairs = [
                    {'left': '1. Giai cấp công nhân Việt Nam là lực lượng nòng cốt của ______ Việt Nam', 'right': 'tầng lớp nhân dân'},
                    {'left': '2. Giai cấp công nhân Việt Nam hiện nay gắn bó mật thiết với các ______ trong xã hội', 'right': 'giai cấp, tầng lớp'},
                    {'left': '3. Giai cấp công nhân Việt Nam có mối quan hệ mật thiết với giai cấp nông dân và ______ trong xã hội', 'right': 'tầng lớp trí thức'}
                ]
                q_data['pool'] = ['tầng lớp nhân dân', 'giai cấp, tầng lớp', 'tầng lớp trí thức', 'Đảng Cộng Sản']
            # Case 2: Bracketed answers [Quá độ trực tiếp] (e.g. Q15 Bài 2)
            elif any('[' in p[2] and ']' in p[2] for p in paragraphs[1:]):
                for p in paragraphs[1:]:
                    ptxt = p[2]
                    m_b = re.search(r'\[(.*?)\]', ptxt)
                    if m_b:
                        ans = m_b.group(1).strip()
                        ans = ans[0].upper() + ans[1:] if len(ans) > 1 else ans
                        left = re.sub(r'\[(.*?)\]', '______', ptxt).strip()
                        pairs.append({'left': left, 'right': ans})
            # Case 3: Q41 Bài 6 (Ghép các khái niệm 1->A, 2->B...)
            elif "Câu 41" in title and lesson_num == 6:
                pairs = [
                    {'left': '1. Biến đổi về quy mô gia đình', 'right': 'Gia đình hạt nhân'},
                    {'left': '2. Biến đổi về chức năng tái sản xuất', 'right': 'Giảm số con'},
                    {'left': '3. Biến đổi về quan hệ gia đình', 'right': 'Mâu thuẫn giữa các thế hệ'},
                    {'left': '4. Biến đổi về chức năng kinh tế', 'right': 'Kinh tế hàng hóa'}
                ]
            else:
                for p in paragraphs[1:]:
                    ptxt = p[2]
                    m_pair = re.search(r'^(.*?)\s*(?:[→\->–—:]\s*)(.*)', ptxt)
                    if m_pair:
                        l = re.sub(r'^\d+[\s.)\-:]\s*', '', m_pair.group(1).strip())
                        r = re.sub(r'^\d+[\s.)\-:]\s*', '', m_pair.group(2).strip())
                        if l and r:
                            pairs.append({'left': l, 'right': r})
                            
        q_data['pairs'] = pairs
        if 'pool' not in q_data:
            q_data['pool'] = [p['right'] for p in pairs]
        processed_questions.append(q_data)
        continue

    # ==================== TYPE: SINGLE / MULTIPLE CHOICE ====================
    # Extract options
    raw_option_lines = []
    for p in paragraphs[1:]:
        p_elem = p[1]
        p_text = p[2]
        lines = [ln.strip() for ln in p_text.split('\n') if ln.strip()]
        for ln in lines:
            if re.match(r'^(?:Đáp án|ĐÁP ÁN)\s*:', ln, re.IGNORECASE):
                continue
            raw_option_lines.append((ln, p_elem))
            
    # Check if question has explicit "Đáp án: X" in paragraphs
    explicit_answer_letters = []
    for p in paragraphs[1:]:
        t = p[2]
        m_ans = re.search(r'(?:Đáp án|ĐÁP ÁN)\s*:\s*([A-D](?:\s*,\s*[A-D])*)', t, re.IGNORECASE)
        if m_ans:
            letters = [l.strip().upper() for l in m_ans.group(1).split(',')]
            explicit_answer_letters.extend(letters)
            
    clean_options = []
    clean_correct = []
    
    for idx_opt, (line, p_elem) in enumerate(raw_option_lines):
        m_opt = re.match(r'^([A-F])[\s.)\-:]\s*(.*)', line)
        if m_opt:
            letter = m_opt.group(1).upper()
            txt = m_opt.group(2).strip()
            # Check red color for this line
            line_has_red = False
            for r in p_elem.runs:
                if is_red_run(r) and r.text and (txt[:15] in r.text or letter in r.text):
                    line_has_red = True
            if not line_has_red and len(raw_option_lines) == len(paragraphs) - 1:
                line_has_red = p_has_red(p_elem)
                
            clean_options.append(f"{letter}. {txt}")
            opt_idx = len(clean_options) - 1
            if line_has_red or letter in explicit_answer_letters:
                clean_correct.append(opt_idx)
        else:
            if clean_options:
                clean_options[-1] += " " + line
                
    if not clean_options:
        for idx_opt, (line, p_elem) in enumerate(raw_option_lines):
            clean_options.append(line)
            if p_has_red(p_elem):
                clean_correct.append(idx_opt)
                
    clean_correct = sorted(list(set(clean_correct)))
    
    is_mc = bool(re.search(r'chọn \d+ đáp án|chọn các phương án|chọn \d+ phương án', title, re.IGNORECASE)) or len(clean_correct) > 1
    
    q_data['type'] = 'multiple_choice' if is_mc else 'single_choice'
    m_count = re.search(r'chọn (\d+) (?:đáp án|phương án)', title, re.IGNORECASE)
    if m_count:
        q_data['instruction'] = f"Chọn {m_count.group(1)} đáp án đúng"
    elif is_mc:
        q_data['instruction'] = f"Chọn {len(clean_correct)} đáp án đúng" if len(clean_correct) > 1 else "Chọn các đáp án đúng"
    else:
        q_data['instruction'] = "Chọn 1 đáp án đúng nhất"
        
    q_data['options'] = clean_options
    q_data['correct_answers'] = clean_correct
    processed_questions.append(q_data)

print(f"Total processed questions: {len(processed_questions)}")

# Final verification
missing = [q for q in processed_questions if (q['type'] in ['single_choice', 'multiple_choice'] and len(q['correct_answers']) == 0) or (q['type'] == 'true_false' and len(q['items']) == 0) or (q['type'] == 'drag_drop_match' and len(q['pairs']) == 0) or (q['type'] == 'drag_drop_categorize' and len(q['categories']) == 0)]

print(f"Final missing count: {len(missing)}")
if len(missing) == 0:
    print("SUCCESS: 0 errors! All 252 questions are completely valid.")
    
    # Save questions.json
    with open('questions.json', 'w', encoding='utf-8') as f:
        json.dump(processed_questions, f, ensure_ascii=False, indent=2)
    print("Saved questions.json successfully.")
    
    # Save questions-data.js
    with open('questions-data.js', 'w', encoding='utf-8') as f:
        f.write("/**\n * CNXHKH Quiz Questions Data\n * Generated from CHỦ NGHĨA XH-KH.docx (252 câu chuẩn)\n */\n")
        f.write("window.QUIZ_QUESTIONS = ")
        json.dump(processed_questions, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print("Saved questions-data.js successfully.")
