import os
import time
from datetime import datetime
import subprocess

import ambient

if __name__ == '__main__':
    try:
        # 環境変数を読み込む
        CHANNEL_ID = int(os.environ['AMBIENT_CHANNEL_ID'])
        WRITE_KEY = os.environ['AMBIENT_WRITE_KEY']
    except KeyError as e:
        print('Missing environment variable: {}'.format(e))
        exit(1)

    # Ambientのクライアントを用意
    am = ambient.Ambient(CHANNEL_ID, WRITE_KEY)

    last_uploaded = datetime.now()
    while True:
        try:
            # コマンドの標準出力を受け取る
            proc = subprocess.run(
                ["./bin/2jcieev01-baro"],
                stdout = subprocess.PIPE, 
                stderr = subprocess.PIPE
                )
            out = proc.stdout.decode("utf8").strip()
            # 標準出力の文字列を分割して気圧と気温のデータを取得する
            # 例:
            # ['100154.6', '32.840', 'a463d4', '665d03', 'retun code: 0']
            data = list(map(lambda str: str.strip(), out.split(',')))

            # AmbientのAPI制限を回避するために60秒に1回の頻度でダータを送信
            timestamp = datetime.now()
            if (timestamp - last_uploaded).seconds > 60:
                am.send({
                    "d1": data[0],
                    "d2": data[1],
                    "created": timestamp.strftime("%Y/%m/%d %H:%M:%S")
                })
                print("Send to Ambient...")
                # タイマーをリセット
                last_uploaded = datetime.now()
            time.sleep(1)
        except KeyboardInterrupt:
            break
