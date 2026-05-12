import streamlit as st
import google.generativeai as genai

# 金庫（Secrets）の読み込みを「より確実な方法」に変えました
try:
    # 直接 st.secrets から取得します
    my_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=my_key)
except Exception as e:
    st.error(f"金庫の鍵が開けられません。設定を確認してください: {e}")
    st.stop()

# 指示書（プロンプト）
SYSTEM_PROMPT = """
あなたは精神科訪問看護の専門家です。
1.主治医報告書 / 2.4要素記録 / 3.GAF評価 / 4.リスクコード / 5.出口戦略
これらを一括で作成してください。
"""

st.title("🏥 Inhapi 統合支援システム")

last = st.text_area("【前回内容】", height=100)
memo = st.text_area("【今回のメモ】", height=200)

if st.button("✨ 監査・リスク分析を実行"):
    if not memo:
        st.warning("メモを入力してください。")
    else:
        with st.spinner("最新AIが分析中..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{SYSTEM_PROMPT}\n\n前回:{last}\n今回:{memo}")
                st.success("完了しました！")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"AI通信エラー: {e}")
