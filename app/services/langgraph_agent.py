from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, SystemMessage, ToolMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
import json

from app.config import settings
from app.database import SessionLocal
from app.models.student import Student
from app.services.vector_service import vector_service


@tool
def get_student_by_id(student_id: str) -> str:
    """Retrieves structured student record by primary ID or student identifier string."""
    db = SessionLocal()
    try:
        # Check if integer ID or string register number
        if str(student_id).isdigit():
            student = db.query(Student).filter(Student.id == int(student_id)).first()
        else:
            student = db.query(Student).filter(
                (Student.email.ilike(f"%{student_id}%")) | 
                (Student.first_name.ilike(f"%{student_id}%"))
            ).first()

        if not student:
            return f"No student record found for identifier: {student_id}"

        return json.dumps({
            "id": student.id,
            "name": f"{student.first_name} {student.last_name}",
            "email": student.email,
            "department": student.department,
            "gpa": student.gpa,
            "bio_notes": student.bio_notes
        })
    finally:
        db.close()


@tool
def list_students_by_department(department: str) -> str:
    """Lists all students belonging to a specific department."""
    db = SessionLocal()
    try:
        students = db.query(Student).filter(Student.department.ilike(f"%{department}%")).all()
        return json.dumps([{"id": s.id, "name": f"{s.first_name} {s.last_name}", "gpa": s.gpa} for s in students])
    finally:
        db.close()


@tool
def search_student_bios_semantic(query: str) -> str:
    """Searches student bio notes semantically using vector search."""
    results = vector_service.search_similar_students(query)
    return json.dumps(results.get("documents", []))


tools = [get_student_by_id, list_students_by_department, search_student_bios_semantic]
tools_by_name = {t.name: t for t in tools}


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "The context messages"]


def create_student_chat_graph():
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        groq_api_key=settings.GROQ_API_KEY,
        temperature=0
    ).bind_tools(tools)

    def call_model(state: AgentState):
        system_msg = SystemMessage(
            content="You are an assistant for managing a Student Database. "
                    "When calling tools, always pass parameters strictly matching expected types. "
                    "Always format tool arguments as valid JSON string fields."
        )
        response = llm.invoke([system_msg] + list(state["messages"]))
        return {"messages": list(state["messages"]) + [response]}

    def call_tool(state: AgentState):
        last_message = state["messages"][-1]
        tool_outputs = []
        
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            for tool_call in last_message.tool_calls:
                tool_name = tool_call.get("name")
                tool_obj = tools_by_name.get(tool_name)
                
                if tool_obj is not None:
                    try:
                        output = tool_obj.invoke(tool_call.get("args", {}))
                    except Exception as e:
                        output = f"Error executing tool {tool_name}: {str(e)}"
                else:
                    output = f"Tool '{tool_name}' not found."
                
                tool_call_id = tool_call.get("id") or "default_id"
                tool_outputs.append(ToolMessage(
                    content=str(output),
                    tool_call_id=tool_call_id,
                    name=tool_name
                ))
                
        return {"messages": list(state["messages"]) + tool_outputs}

    def should_continue(state: AgentState):
        last_message = state["messages"][-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "call_tool"
        return END

    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("call_tool", call_tool)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue, {"call_tool": "call_tool", END: END})
    workflow.add_edge("call_tool", "agent")

    return workflow.compile()


agent_graph = create_student_chat_graph()