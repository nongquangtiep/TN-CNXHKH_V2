# ⚡ HỆ THỐNG ÔN THI TRẮC NGHIỆM CHỦ NGHĨA XÃ HỘI KHOA HỌC (QUIZIZZ STYLE)

Trang web ôn luyện trắc nghiệm môn **Chủ Nghĩa Xã Hội Khoa Học** phong cách Quizizz - Bấm chọn là biết ngay kết quả Đúng / Sai, đáp án chuẩn bôi đỏ tự động nhận diện từ tài liệu gốc.

Hỗ trợ giao diện Responsive chuyên nghiệp trên cả **Điện thoại di động (Mobile App UI)** và **Máy tính (Desktop)**.

---

## 🌟 ĐẶC ĐIỂM NỔI BẬT

- **Toàn bộ 263 câu hỏi chuẩn xác** trích xuất từ tài liệu học tập cập nhật:
  - `CHỦ NGHĨA XH-KH (1).docx`, `CNKHXH BAI6.docx`, `GỘP CHỦ NGHĨA XÃ HỘI KHOA HỌC - BÀI 1 2 3 4 5 6.docx`
  - Phân loại theo 6 bài học chính + tab riêng ôn luyện **Kiểm Tra TX (12 câu)**.
- **Đầy đủ 4 dạng bài tập chuẩn**:
  1. Trắc nghiệm 1 đáp án đúng (*Single Choice*) - 177 câu (đã khắc phục triệt để lỗi chọn 1 đáp án bị nhận nhầm thành chọn 4 đáp án)
  2. Trắc nghiệm nhiều đáp án đúng (*Multiple Choice*) - 36 câu
  3. Đúng / Sai theo mệnh đề (*True / False*) - 18 câu
  4. Kéo thả & Ghép cột, phân loại 2 cột (*Drag & Drop / Match*) - 21 câu (16 câu ghép vế + 5 câu phân loại 2 cột)
- **Tối ưu hóa đặc biệt cho điện thoại di động**:
  - Thanh Header 2 tầng hiển thị đầy đủ công cụ và điểm số không bị tràn viền.
  - Thao tác 1 chạm cho câu hỏi ghép vế và phân loại (chạm đáp án là các ô trống tự phát sáng, chạm để gắn vào).
  - Thanh điều hướng đáy màn hình (*Sticky Bottom Navigation*) giúp ngón tay cái dễ dàng chuyển câu.
- **Tính năng phong phú**:
  - Chế độ Sáng / Tối (*Light / Dark Theme*)
  - Âm thanh vui nhộn (*Web Audio API*)
  - Pháo hoa chúc mừng (*Canvas Confetti*)
  - Chuỗi đúng liên tiếp (*🔥 Streak Counter*)
  - Bảng xếp hạng (*Leaderboard*) & Lịch sử làm bài (*History*)
  - Xem lại chi tiết các câu làm sai và ôn lại riêng câu sai

---

## 🚀 HƯỚNG DẪN SỬ DỤNG

### Cách 1: Chạy trực tiếp
Nhấp đúp chuột vào file `index.html` hoặc `run_app.bat` trên Windows để mở ngay trong trình duyệt mà không cần cài đặt.

### Cách 2: Chạy qua Live Server / Python
```bash
python -m http.server 5500
```
Truy cập: `http://localhost:5500`

---

## 📂 CẤU TRÚC DỰ ÁN

- `index.html`: Cấu trúc trang web và giao diện ứng dụng.
- `style.css`: Toàn bộ phong cách thiết kế Quizizz, giao diện di động responsive, dark/light theme.
- `script.js`: Logic câu hỏi, tính điểm, âm thanh, lịch sử, bảng xếp hạng, tương tác kéo thả.
- `questions.json` & `questions-data.js`: Bộ ngân hàng 263 câu hỏi phân chia theo 6 bài và đề kiểm tra thường xuyên.
- `parse_all_questions.py`: Script trích xuất và phân tích câu hỏi từ Word docx (`CHỦ NGHĨA XH-KH (1).docx`).
- `run_app.bat`: Phím tắt chạy nhanh trên Windows.
