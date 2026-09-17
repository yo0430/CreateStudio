# Assembler Agent 仕様書 (Assembler Agent Spec)

## 1. 概要
Assembler Agentは、Critic Agentの審査を通過したクリップ群をタイムライン順に結合し、音声（ナレーション）、BGM、テロップ（字幕）をレイヤー合成して、プラットフォーム最適化された最終動画を出力するエージェントです。

---

## 2. 処理パイプライン

1. **映像結合 (Video Concatenation)**:
   - 全クリップの解像度・フレームレート（例: 1080x1920, 25fps または 30fps）を統一。
   - FFmpeg concat filter を用いた結合処理。
2. **音声トラック合成 & ダッキング**:
   - ナレーション音声（TTS生成または事前録音ファイル）の配置。
   - BGMトラックの音量をナレーション発話区間で-12dB自動減衰（Sidechain ducking）。
3. **テロップ（字幕）描画**:
   - `telop_text` を画面下部または中央に描画。
   - フォントサイズ、縁取り（Stroke）、視認性の高い配色。
4. **エンコード & 出力**:
   - コーデック: H.264 (`libx264`), AAC (`aac`)
   - プリセット: `fast` または `medium`
   - Faststart フラグ（Web再生最適化）付与。
