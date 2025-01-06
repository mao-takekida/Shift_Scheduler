import subprocess

import flet as ft


def main(page: ft.Page):
    streamlit_process = None

    def start_streamlit(e):
        nonlocal streamlit_process
        if streamlit_process is None or streamlit_process.poll() is not None:
            # Streamlit を起動 (ブラウザを開かない設定)
            streamlit_process = subprocess.Popen(
                [
                    "streamlit",
                    "run",
                    "src/gui/utils/table_editor.py",
                    "--server.headless=true",  # ブラウザを開かない設定
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            page.add(ft.Text("Streamlit を起動しました。ブラウザは開きません。"))
        else:
            page.add(ft.Text("Streamlit はすでに起動中です。"))

    def stop_streamlit(e):
        nonlocal streamlit_process
        if streamlit_process is not None and streamlit_process.poll() is None:
            # Streamlit プロセスを終了
            streamlit_process.terminate()
            streamlit_process.wait()
            page.add(ft.Text("Streamlit を終了しました。"))
        else:
            page.add(ft.Text("Streamlit は起動していません。"))

    def on_close(e):
        # Flet アプリ終了時に Streamlit プロセスを停止
        if streamlit_process is not None and streamlit_process.poll() is None:
            streamlit_process.terminate()
            streamlit_process.wait()

    # ボタンとレイアウトの追加
    page.title = "Flet と Streamlit の連携 (ブラウザなし)"
    page.on_disconnect = on_close  # アプリ終了時の処理
    page.add(ft.ElevatedButton("Streamlit を起動", on_click=start_streamlit))
    page.add(ft.ElevatedButton("Streamlit を終了", on_click=stop_streamlit))


ft.app(target=main)
