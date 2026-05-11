import streamlit as st
import google.generativeai as genai

# 設定（よねさんのAPIキーを設定済みです）
API_KEY = "AIzaSyBzR3TL-NRQNmOz3892ir-JgHfZZxk9wWo"
genai.configure(api_key=API_KEY)

# 最強プロンプトの指示
SYSTEM_PROMPT = """
あなたは、日本の精神科訪問看護における実地指導・監査対応のプロフェッショナルであり、利用者の強みを引き出すエンパワメント・アプローチの専門家です。
入力された【データ】に基づき、以下の「運用ルール」を厳守して4つの書類を作成してください。

【運用ルール：GAF精度と出口戦略の厳守】
1. GAFスコアを「誤差1点以内」で特定するため、以下の【GAF評価の5軸】（A.危険行動 / B.現実検討能力 / C.コミュニケーション / D.社会的機能 / E.セルフケア自立度）を分析してください。
2. 「誤差1点以内」の特定が困難な場合、または「出口戦略（卒業・移行）」の具体的指標が不足している場合は、書類作成を開始せず、必ず私に最大3つの具体的な【逆質問】をしてください。
3. 情報が十分な場合のみ、指定フォーマットで出力してください。
"""

st.set_page_config(page_title="Inhapi 報告書支援", page_icon="🏥")
st.title("🏥 Inhapi 報告書作成ツール")
st.caption("ログイン不要・スマホ対応 / 生成AI活用")

with st.form("input_form"):
    phase = st.selectbox("現在のフェーズ", ["導入期", "安定期", "終結期・移行期", "その他"])
    last_report = st.text_area("先月の報告書（コピペ用）", height=100)
    current_memo = st.text_area("今月の経過・メモ（今日の様子など）", height=200, help="断片的なメモでOKです。AIが整形します。")
    
    submitted = st.form_submit_button("✨ 最高の報告書を生成する")

if submitted:
    if not current_memo:
        st.warning("今月の経過メモを入力してください。")
    else:
        with st.spinner("AIがプロの視点で執筆中..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-pro', system_instruction=SYSTEM_PROMPT)
                response = model.generate_content(f"フェーズ: {phase}\n先月の内容: {last_report}\n今月の事実: {current_memo}")
                
                st.success("作成完了！")
                st.markdown("---")
                st.markdown(response.text)
                st.info("💡 上の文章をコピーして電子カルテ等に貼り付けてください。")
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
