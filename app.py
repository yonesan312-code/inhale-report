import streamlit as st
import google.generativeai as genai

# 1. 鍵（Secrets）の読み込み
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Secretsに GOOGLE_API_KEY が入っていません。")

st.title("🏥 Inhapi 統合支援システム")

# 2. 入力欄
memo = st.text_area("訪問メモを貼り付けてください", height=200)

# 3. 実行ボタン
if st.button("✨ 分析を実行"):
    if not memo:
        st.warning("メモを入力してください。")
    else:
        with st.spinner("AIが分析中..."):
            try:
                # 404エラーを回避する最新モデルの呼び出し
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"精神科訪問看護の視点で報告書とリスク評価を作成して：\n\n{memo}")
                st.success("完了しました！")
                st.write(response.text)
            except Exception as e:
                st.error(f"技術的エラー: {e}")
