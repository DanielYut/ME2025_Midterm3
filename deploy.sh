#!/bin/bash

# === 設定區（請依你專案調整） ===
REPO_URL="https://github.com/你的帳號/你的Repo.git"
PROJECT_DIR="$HOME/ME2025_Midterm3"
VENV_DIR="$PROJECT_DIR/.venv"
PYTHON_BIN="python3"
APP_FILE="app.py"

echo "[INFO] 部署腳本開始執行..."

# ====================================
# 第一次執行：clone + 建立環境 + 啟動
# ====================================
if [ ! -d "$PROJECT_DIR" ]; then
    echo "[INFO] 第一次部署：Clone repository"

    git clone "$REPO_URL" "$PROJECT_DIR"
    cd "$PROJECT_DIR" || exit

    echo "[INFO] 建立虛擬環境 .venv"
    $PYTHON_BIN -m venv "$VENV_DIR"

    echo "[INFO] 啟動虛擬環境並安裝 requirements.txt"
    source "$VENV_DIR/bin/activate"
    pip install -r requirements.txt

    echo "[INFO] 啟動 app.py"
    nohup $VENV_DIR/bin/python "$APP_FILE" > app.log 2>&1 &

    echo "[INFO] 部署完成！"
    exit 0
fi

# ====================================
# 第二次以後更新：pull + 套件更新 + 重啟
# ====================================
echo "[INFO] 已存在專案：更新程式碼版本"

cd "$PROJECT_DIR" || exit
git pull

echo "[INFO] 啟動虛擬環境"
source "$VENV_DIR/bin/activate"

echo "[INFO] 安裝 requirements.txt 中缺少的依賴"
pip install -r requirements.txt

echo "[INFO] 重啟 app.py"
pkill -f "$APP_FILE"
nohup $VENV_DIR/bin/python "$APP_FILE" > app.log 2>&1 &

echo "[INFO] 更新完成！"
