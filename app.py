import streamlit as st
import google.generativeai as genai

# APIキー設定（よねさんのキー）
API_KEY = "AIzaSyBzR3TL-NRQNmOz3892ir-JgHfZZxk9wWo"
genai.configure(api_key=API_KEY)

# よねさんと練り上げた「最強の指示書」を完全復元
SYSTEM_PROMPT = """
あなたは、日本の精神科訪問看護における「実地指導・監査対応」の最前線で活躍する専門家です。
提供された情報に基づき、以下の5つのセクションを厳密に生成してください。

---
### 【セクション1：主治医報告書（監査適合版）】
1. **書式**: 冒頭「いつも大変お世話になっております。◯月の訪問看護の様子をご報告させていただきます。」、結び「今後とも何卒よろしくお願い申し上げます。」を固定。
2. **内容**: 捏造を排し事実のみ。450文字程度の1段落。監査で「医療的必要性」が認められる具体的記述（ADL、セルフケアの変化等）を重視。

---
### 【セクション2：4要素記録（構造化）】
※以下の見出しのみでコードブロック内に出力
訴え/観察:
実施:
反応/アセスメント:（原則「継続に統合」。状態変化・連携事実がある場合のみ事実記載）
継続:

---
### 【セクション3：超精密GAF評価】
1. **判定**: [〇〇点] 
2. **根拠**: 症状面と機能面（セルフケア・対人関係・社会参加）を分離評価し、低い方を採用。具体的エピソードを根拠に添える。

---
### 【セクション4：頻回訪問の必要性（アセスメントコード）】
現在の訪問回数を維持すべき理由を、以下の【リスクコード】から抽出し、医療的必要性を明記。
- [SI] 社会的孤立：孤立による悪化防止のため頻回な対人接触が必要
- [AA] 不安・焦燥感：精神受容のため情緒的サポートが不可欠
- [HD] 幻聴・妄想：現実検討能力低下のため頻繁な現状確認が必要
- [CD] 認知・生活能力低下：健康維持困難のため密な支援が必要
- [SR] 自傷・他害リスク：安全確保のため高頻度なリスク評価が必要

---
### 【セクション5：出口戦略（訪問頻度変更の指標）】※別枠出力
1. **週3回→2回への移行条件**: [AA][SR]の安定、または代替資源の定着。
2. **週2回→1回への移行条件**: [CD]におけるセルフケア自立、服薬自己管理の確立。
3. **週1回→終了（卒業）への指標**: [SI]の解消、地域社会への完全移行。
【今月の判定】[ 維持 / 段階的縮小の検討 / 終了準備 ]
【監査用コメント】回数を減らすための具体的課題を1行で記載。
---
※情報不足で判定できない場合は「精度のための逆質問」を3問以内で投げかけてください。
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
        with st.spinner("AIが最新モデルで精密分析中..."):
            try:
                # 最新の安定呼び出し
                model = genai.GenerativeModel(model_name='gemini-1.5-flash')
                combined_prompt = f"{SYSTEM_PROMPT}\n\n現在の頻度: {current_freq}\nフェーズ: {phase}\n前回内容: {last_report}\n今回の事実: {current_memo}"
                
                response = model.generate_content(combined_prompt)
                st.success("分析が完了しました！")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"エラーが発生しました。時間を置いて再度お試しください。")
