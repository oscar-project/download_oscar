import subprocess
import threading

import PySimpleGUI as sg

# oriented this gui on the example at:
# https://raw.githubusercontent.com/PySimpleGUI/PySimpleGUI/069d1d08dc7ec19a8c59d5c13f3b8d60115c286b/UserCreatedPrograms/jumpcutter/jumpcutter_gui.py


def main():
    layout = [
        [sg.Text("Download OSCAR Corpus", font="Any 20")],
        [
            sg.Text(
                "Username:",
                size=(40, 1),
                justification="l",
                tooltip="the username for login",
            ),
            sg.Input(
                default_text="",
                key="user",
                size=(40, 1),
                tooltip="the username for login",
            ),
        ],
        [
            sg.Text(
                "Password:",
                size=(40, 1),
                justification="l",
                tooltip="the password for login",
            ),
            sg.Input(
                default_text="",
                key="password",
                size=(40, 1),
                tooltip="the password for login",
                password_char="*",
            ),
        ],
        [
            sg.Text(
                "Url:",
                size=(40, 1),
                justification="l",
                tooltip="the url to download files from",
            ),
            sg.Input(
                default_text="",
                key="base_url",
                size=(40, 1),
                tooltip="the url to download files from",
            ),
        ],
        [
            sg.Text(
                "Download folder:",
                size=(40, 1),
                justification="l",
                tooltip="the folder where files should be downloaded to",
            ),
            sg.Input(
                key="out",
                size=(40, 1),
                tooltip="the folder where files should be downloaded to",
            ),
            sg.FolderBrowse(),
        ],
        [
            sg.Text(
                "Chunk size:",
                size=(40, 1),
                justification="l",
                tooltip="the url to download files from",
            ),
            sg.Input(
                default_text="4096",
                key="chunk_size",
                size=(40, 1),
                tooltip="specifies in which chunks downloads are to be processed",
                enable_events=True,
            ),
        ],
        [sg.Text("Constructed Command Line:")],
        [
            sg.Text(
                size=(80, 3),
                key="cmd",
                text_color="yellow",
                font="Courier 8",
            )
        ],
        [
            sg.MLine(
                size=(80, 10),
                reroute_stdout=True,
                reroute_stderr=True,
                reroute_cprint=True,
                write_only=True,
                font="Courier 8",
                autoscroll=True,
                key="mline",
                auto_refresh=True,
            )
        ],
        [sg.Button("Start"), sg.Button("Exit")],
    ]
    window = sg.Window("Download OSCAR Corpus", layout, finalize=True)
    event_loop(window)


def event_loop(window):
    proc = None
    t_read = None
    try:
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Exit"):
                break
            if event == "chunk_size" and values["chunk_size"]:
                validate_int(window, "chunk_size", values)
            if event == "Start":
                user, password, base_url, out, _, chunk_size = values.values()
                command = f"dodc --user={user} --password={password} --base_url={base_url} --chunk_size={chunk_size} --out={out}"
                window["cmd"].update(command)
                window.refresh()
                proc = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                t_read = threading.Thread(target=read_stdout, args=(proc, window))
                t_read.start()
    finally:
        window.close()
        if proc is not None:
            proc.terminate()
    if t_read is not None:
        t_read.join()


def read_stdout(proc, window):
    for line in proc.stdout:
        print(line.decode().strip())
        window.refresh()


def validate_int(window, key, values):
    try:
        int(values[key])
    except Exception:
        sg.popup("Only integer values allowed.")
        window[key].update(values[key][:-1])


if __name__ == "__main__":
    main()
