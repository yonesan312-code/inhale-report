import streamlit as st
import google.generativeai as genai

# APIキーの設定
API_KEY = "AIzaSyBzR3TL-NRQNmOz3892ir-JgHfZZxk9wWo"
genai.configure(api_key=API_KEY)

# 最強のプロンプト（内容はそのままです）
SYSTEM_PROMPT = """
あなたは、日本の精神科訪問看護における「実地指導・監査対応」の最前線で活躍する専門家です。
以下の5つのセクションを厳密に生成してください。
1. 主治医報告書（監査適合版）
2. 4要素記録（構造化）
3. 超精密GAF評価
4. 頻回訪問の必要性（アセスメントコード）
5. 出口戦略（訪問頻度変更の指標）
"""

st.set_page_config(page_title="Inhapi 統合支援システム", page_icon="🏥")
st.title("🏥 Inhapi 監査・出口戦略・リスクコード生成")

with st.sidebar:
    current_freq = st.selectbox("現在の訪問回数", ["週3回", "週2回", "週1回", "その他"])
    phase = st.selectbox("フェーズ", ["導入期", "安定期", "終結・移行期"])

last_report = st.text_area("【前回の報告内容】", height=100)
current_memo = st.text_area("【今回の経過記録・メモ】", height=150)

if st.button("✨ 監査・リスク分析を実行"):
    if not current_memo:
        st.error("経過メモを入力してください。")
    else:
        with st.spinner("AIが分析中..."):
            try:
                # 404エラーを防ぐための、最も安定した呼び出し方です
                model = genai.GenerativeModel('gemini-1.5-flash')
                full_prompt = f"{SYSTEM_PROMPT}\n\n現在の頻度: {current_freq}\nフェーズ: {phase}\n前回: {last_report}\n今回: {current_memo}"
                
                response = model.generate_content(full_prompt)
                st.success("分析が完了しました！")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
