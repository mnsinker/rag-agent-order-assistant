import sys
from pathlib import Path
import streamlit as st
# 1. 环境路径设置
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agent.agent import agent
from audit.audit_logger import AuditLogger

# 2. render 逻辑: 可视化渲染
def render_audit_timeline(logs):
    if not isinstance(logs, list):
        st.warning("audit_logs 格式不正确")
        return

    for i, log in enumerate(logs, start=1):
        step = log.get("step", "unknown")

        if step == "llm_raw":
            title = "LLM Intent Parsing"
        elif step == "before_tool":
            title = f"Run Tool:  {log.get('tool')}"
        elif step == "after_tool":
            title = f"Tool Result:  {log.get('tool')}"
        elif step == "final_answer":
            title = "Generate Final Answer"
        elif step == "error":
            title = "Error"
        else:
            title = step

        with st.expander(f"{i}. {title}", expanded=False):
            st.json(log)

def render_runtime_graph(planned_tools):
    if not planned_tools:
        st.info("No runtime graph")
        return

    graph_text = "\n ↓\n".join(f"{tool}()" for tool in planned_tools)
    st.code(graph_text, language="python")

def render_runtime_state(tool_results):
    if not tool_results:
        st.info("No runtime state")
        return

    for i, result in enumerate(tool_results, start=1):
        dto_name = type(result).__name__
        with st.expander(f"{i}. {dto_name}"):
            if hasattr(result, "__dict__"): # 这个 dto_obj 是否带 __dict__ (obj默认都会带, 把属性和值 转为 dict)
                st.json(result.__dict__)
            else:
                st.write(result)


# --- 页面配置 ---
st.set_page_config(page_title="AI Order Decision System", layout="centered")
st.title("🧠 AI Order Decision System")

# --- 初始化 Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# # --- 侧边栏设置 ---
# with st.sidebar:
#     # 这里的 checkbox 仅控制“当前”执行时是否记录/显示，不应影响历史记录的显示逻辑
#     if st.button("Clear Chat"):
#         st.session_state.messages = []
#         st.rerun()

# --- 渲染历史消息 ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("audit_logs"):
            with st.expander("🔍 Execution Details"):
                tab1, tab2, tab3 = st.tabs([
                    "Audit Logs",
                    "Runtime Graph",
                    "Runtime State"
                ])
                with tab1:
                    render_audit_timeline(message["audit_logs"])
                with tab2:
                    render_runtime_graph(message.get("planned_tools", []))
                with tab3:
                    render_runtime_state(message.get("tool_results", []))


# --- 聊天输入框 ---
if prompt := st.chat_input("帮我判断订单123有没有风险"):

    # 1. 用户消息
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. 助手响应
    with st.chat_message("assistant"):
        # 初始化 audit 对象
        audit = AuditLogger(enabled=True)

        # 使用 status 组件展示实时过程
        with st.status("AI 正在处理...", expanded=True) as status:
            try:
                # 执行核心逻辑
                result = agent(prompt, audit)
                response = result["response"]
                trace = result["trace"]
                final_answer = response["data"]

                # 获取本次执行的日志
                current_logs = audit.get_logs()

                # 实时渲染日志到 status 内部
                if current_logs:
                    render_audit_timeline(current_logs)

                status.update(label="处理完成!", state="complete", expanded=False)

            except Exception as e:
                status.update(label="运行出错", state="error")
                st.error(f"错误: {e}")
                final_answer = "抱歉，处理出错。"
                current_logs = []

        # 显示最终文字结果
        st.markdown(final_answer)

        # 将 audit, graph, tool_results 完整存入 session_state
        st.session_state.messages.append({
            "role": "assistant",
            "content": final_answer,

            "audit_logs": trace["audit_logs"],
            "planned_tools": trace["planned_tools"],
            "tool_results": trace["tool_results"],
        })

        # 强制刷新一下，确保 UI 状态同步（可选，但推荐）
        st.rerun()