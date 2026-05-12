import streamlit as st
import google.generativeai as genai

# 金庫（Secrets）から鍵を取り出す
try:
    if "GOOGLE_API_KEY" in st.secrets:
        # transport='rest' を指定し、通信トラブルを回避します
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport='rest')
    else:
        st.error("金庫（Secrets）に GOOGLE_API_KEY が入っていません。")
except Exception as e:
    st.error(f"初期設定エラー: {e}")

# 監査・出口戦略・リスク：プロフェッショナル指示書
SYSTEM_PROMPT = """
あなたは精神科訪問看護の専門家です。
1.主治医報告書 / 2.4要素記録 / 3.超精密GAF評価 / 4.リスクコード / 5.出口戦略
これらを一括で作成してください。
"""

st.set_page_config(page_title="Inhapi 統合支援システム", page_icon="🏥")
st.title("🏥 Inhapi 統合支援システム")

memo = st.text_area("訪問時のメモを貼り付けてください", height=200)

if st.button("✨ 監査・リスク分析を実行"):
    if not memo:
        st.warning("メモを入力してください。")
    else:
        with st.spinner("最新AIで精密分析中..."):
            try:
                # 404エラーを物理的に回避する最新の呼び出し方
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{SYSTEM_PROMPT}\n\nメモ:\n{memo}")
                st.success("分析が完了しました！")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"AI通信エラー: {e}")
