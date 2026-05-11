import streamlit as st
import google.generativeai as genai

# よねさんのAPIキーをここに正確に入れてください
API_KEY = "AIzaSyD_iEp6BTocuGAnAWyQ4mmYHHKIeUe7JYk" 

genai.configure(api_key=API_KEY)

# 最強のプロンプトをシステム命令として定義
SYSTEM_PROMPT = """
あなたは、日本の精神科訪問看護の監査・実地指導対応に精通したエキスパートです。
以下の5項目を、客観的事実に基づき、一括生成してください。

1. 【主治医報告書】
   - 冒頭：「いつも大変お世話になっております。◯月の訪問看護の様子をご報告させていただきます。」
   - 結び：「今後とも何卒よろしくお願い申し上げます。」
   - 450文字程度の1段落。医療的必要性（ADLの変化等）を重視。

2. 【4要素記録（コードブロック内）】
   訴え/観察： / 実施： / 反応/アセスメント： / 継続：

3. 【超精密GAF評価】
   - [〇〇点] 根拠（症状面・機能面）を明記。

4. 【頻回訪問の根拠（アセスメントコード）】
   - [SI]社会的孤立 [AA]不安・焦燥 [HD]幻聴・妄想 [CD]認知・生活能力低下 [SR]自傷・他害リスク
   - 該当コードを抽出し、理由を記載。

5. 【出口戦略・看護計画評価】（※別枠出力）
   - 回数を減らす条件（週3→2への移行条件等）を提示し、[維持 / 縮小検討 / 終了準備]を判定。
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
        with st.spinner("AIが最新モデルで精密分析中..."):
            try:
                # 404エラーを確実に回避するための明示的なモデル指定
                model = genai.GenerativeModel(model_name='gemini-1.5-flash')
                full_query = f"システム命令: {SYSTEM_PROMPT}\n\n入力データ:\n回数:{freq}\nフェーズ:{phase}\n前回内容:{last}\n今回のメモ:{memo}"
                
                response = model.generate_content(full_query)
                st.success("分析が完了しました！")
                st.markdown(response.text)
            except Exception as e:
                # エラーの詳細を画面に出す（原因特定のため）
                st.error(f"技術的エラーが発生しました: {e}")
