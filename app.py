import streamlit as st
import google.generativeai as genai
import os

# 1. 鍵の読み込み（金庫から取り出す）
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    # 通信方式を「v1」に強制固定する設定です
    genai.configure(api_key=api_key, transport='rest')
except Exception:
    st.error("StreamlitのSettings > Secretsに GOOGLE_API_KEY が設定されていません。")

# 2. 賢い指示書
SYSTEM_PROMPT = """
あなたは精神科訪問看護の監査・実地指導対応の専門家です。
看護師のメモから、以下の5つを厳密に作成してください。
1. 主治医報告書 / 2. 4要素記録 / 3. GAF評価 / 4. リスクコード / 5. 出口戦略
"""

st.title("🏥 Inhapi 統合支援システム")

last = st.text_area("【前回内容】")
memo = st.text_area("【今回のメモ】")

if st.button("✨ 分析を実行"):
    if not memo:
        st.error("メモを入力してください。")
    else:
        with st.spinner("最新モデルで分析中..."):
            try:
                # 404エラーを回避するため、モデル名を直接指定します
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{SYSTEM_PROMPT}\n\n前回:{last}\n今回:{memo}")
                st.success("完了しました！")
                st.markdown(response.text)
            except Exception as e:
                # もしエラーが出ても、原因がわかるように詳しく表示します
                st.error(f"技術的エラー: {e}")
