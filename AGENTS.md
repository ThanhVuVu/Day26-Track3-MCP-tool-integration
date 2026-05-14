# Agent Instructions

Sử dụng `sqlite-lab` MCP server bất cứ khi nào nhiệm vụ yêu cầu:
1. Tra cứu thông tin sinh viên, khóa học hoặc đăng ký (`students`, `courses`, `enrollments`).
2. Chèn dữ liệu mới vào hệ thống.
3. Tính toán các thông số thống kê như điểm trung bình, tổng số lượng bản ghi.
4. Kiểm tra cấu trúc bảng dữ liệu qua tài nguyên `schema://`.

Lưu ý:
- Luôn kiểm tra schema trước khi thực hiện các truy vấn phức tạp.
- Sử dụng tool `search` với `filters` để tìm kiếm chính xác.
