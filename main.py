import sys
import subprocess
import io
import tempfile
import os
import selectors

from llfApp import llfApp


def run() -> None:
    if len(sys.argv) != 2 and sys.stdin.isatty():
        print("need file (and better error msgs)")
        exit()
    if sys.stdin.isatty():
        app = llfApp(sys.argv[1])
        app.run()
    else:
        # credit to Textualize/toolong and will mcgugan on GH for this solution
        with tempfile.NamedTemporaryFile(
            mode="w+b", buffering=0, prefix="pipe_out_"
        ) as temp_file:
            with open("/dev/tty", "rb", buffering=0) as tty_stdin:
                with subprocess.Popen(
                    ["python", sys.argv[0], temp_file.name],
                    stdin=tty_stdin,
                    close_fds=True,
                    env={**os.environ, "TEXTUAL_ALLOW_SIGNALS": "1"},
                ) as process:  # spawn the REAL process, reading from /dev/tty
                    selector = selectors.SelectSelector()
                    selector.register(sys.stdin.fileno(), selectors.EVENT_READ)

                    while process.poll() is None:  # while the process is still running
                        for _, event in selector.select(0.1):  # check every 100ms
                            if process.poll() is not None:  # if process end, close
                                break
                            if event & selectors.EVENT_READ:
                                if line := os.read(sys.stdin.fileno(), 1024 * 64):
                                    temp_file.write(line)  # forward stdin to tempfile
                                else:
                                    break


if __name__ == "__main__":
    run()
