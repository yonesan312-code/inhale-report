import streamlit as st
import google.generativeai as genai

# 金庫（Secrets）から鍵を取り出す
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # 【ここが最重要】 transport='rest' を指定し、強制的に最新の通信方式（v1）を使わせます
    genai.configure(api_key=API_KEY, transport='rest')
except:
    st.error("StreamlitのSettings > Secretsに GOOGLE_API_KEY を設定してください。")

# --- 監査・リスクコード・出口戦略：最強プロンプト ---
SYSTEM_PROMPT = """
あなたは、日本の精神科訪問看護の監査・実地指導対応におけるエキスパートです。
提供された情報に基づき、以下の5セクションを生成してください。
1.主治医報告書 / 2.4要素記録 / 3.超精密GAF評価 / 4.リスクコード(SI,AA,HD,CD,SR) / 5.出口戦略
※事実に基づき、医療的必要性を明確にしてください。
"""

st.set_page_config(page_title="Inhapi 統合支援システム", page_icon="🏥", layout="wide")
st.title("🏥 Inhapi 監査・出口戦略・リスク生成")

with st.sidebar:
    st.header("訪問設定")
    freq = st.selectbox("現在の回数", ["週3回", "週2回", "週1回", "その他"])
    phase = st.selectbox("フェーズ", ["導入期", "安定期", "終結・移行期"])

memo = st.text_area("【経過記録・メモ】を貼り付けてください", height=200)

if st.button("✨ 監査・リスク分析を実行"):
    if not memo:
        st.error("メモを入力してください。")
    else:
        with st.spinner("最新モデル（Gemini 1.5 Flash）で精密分析中..."):
            try:
                # モデル名を明示的に指定
                model = genai.GenerativeModel('models/gemini-1.5-flash')
                
                # 指示とデータを合体
                full_query = f"システム指示: {SYSTEM_PROMPT}\n\n入力データ:\n現在の頻度:{freq}\nフェーズ:{phase}\nメモ:{memo}"
                
                response = model.generate_content(full_query)
                st.success("分析が完了しました！")
                st.markdown(response.text)
            except Exception as e:
                # 404エラーが出た場合、このメッセージで原因が分かります
                st.error(f"AI通信エラーが発生しました: {e}")
