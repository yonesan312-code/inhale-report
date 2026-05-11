import streamlit as st
import google.generativeai as genai

# 設定
API_KEY = "AIzaSyBzR3TL-NRQNmOz3892ir-JgHfZZxk9wWo"
genai.configure(api_key=API_KEY)

# 監査・リスクコード・出口戦略 統合プロンプト
SYSTEM_PROMPT = """
あなたは、日本の精神科訪問看護における「実地指導・監査対応」の最前線で活躍する専門家です。
看護師のメモに基づき、以下の5つのセクションを厳密に生成してください。

---
### 【セクション1：主治医報告書（監査適合版）】
1. **書式**: 冒頭「いつも大変お世話になっております。◯月の訪問看護の様子をご報告させていただきます。」、結び「今後とも何卒よろしくお願い申し上げます。」を固定。
2. **内容**: 捏造を排し、事実のみで構成。450文字程度の1段落。
3. **視点**: 単なる様子見ではなく「医療的介入の必要性」が伝わる文面にする。

---
### 【セクション2：4要素記録（構造化）】
コードブロック内に以下のみ出力。
訴え/観察:
実施:
反応/アセスメント: 原則「継続に統合」。
継続:

---
### 【セクション3：超精密GAF評価】
1. **スコア**: [〇〇点] 
2. **根拠**: 症状面と機能面を分離して記載。

---
### 【セクション4：頻回訪問の必要性（アセスメントコード）】
現在の訪問回数を維持すべき理由を、以下の【リスクコード】から抽出し、医療的必要性を明記。
- [SI] 社会的孤立
- [AA] 不安・焦燥感
- [HD] 幻聴・妄想
- [CD] 認知・生活能力低下
- [SR] 自傷・他害リスク

---
### 【セクション5：出口戦略（訪問頻度変更の指標）】※別枠出力
1. 週3回→2回への移行条件
2. 週2回→1回への移行条件
3. 週1回→終了（卒業）への指標
【今月の判定】[ 維持 / 段階的縮小の検討 / 終了準備 ]
【監査用コメント】「回数を減らすための具体的課題」を1行で記載。
---
"""

st.set_page_config(page_title="Inhapi 統合支援システム", page_icon="🏥", layout="wide")

st.title("🏥 Inhapi 監査・出口戦略・リスクコード生成")

with st.sidebar:
    st.header("訪問設定")
    current_freq = st.selectbox("現在の訪問回数", ["週3回", "週2回", "週1回", "その他"])
    phase = st.selectbox("フェーズ", ["導入期", "安定期", "終結・移行期"])

col1, col2 = st.columns(2)
with col1:
    last_report = st.text_area("【前回の報告内容】", height=150)
with col2:
    current_memo = st.text_area("【今回の経過記録・メモ】", height=150, placeholder="ここにメモを貼り付けてください")

if st.button("✨ 監査・リスク分析を実行"):
    if not current_memo:
        st.error("経過メモを入力してください。")
    else:
        with st.spinner("最新のAIモデルで分析中..."):
            try:
                # ここがエラー対策の「flash」になっています
                model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)
                prompt_text = f"現在の頻度: {current_freq}\nフェーズ: {phase}\n\n【前回】\n{last_report}\n\n【今回】\n{current_memo}"
                response = model.generate_content(prompt_text)
                
                st.success("分析が完了しました！")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
