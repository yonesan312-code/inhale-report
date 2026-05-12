import streamlit as st
import google.generativeai as genai

# 1. 鍵（Secrets）の読み込み
if "GOOGLE_API_KEY" in st.secrets:
    # 古い通信トラブルを避ける設定
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport='rest')
else:
    st.error("Secretsの設定がまだ完了していません。")

st.title("🏥 Inhapi 報告支援ツール")

memo = st.text_area("訪問メモを貼り付けてください", height=200)

if st.button("✨ 分析を実行"):
    if not memo:
        st.warning("メモを入力してください。")
    else:
        with st.spinner("AIが最新モデルで分析中..."):
            try:
                # 最新モデルを呼び出す
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"以下のメモから精神科訪問看護報告書を作成して：\n\n{memo}")
                st.success("完了しました！")
                st.write(response.text)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
