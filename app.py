import streamlit as st
from nl_to_sql import generate_sql, run_query
st.set_page_config(page_title="AI SQL Chatbot", page_icon="■")
st.title("■ AI SQL Chatbot")
st.caption("Ask questions about your database in plain English.")
if "messages" not in st.session_state:
 st.session_state.messages = []
# Show past messages
for msg in st.session_state.messages:
 with st.chat_message(msg["role"]):
   st.write(msg["content"])

# Chat input box
question = st.chat_input("Ask something like: Show all customers from Delhi")
if question:
  st.session_state.messages.append({"role": "user", "content": question})
  with st.chat_message("user"):
    st.write(question)
  with st.chat_message("assistant"):
   try:
     sql = generate_sql(question)
     st.code(sql, language="sql")

     result_df = run_query(sql)
     st.dataframe(result_df)

     answer = f"Found {len(result_df)} result(s)."
     st.write(answer)
     st.session_state.messages.append(
        {"role": "assistant", "content": f"{answer}\n\nSQL used:\n{sql}"}
 )
   except Exception as e:
     st.error(f"Something went wrong: {e}")