import streamlit as st
# インストールを待つための処理
try:
    import google.generativeai as genai
except ImportError:
    st.error("現在、道具箱をインストール中です。1分後にこの画面を更新（再読み込み）してください。")
    st.stop()

# 鍵の読み込み
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Secretsに鍵を設定してください。")

st.title("🏥 Inhapi 報告支援ツール")

memo = st.text_area("訪問メモを貼り付けてください", height=200)

if st.button("✨ 分析を実行"):
    if not memo:
        st.warning("メモを入力してください。")
    else:
        with st.spinner("AIが考え中..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"精神科訪問看護報告書を作成して：\n\n{memo}")
                st.success("完了！")
                st.write(response.text)
            except Exception as e:
                st.error(f"エラー: {e}")
