import streamlit as st
import google.generativeai as genai

# 金庫（Secrets）から鍵を自動で取り出す設定
try:
    # 鍵をGitHubに書かずに、Streamlitの金庫から呼び出します
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("金庫に鍵（APIキー）が入っていません。Streamlitの Settings > Secrets を確認してください。")

# --- 以降、最強のプロンプトとアプリの動きはそのままです ---
SYSTEM_PROMPT = """
あなたは、日本の精神科訪問看護の監査・実地指導対応に精通したエキスパートです。
以下の5項目を、客観的事実に基づき、一括生成してください。
1. 主治医報告書 / 2. 4要素記録 / 3. 超精密GAF評価 / 4. リスクコード判定 / 5. 出口戦略
"""

st.set_page_config(page_title="Inhapi 統合支援システム", page_icon="🏥", layout="wide")
st.title("🏥 Inhapi 監査・出口戦略・リスク生成")

with st.sidebar:
    freq = st.selectbox("現在の回数", ["週3回", "週2回", "週1回"])
    phase = st.selectbox("フェーズ", ["導入期", "安定期", "終結・移行期"])

last = st.text_area("【前回の報告内容】", height=100)
memo = st.text_area("【今回の経過記録・メモ】", height=150)

if st.button("✨ 監査・リスク分析を実行"):
    if not memo:
        st.error("メモを入力してください。")
    else:
        with st.spinner("AIが精密分析中..."):
            try:
                model = genai.GenerativeModel(model_name='gemini-1.5-flash')
                response = model.generate_content(f"{SYSTEM_PROMPT}\n\n回数:{freq}\n前回:{last}\n今回:{memo}")
                st.success("分析完了！")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
