from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.tools import tool

from login import login
import time
from getscore import get_scores
from getstudent_id import get_student_id

load_dotenv()

username = input("Username: ")
password = input("Password: ")


access_token = None
token = 0

def ensure_token(username, password):
    """Đảm bảo token truy cập hợp lệ."""
    global access_token, token
    if access_token is None or time.time() > token:
        access_token = login(username, password)
        token = time.time() + 1700 
    return access_token


@tool
def get_scores_tool():
    """Lấy điểm sinh viên từ hệ thống."""
    access_token = ensure_token(username, password)
    student_id = get_student_id(access_token)
    return get_scores(access_token, student_id)


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

agent = create_agent(llm, tools=[get_scores_tool], system_prompt= """Bạn là trợ lý tra cứu điểm.
QUY TẮC BẮT BUỘC:
- Khi người dùng hỏi điểm (môn nào, học kỳ nào, hoặc tổng), PHẢI dùng tool get_scores_tool để lấy dữ liệu.
- KHÔNG được bịa. Nếu không tìm thấy môn/ngữ cảnh thì nói không có dữ liệu.
- CHỈ được trả lời DUY NHẤT 1 DÒNG, không xuống dòng, không giải thích.

ĐỊNH DẠNG TRẢ LỜI (chọn đúng 1 trong các mẫu):
1) Nếu tìm thấy điểm môn:
   "Môn {TEN_MON} của bạn được {DIEM} điểm."
2) Nếu không tìm thấy môn người dùng hỏi:
   "Không tìm thấy điểm môn {TEN_MON} trong dữ liệu."
3) Nếu người dùng hỏi chung chung mà không nêu môn:
   "Bạn muốn xem điểm môn nào?""")

while True:
    q = input("\nBạn: ").strip()
    if q.lower() in {"exit", "quit"}:
        break

    result = agent.invoke({"messages": [{"role": "user", "content": q}]})

    msg = result["messages"][-1].content
    text = msg if isinstance(msg, str) else msg[0].get("text", "")
    print("Bot:", text)


