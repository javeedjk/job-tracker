import os
from dotenv import load_dotenv
from tavily import TavilyClient
from openai import OpenAI

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def research_company(company_name: str) -> str:
    # Step 1: search for recent news
    results = tavily.search(
        query=f"{company_name} company recent news engineering hiring",
        max_results=5
    )
    context = "\n\n".join([f"{r['title']}: {r['content']}" for r in results["results"]])

    # Step 2: summarize with LLM
    response = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You summarize company research for a job applicant preparing for interviews. Be factual, cite what's recent, and flag if info seems outdated."},
            {"role": "user", "content": f"Summarize what a job applicant should know about {company_name} based on this:\n\n{context}"}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    import sys
    company = sys.argv[1] if len(sys.argv) > 1 else "Razorpay"
    print(research_company(company))