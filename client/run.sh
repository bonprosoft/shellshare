#!/bin/bash

# ===========
# 引数チェック
# ===========
if [ $# -ne 1 ]; then
    echo -e "Usage\n ./run.sh [UserName]" 1>&2
    exit 1
fi
USERNAME=$1

BASEDIR=`dirname $0`
BASEDIR=`(cd "$BASEDIR"; pwd)`


# 不要なら外してください
source env/bin/activate

# ========
# 環境設定
# ========
SESSION_NAME=recorded_session
INITIAL_WINDOW_NAME=recorded_pane
LOGFILE_NAME=shellshare_log.$$
## 2015-10/21/161919.logみたいな感じで残しておきたいなら以下の設定で上書きしてください
#LOGFILE_NAME=$(date +%Y-%m/%d/%H%M%S.log)
BINDIR=$BASEDIR/bin
LOGDIR=$BASEDIR/tmp
## もしhomeとかに残しておきたいなら以下の設定で上書きしてください
#LOGDIR=$HOME/.shellsharelog
LOG_PATH=$LOGDIR/$LOGFILE_NAME
OBSERVER_PATH=$BINDIR/observer.py
OBSERVER_INTERVAL=500


# ログディレクトリのチェック
if [ ! -d "$LOGDIR" ]; then
    mkdir "$LOGDIR"
fi
# ログファイルを上書きしたくない場合はコメントアウトしてください
echo > $LOG_PATH
echo $LOG_PATH

# 監視プロセスの起動
python $OBSERVER_PATH $LOG_PATH $OBSERVER_INTERVAL $USERNAME &
PID=$!
echo "[$(date +%Y-%m-%d_%H\:%M\:%S)]* Observer process started (pid: $PID)"

# tmuxプロセスのスタート
tmux start-server
echo "[$(date +%Y-%m-%d_%H\:%M\:%S)]* tmux server started."
tmux new-session  -n $INITIAL_WINDOW_NAME -s $SESSION_NAME \; pipe-pane -t $INITIAL_WINDOW_NAME "cat > $LOG_PATH"
echo "[$(date +%Y-%m-%d_%H\:%M\:%S)]* tmux server stopped."

# 監視プロセスの終了
echo "[$(date +%Y-%m-%d_%H\:%M\:%S)]* Send kill signal to observer process.(pid: $PID)"
kill -9 $PID

rm $LOG_PATH

