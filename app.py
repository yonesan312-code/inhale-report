import streamlit as st
import google.generativeai as genai

# 1. 鍵（Secrets）の読み込み
if "GOOGLE_API_KEY" in st.secrets:
    # 接続を安定させる設定を維持します
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport='rest')
else:
    st.error("Secretsの設定がまだ完了していません。")

# --- 最強プロンプトの定義 ---
SYSTEM_PROMPT = """
あなたは、日本の精神科訪問看護における監査・実地指導対応および出口戦略策定のプロフェッショナルです。
提供された情報から、以下の5つの項目を専門用語を用いて厳密に作成してください。

1. 【主治医報告書案】
   - 医療的必要性が伝わる客観的要約
2. 【看護記録（4要素記録）】
   - 精神症状、対人関係、生活状況、服薬状況を網羅した記録
3. 【GAF評価】
   - 今回の訪問時点での推定GAFスコアとその根拠
4. 【リスクコード判定】
   - SI(自死), AA(自傷他害), HD(生活崩壊), CD(認知低下), SR(社会的孤立)から該当を抽出
5. 【出口戦略と今後のプラン】
   - 頻度調整の可能性や、終結に向けた具体的なアプローチ
"""

st.set_page_config(page_title="Inhapi 統合支援システム", page_icon="🏥", layout="centered")

st.title("🏥 Inhapi 監査・出口戦略・リスク生成")
st.caption("精神科訪問看護 専門支援ツール")

# --- 2つの入力欄を復活 ---
last_report = st.text_area("【前回内容・経過記録】", placeholder="前回の状態や、申し送り事項を入力してください", height=100)
current_memo = st.text_area("【今回の訪問メモ】", placeholder="本日の発言、症状、看護介入の内容を入力してください", height=200)

# 実行ボタン
if st.button("✨ 監査・リスク分析を実行"):
    if not current_memo:
        st.warning("今回の訪問メモを入力してください。")
    else:
        with st.spinner("プロフェッショナルAIが精密分析中..."):
            try:
                # 最新モデル Gemini 1.5 Flash を使用
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # 入力データを合体
                user_input = f"【前回内容】:\n{last_report}\n\n【今回のメモ】:\n{current_memo}"
                
                # AIへの依頼
                response = model.generate_content(f"{SYSTEM_PROMPT}\n\n{user_input}")
                
                st.success("分析が完了しました！")
                st.divider()
                # 結果の表示
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"技術的エラーが発生しました: {e}")

st.info("※生成された内容は必ず看護師が確認し、適切に修正して使用してください。")
