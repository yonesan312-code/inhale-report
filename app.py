import streamlit as st
import google.generativeai as genai

# 1. 鍵の読み込み
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Secretsの設定（鍵）がまだ完了していません。")

# 2. 画面のタイトル
st.title("🏥 Inhapi 報告支援ツール")

# 3. 入力欄
memo = st.text_area("訪問メモを入力してください", height=200)

# 4. ボタン
if st.button("AI分析を実行"):
    if not memo:
        st.warning("メモを入力してください。")
    else:
        with st.spinner("AIが考え中..."):
            try:
                # 接続エラーを回避する最新の呼び出し方
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"以下のメモから訪問看護報告書を作成して：\n\n{memo}")
                st.success("作成完了！")
                st.write(response.text)
            except Exception as e:
                st.error(f"技術的なエラー：{e}")
