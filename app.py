import streamlit as st
import google.generativeai as genai

# 1. 鍵（Secrets）の読み込み
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("StreamlitのSettings > Secretsに鍵（GOOGLE_API_KEY）が入っていません。")

# 2. 最強の指示書（プロンプト）
SYSTEM_PROMPT = """
あなたは、日本の精神科訪問看護の監査・実地指導対応に精通したエキスパートです。
提供された情報から、以下の5項目を厳密に生成してください。
1.【主治医報告書】/ 2.【4要素記録】 / 3.【超精密GAF評価】 / 4.【リスクコード判定】 / 5.【出口戦略】
"""

st.set_page_config(page_title="Inhapi 統合支援システム", page_icon="🏥", layout="wide")
st.title("🏥 Inhapi 監査・出口戦略・リスク生成")

with st.sidebar:
    st.header("訪問設定")
    freq = st.selectbox("現在の回数", ["週3回", "週2回", "週1回"])
    phase = st.selectbox("フェーズ", ["導入期", "安定期", "終結・移行期"])

last = st.text_area("【前回の報告内容】", height=100)
memo = st.text_area("【今回の経過記録・メモ】", height=150)

if st.button("✨ 監査・リスク分析を実行"):
    if not memo:
        st.error("経過メモを入力してください。")
    else:
        with st.spinner("AIが分析中..."):
            try:
                # 【ここが修正ポイント】最もエラーが起きにくい呼び出し方に変更しました
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # システム指示とユーザー入力を合体させて送る（古いSDKでも動く形式）
                prompt = f"{SYSTEM_PROMPT}\n\n現在の回数:{freq}\nフェーズ:{phase}\n前回内容:{last}\n今回のメモ:{memo}"
                
                response = model.generate_content(prompt)
                st.success("分析完了！")
                st.markdown(response.text)
            except Exception as e:
                # 万が一エラーが出た場合、原因を特定するために詳細を表示します
                st.error(f"技術的エラーが発生しました: {e}")
