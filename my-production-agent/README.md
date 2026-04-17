# 🤖 Production AI Agent

---

## 🚀 Thông tin Deployment
- **Platform:** Railway
- **Project URL:** [https://my-production-agent-lab12-vinuni-production.up.railway.app](https://my-production-agent-lab12-vinuni-production.up.railway.app)
- **Status:** ✅ Deployed Successfully
- **API Key (Demo):** `secret-key-123`

## Hướng dẫn test cloud service
```bash
curl -H "X-API-Key: secret-key-123" \
      -X POST "https://my-production-agent-lab12-vinuni-production.up.railway.app/ask" \
      -H "Content-Type: application/json" \
      -d '{"question": "Hello AI"}'
```
- **Response:** JSON với kết quả trả lời AI.

---

## 📦 Cấu trúc dự án
```text
my-production-agent/
├── app/
│   ├── auth.py          # Xác thực API Key
│   ├── config.py        # Quản lý cấu hình (Pydantic)
│   ├── cost_guard.py    # Kiểm soát ngân sách
│   ├── main.py          # API chính & Logic
│   └── rate_limiter.py  # Giới hạn băng thông (Redis)
├── utils/
│   └── mock_llm.py      # Giả lập LLM
├── Dockerfile           # Multi-stage build
├── docker-compose.yml   # Chạy stack local (Agent + Redis)
└── requirements.txt     # Thư viện cần thiết
```

---

## 🛠 Hướng dẫn chạy Local
1. Clone repo và vào thư mục: `cd my-production-agent`
2. Chạy bằng Docker Compose:
   ```bash
   docker compose up --build
   ```
3. Test API:
   ```bash
   curl -H "X-API-Key: secret-key-123" \
        -X POST "http://localhost:8000/ask" \
        -H "Content-Type: application/json" \
        -d '{"question": "Hello AI"}'
   ```
