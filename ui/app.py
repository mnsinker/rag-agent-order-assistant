import sys
from pathlib import Path
import streamlit as st

# 1. 环境路径设置
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agent.agent import agent
from audit.audit_logger import AuditLogger


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


# --- 页面配置 ---
st.set_page_config(page_title="AI Order Agent", layout="centered")
st.title("🧠 AI Order Decision System")

# --- 初始化 Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 侧边栏设置 ---
with st.sidebar:
    st.header("设置")
    # 这里的 checkbox 仅控制“当前”执行时是否记录/显示，不应影响历史记录的显示逻辑
    show_audit = st.checkbox("实时显示执行过程 (Audit)", value=True)
    if st.button("清除聊天记录"):
        st.session_state.messages = []
        st.rerun()

# --- 渲染历史消息 ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # 修复点：只要这条历史消息里存了 logs，就显示详情，不随左侧勾选框改变而消失
        if message.get("audit_logs"):
            with st.expander("🔍 查看执行详情"):
                render_audit_timeline(message["audit_logs"])

# --- 聊天输入框 ---
if prompt := st.chat_input("帮我判断订单123有没有风险"):

    # 1. 用户消息
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. 助手响应
    with st.chat_message("assistant"):
        # 核心修复：确保 AuditLogger 始终根据当前勾选状态初始化
        audit = AuditLogger(enabled=show_audit)

        # 使用 status 组件展示实时过程
        with st.status("AI 正在处理...", expanded=show_audit) as status:
            try:
                # 执行核心逻辑
                result = agent(prompt, audit)
                final_answer = result["data"]

                # 获取本次执行的日志
                current_logs = audit.get_logs() if show_audit else []

                # 实时渲染日志到 status 内部
                if show_audit and current_logs:
                    render_audit_timeline(current_logs)

                status.update(label="处理完成!", state="complete", expanded=False)

            except Exception as e:
                status.update(label="运行出错", state="error")
                st.error(f"错误: {e}")
                final_answer = "抱歉，处理出错。"
                current_logs = []

        # 显示最终文字结果
        st.markdown(final_answer)

        # 将结果和日志完整存入 session_state
        st.session_state.messages.append({
            "role": "assistant",
            "content": final_answer,
            "audit_logs": current_logs  # 确保日志被存下来了
        })

        # 强制刷新一下，确保 UI 状态同步（可选，但推荐）
        st.rerun()