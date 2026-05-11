import streamlit as st
import google.generativeai as genai

# 【重要】ここを「よねさんのAPIキー」に書き換えてください！
API_KEY = "AIzaSyD_iEp6BTocuGAnAWyQ4mmYHHKIeUe7JYk" 

genai.configure(api_key=API_KEY)

SYSTEM_PROMPT = """
あなたは、日本の精神科訪問看護における「実地指導・監査対応」のプロフェッショナルです。
提供された情報に基づき、以下の5つのセクションを厳密に生成してください。
1. 主治医報告書（監査適合版）
2. 4要素記録（構造化）
3. 超精密GAF評価
4. 頻回訪問の必要性（アセスメントコード：[SI][AA][HD][CD][SR]）
5. 出口戦略（週3→2、2→1への具体的移行条件と判定）
※捏造は厳禁です。
"""

st.set_page_config(page_title="Inhapi 統合支援システム", page_icon="🏥", layout="wide")
st.title("🏥 Inhapi 監査・出口戦略・リスクコード生成")

with st.sidebar:
    st.header("訪問設定")
    current_freq = st.selectbox("現在の訪問回数", ["週3回", "週2回", "週1回", "その他"])
    phase = st.selectbox("フェーズ", ["導入期", "安定期", "終結・移行期"])

last_report = st.text_area("【前回の報告内容】", height=100)
current_memo = st.text_area("【今回の経過記録・メモ】", height=150, placeholder="メモを貼り付けてください")

if st.button("✨ 監査・リスク分析を実行"):
    if not current_memo:
        st.error("経過メモを入力してください。")
    else:
        with st.spinner("AIが最新モデルで分析中..."):
            try:
                # 404エラーを回避するための最新の呼び出し方
                model = genai.GenerativeModel(model_name='gemini-1.5-flash')
                combined_prompt = f"{SYSTEM_PROMPT}\n\n現在の頻度: {current_freq}\nフェーズ: {phase}\n前回: {last_report}\n今回: {current_memo}"
                
                response = model.generate_content(combined_prompt)
                st.success("分析が完了しました！")
                st.markdown(response.text)
            except Exception as e:
                # 何が原因か特定するために、詳しいエラーを表示させます
                st.error(f"エラーが発生しました: {e}")
