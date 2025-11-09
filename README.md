# 100math 💯

100マス計算用のPDFを生成するPython製CLIツールです。

SPI対策のために100マス計算を手軽に実施したいと考え、1時間のプチハッカソンで開発しました。

## ✨ 主な機能

* **四則演算に対応**: 足し算、引き算、掛け算、割り算の計算問題を作成できます。
* **桁数の指定**: 1桁～4桁まで対応し、左側と上側で異なる桁数を指定することもできます。
* **PDF出力**: A4サイズのPDFとして問題と解答が生成されるため、すぐに印刷して使えます。

## 🖼️ 出力サンプル

[生成されたPDFのサンプル(2桁と1桁のたし算)](./sample/hyakumasu_たしざん_2x1keta.pdf)


## 🚀 使い方

### 1. セットアップ

本ツールはPython環境で動作します。はじめにリポジトリをクローンし、必要なライブラリをインストールしてください。

**A) uv を使う場合 (推奨)**
```bash
git clone https://github.com/emi-12d/100math.git
cd 100math
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

**B) venv + pip を使う場合**
```bash
git clone https://github.com/emi-12d/100math.git
cd 100math
python -m venv .venv
source .venv/bin/activate  # Windowsの場合は `.venv\Scripts\activate`
pip install -r requirements.txt
```

### 2. 実行

`main.py` に引数を渡して実行すると、カレントディレクトリにPDFファイルが生成されます。

```bash
python main.py <operator> <left_digits> <top_digits>
```

**実行例:**
```bash
# 2桁と1桁の足し算
python main.py "+" 2 1

# 2桁同士の掛け算
python main.py "*" 2 2

# 3桁と2桁の引き算
python main.py "-" 3 2
```
生成されるファイル名: `hyakumasu_たしざん_2x1keta.pdf` のように、内容が分かる名前で問題と解答（`_ans.pdf`付き）が出力されます。

## 📝 コマンドライン引数

| 引数          | 説明                               | 指定できる値                                           | 必須 |
| :------------ | :--------------------------------- | :----------------------------------------------------- | :--- |
| `operator`    | 計算の種類を指定します。           | `+` (足し算), `-` (引き算), `*` (掛け算), `/` (割り算) | ✅    |
| `left_digits` | 左側の数字の桁数を指定します。     | `1`～`4`の整数                                          | ✅    |
| `top_digits`  | 上側（ヘッダー）の数字の桁数を指定します。 | `1`～`4`の整数                                          | ✅    |

## 📄 ライセンス

このプロジェクトは [MIT License](LICENSE) の下で公開されています。