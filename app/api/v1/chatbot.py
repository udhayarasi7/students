from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage
from app.schemas.student import ChatQuery, ChatResponse
from app.services.langgraph_agent import agent_graph

router = APIRouter(prefix="/chat", tags=["AI Chatbot"])

# Existing POST endpoint
@router.post("/", response_model=ChatResponse)
def chat_with_database(query: ChatQuery):
    try:
        inputs = {"messages": [HumanMessage(content=query.message)]}
        result = agent_graph.invoke(inputs)
        return ChatResponse(response=result["messages"][-1].content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/")
async def chat_with_agent(q: str):
    try:
        response = agent_graph.invoke({"messages": [HumanMessage(content=q)]})
        last_message = response["messages"][-1]
        return {"response": last_message.content}
    except Exception as e:
        # Internal server 500 crasheng-a thavirka readable error response
        raise HTTPException(
            status_code=500, 
            detail=f"AI Agent Error (Check API limits/keys): {str(e)}"
        )
# New GET endpoint for easy browser testing
@router.get("/")
def chat_get_test(q: str = "List all students"):
    try:
        inputs = {"messages": [HumanMessage(content=q)]}
        result = agent_graph.invoke(inputs)
        return {"query": q, "response": result["messages"][-1].content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))