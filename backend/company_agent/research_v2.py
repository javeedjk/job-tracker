import os
from typing import TypedDict
from dotenv import load_dotenv
from tavily import TavilyClient
from openai import OpenAI
from langgraph.graph import StateGraph, START, END

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# "State" is just a shared notebook that gets passed between steps.
# Each step reads from it and writes its own findings into it.
class ResearchState(TypedDict):
    company_name: str
    news_summary: str
    tech_summary: str
    interview_summary: str
    final_report: str

def search_and_summarize(query: str, instruction: str) -> str:
    results = tavily.search(query=query, max_results=5)
    context = "\n\n".join([f"{r['title']}: {r['content']}" for r in results["results"]])
    response = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": context}
        ]
    )
    return response.choices[0].message.content

def news_node(state: ResearchState) -> dict:
    summary = search_and_summarize(
        query=f"{state['company_name']} company recent news hiring",
        instruction="Summarize recent news relevant to a job applicant. Be factual, note dates where possible."
    )
    return {"news_summary": summary}

def tech_node(state: ResearchState) -> dict:
    summary = search_and_summarize(
        query=f"{state['company_name']} engineering blog tech stack architecture",
        instruction="Summarize what technologies this company uses based on the results. If nothing specific found, say so."
    )
    return {"tech_summary": summary}

def interview_node(state: ResearchState) -> dict:
    summary = search_and_summarize(
        query=f"{state['company_name']} interview experience Glassdoor Blind reviews",
        instruction="Summarize what candidates say about the interview process and culture there."
    )
    return {"interview_summary": summary}

def synthesize_node(state: ResearchState) -> dict:
    combined = f"""NEWS:
{state['news_summary']}

TECH STACK:
{state['tech_summary']}

INTERVIEW & CULTURE:
{state['interview_summary']}"""
    response = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Combine these three research summaries into one clean, organized interview-prep briefing with headers. Be concise."},
            {"role": "user", "content": f"Company: {state['company_name']}\n\n{combined}"}
        ]
    )
    return {"final_report": response.choices[0].message.content}

# Build the graph: three nodes run in parallel from START, then both feed into synthesize
graph = StateGraph(ResearchState)
graph.add_node("news", news_node)
graph.add_node("tech", tech_node)
graph.add_node("interview", interview_node)
graph.add_node("synthesize", synthesize_node)

graph.add_edge(START, "news")
graph.add_edge(START, "tech")
graph.add_edge(START, "interview")
graph.add_edge("news", "synthesize")
graph.add_edge("tech", "synthesize")
graph.add_edge("interview", "synthesize")
graph.add_edge("synthesize", END)

app = graph.compile()

if __name__ == "__main__":
    import sys
    company = sys.argv[1] if len(sys.argv) > 1 else "Razorpay"
    result = app.invoke({"company_name": company})
    print(result["final_report"])