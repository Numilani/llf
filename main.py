import asyncio
import sys
from blessed import Terminal
import types

log_lines = []
queue: asyncio.Queue = asyncio.Queue()


def write_line(text, ttyout):
    if sys.stdin.isatty():
        print(text)
    else:
        ttyout.write(text)
        ttyout.flush()


def prompt_input(ttyin=None, ttyout=None):
    if ttyin is None:
        i = input("Enter input: ")
        return i
    else:
        write_line("Enter input: ", ttyout)
        i = ttyin.readline().rstrip("\n")
        return i


async def read_lines():
    while True:
        line = await asyncio.to_thread(sys.stdin.readline)
        if line == "":
            return
        await queue.put(line)


def clear_log_printout(term, ttyout):
    print(term.home)
    for i in range(16):
        write_line(term.clear_eol, ttyout)
        write_line(term.move_down(1) + term.move_x(0), ttyout)


async def write_log(term, ttyout):
    while True:
        new_line = await queue.get()
        if new_line is None:
            return
        log_lines.append(new_line)
        clear_log_printout(term, ttyout)
        write_line(term.home, ttyout)
        for line in log_lines[-16:]:
            write_line(line, ttyout)


async def prompt_loop(term, ttyin, ttyout):
    while True:
        write_line(term.move_xy(0, term.height - 2), ttyout)
        user_input = await asyncio.to_thread(prompt_input, ttyin, ttyout)
        write_line(f"You entered: {user_input}", ttyout)


async def log_print_loop(term, ttyout):
    while True:
        if sys.stdin.isatty():
            # NOTE: add logic for non-pipe reading here later
            return
        else:
            read_task = asyncio.create_task(read_lines())
            write_task = asyncio.create_task(write_log(term, ttyout))
            await read_task
            await write_task


async def main():
    term = Terminal()
    print(term.home + term.clear)
    if sys.stdin.isatty():
        await asyncio.gather(prompt_loop(term, None, None), log_print_loop(term, None))
    else:
        ttyin = open("/dev/tty", "r")
        ttyout = open("/dev/tty", "w")
        await asyncio.gather(prompt_loop(term, ttyin, ttyout), log_print_loop(term, ttyout))


if __name__ == "__main__":
    asyncio.run(main())
