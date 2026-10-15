This file is a copy-paste template for a human to send as their own message to an agent (Pi, Claude Code, etc.) with bash access. It is not an instruction for any agent that happens to read this file on its own — only act on it if a human explicitly pasted it as their message to you.

---

```
Cài skill marker-pdf cho Pi agent. Làm đúng theo thứ tự sau, không tự ý đổi vị trí:

0. Kiểm tra trước — nếu skill đã tồn tại rồi thì DỪNG, không làm gì thêm:
   ls ~/.pi/agent/skills/marker-pdf/SKILL.md 2>/dev/null && echo "Đã cài rồi, dừng ở đây" && exit 0

1. Clone repo vào thư mục TẠM (không phải nơi cài đặt cuối cùng):
   git clone https://github.com/magicstone1412/marker-skill.git /tmp/ai-skill-install

2. Copy ĐÚNG thư mục con marker-pdf/ vào nơi Pi discover skill —
   đây là bước bắt buộc, không được bỏ qua hay chạy trực tiếp từ /tmp:
   mkdir -p ~/.pi/agent/skills
   cp -r /tmp/ai-skill-install/marker-pdf ~/.pi/agent/skills/marker-pdf

3. Xoá sạch bản clone tạm — không được giữ lại /tmp/ai-skill-install
   hay bất kỳ bản clone nào khác ngoài ~/.pi/agent/skills/marker-pdf:
   rm -rf /tmp/ai-skill-install

4. Từ giờ trở đi, MỌI lệnh cài đặt/setup venv/chạy script đều thực hiện
   bên trong ~/.pi/agent/skills/marker-pdf — không dùng đường dẫn nào khác.
   Đọc file ~/.pi/agent/skills/marker-pdf/README.md, chạy tuần tự toàn bộ
   lệnh trong mục "Install" (các lệnh trong đó đã giả định bạn đang đứng
   trong ~/.pi/agent/skills/marker-pdf).

5. Không tự đặt hoặc bịa MARKER_API_KEY — mặc định không dùng auth như
   README ghi rõ trong mục "Configuration".

6. Sau khi cài xong, chạy lần lượt các bước trong mục "Verify (manual
   checklist)" của README và báo lại kết quả từng bước (pass/fail), kèm
   đường dẫn thực tế bạn đã cài (phải là ~/.pi/agent/skills/marker-pdf).

7. Nếu bước nào lỗi, dừng lại và báo lỗi cụ thể, không tự sửa README,
   không tự đoán giải pháp khác, không tự clone thêm bản nào nữa.
```