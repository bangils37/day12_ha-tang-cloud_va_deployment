# Checklist Lab 12: Hạ Tầng Cloud và Deployment

## Những việc đã làm

- [x] Clone repository từ Github.
- [x] Tạo nhánh `feature/lab12` để làm việc.
- [x] Đẩy nhánh `feature/lab12` lên Github.
- [x] Đọc `CODE_LAB.md` để hiểu yêu cầu của lab.

### Phần lý thuyết và Code đọc hiểu (Part 1 - Part 5)
- [x] **Part 1: Localhost vs Production**: Đã đọc hiểu về 12-Factor App, khác biệt giữa basic và advanced `app.py`.
- [x] **Part 2: Docker Containerization**: Đã đọc hiểu cấu trúc `Dockerfile` (cơ bản và multi-stage) và `docker-compose.yml`.
- [x] **Part 4: API Security**: Đã xem các file implementation về API key auth, JWT, Rate Limiting và Cost Guard.
- [x] **Part 5: Scaling & Reliability**: Đã đọc về health checks, graceful shutdown, stateless design và load balancing.

### Phần thực hành code (Part 6: Final Project)
*(Đã hoàn thành)*
- [x] Khởi tạo project structure (`my-production-agent`).
- [x] Viết file config (`app/config.py`).
- [x] Viết logic auth, rate limit, cost guard với Redis (`app/auth.py`, `app/rate_limiter.py`, `app/cost_guard.py`).
- [x] Viết API chính (`app/main.py`).
- [x] Viết `Dockerfile` dạng multi-stage.
- [x] Viết `docker-compose.yml` để chạy stack với Redis và Nginx (Load Balancer).

## Những việc cần User cung cấp / thực hiện thủ công

### Part 3 & Part 6: Cloud Deployment
Để deploy dự án lên cloud platform (như Railway hoặc Render), bạn cần tự thực hiện các bước sau vì tôi (Agent) không có tài khoản và credentials của bạn:

- [ ] **Tạo tài khoản Cloud**: Đăng ký Railway (hoặc Render, Cloud Run).
- [ ] **Cài đặt CLI & Login (nếu dùng Railway)**: Chạy `npm i -g @railway/cli` và `railway login` trên máy của bạn.
- [ ] **Deploy**: Liên kết Github repo hoặc dùng CLI để deploy (`railway up`).
- [ ] **Thiết lập Environment Variables**: Bạn cần tự thiết lập các biến môi trường trên dashboard của nền tảng cloud (VD: `PORT`, `AGENT_API_KEY`, `REDIS_URL`, `OPENAI_API_KEY` nếu dùng LLM thật).
- [ ] **Kiểm tra Public URL**: Cung cấp Public URL sau khi deploy thành công để xác nhận.

---
*Ghi chú: Tôi sẽ tự động tiến hành code phần **Part 6: Final Project** trong các bước tiếp theo.*
