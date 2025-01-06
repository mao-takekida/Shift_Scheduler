# app.py (Streamlit)
import pandas as pd
import streamlit as st

# サンプルデータ
data = {"ID": [1, 2, 3], "Name": ["Alice", "Bob", "Charlie"], "Age": [25, 30, 35]}
df = pd.DataFrame(data)

st.title("データ編集アプリ")
st.write("以下のテーブルを編集してください:")

# データ編集
edited_df = st.data_editor(df)

# 保存ボタン
if st.button("保存"):
    st.write("データが保存されました!")
    st.write(edited_df)
