from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.tools import tool
import getpass
from getscore import get_scores
from getstudent_id import get_student_id
from ensuretoken import ensure_token
load_dotenv()

username = input("Username: ")
password = getpass.getpass("Password: ")



@tool
def get_scores_tool():
    """Lấy điểm sinh viên từ hệ thống."""
    access_token = ensure_token(username, password)
    student_id = get_student_id(access_token)
    return get_scores(access_token, student_id)


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

agent = create_agent(llm, tools=[get_scores_tool], system_prompt= """Bạn là trợ lý tra cứu điểm.
                     Khi người dùng hỏi điểm (môn nào, học kỳ nào, hoặc tổng), PHẢI dùng tool get_scores_tool để lấy dữ liệu.
                     KHÔNG được bịa. Nếu không tìm thấy môn/ngữ cảnh thì nói không có dữ liệu.
                     """)

while True:
    q = input("\nBạn: ").strip()
    if q.lower() in {"exit", "quit"}:
        break

    result = agent.invoke({"messages": [{"role": "user", "content": q}]})
    msg = result["messages"][-1].content
    text = msg if isinstance(msg, str) else msg[0].get("text", "")
    print("Bot:", text) 

   