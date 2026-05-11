# file: masothue_demo.py
import asyncio
import os
from browser_use import Agent, Browser, ChatAnthropic, ChatBrowserUse, ChatGoogle, ChatOllama, ChatOpenAI
from dotenv import load_dotenv
from browser_use.llm import ChatDeepSeek


def build_llm():
    load_dotenv()
    # if os.getenv("GOOGLE_API_KEY"):
    #     return ChatGoogle(model="gemini-2.0-flash")
    # if os.getenv("BROWSER_USE_API_KEY"):
    #     return ChatBrowserUse()
    if os.getenv("ANTHROPIC_AUTH_TOKEN"):
        return ChatAnthropic(
            model="haiku-4-5-20251001",
            api_key=os.getenv("ANTHROPIC_AUTH_TOKEN"),
            base_url=os.getenv("ANTHROPIC_BASE_URL", "https://gw.claudeapi.com"),
        )
    if os.getenv("ANTHROPIC_API_KEY"):
        return ChatAnthropic(model="haiku-4-5-20251001", api_key=os.getenv("ANTHROPIC_API_KEY"))
    if os.getenv("OPENAI_API_KEY"):
        return ChatOpenAI(model="gpt-4.1-mini")
    raise RuntimeError(
        "Missing LLM API key. Add one key in .env: OPENAI_API_KEY or GOOGLE_API_KEY or ANTHROPIC_API_KEY"
    )

async def main():
    tax_code = "3101156111"
    browser = Browser(headless=False)
    agent = Agent(
        task=(
            f"Vào https://masothue.com và CHI duoc thao tac tren trang chu. "
            "TUYET DOI khong duoc navigate truc tiep toi URL tim kiem co query string (khong duoc vao /Search?q=...). "
            f"Bat buoc nhap ma so thue {tax_code} vao dung o input co id='search' (name='q', placeholder='Nhập mã số thuế, CMND, tên công ty') roi bam nut tim kiem tren giao dien. "
            "Sau khi bấm tìm kiếm, chờ trang tải tối đa 25 giây để danh sách kết quả xuất hiện. "
            "Nếu bị vòng xoay loading quá lâu hoặc không ra kết quả thì refresh trang 1 lần và tìm lại đúng mã số thuế đó. "
            "Mở trang chi tiết doanh nghiệp, sau đó lấy toàn bộ thông tin đang hiển thị trên trang "
            "(tên doanh nghiệp, mã số thuế, trạng thái, ngày cấp, địa chỉ, người đại diện, ngành nghề, thông tin liên hệ, "
            "chi nhánh/phụ thuộc hoặc các trường khác nếu có). "
            "Trả về kết quả dưới dạng JSON đầy đủ, không bỏ sót trường nào nhìn thấy được."
        ),
        llm=build_llm(),
        fallback_llm=ChatGoogle(model="gemini-2.0-flash") if os.getenv("GOOGLE_API_KEY") else None,
        browser=browser,
    )
    result = await agent.run()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())