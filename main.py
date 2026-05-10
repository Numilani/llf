import asyncio
import sys
from blessed import Terminal
import types

log_lines = []
queue: asyncio.Queue = asyncio.Queue()

async def ui_loop(term, ttyin, ttyout):
    while True:
        if sys.stdin.isatty():
            user_input = await asyncio.to_thread(prompt_input)
            print(f"You entered: {user_input}")
        else:
            user_input = await asyncio.to_thread(prompt_input, ttyin, ttyout)
            # user_input = await session.prompt_async("Enter input(notty): ")
            ttyout.write(f"You entered: {user_input}")
            ttyout.flush()


async def tty_loop(term, ttyout):
    while True:
        if not sys.stdin.isatty():
            read_task = asyncio.create_task(read_lines())
            # await read_lines(ttyout)
            # await asyncio.to_thread(read_lines)
            # await write_log(ttyout)
            write_task = asyncio.create_task(write_log(ttyout))
            await read_task
            await write_task
        else:
            return


def prompt_input(ttyin=None, ttyout=None):
    if ttyin is None:
        i = input("Enter input: ")
        return i
    else:
        ttyout.write("Enter input (ttyfile): ")
        ttyout.flush()
        i = ttyin.readline().rstrip("\n")
        return i


async def read_lines():
    while True:
        line = await asyncio.to_thread(sys.stdin.readline)
        if line == "":
            return
        await queue.put(line)


async def write_log(ttyout):
    while True:
        new_line = await queue.get()
        if new_line is None:
            return
        log_lines.append(new_line)
        for line in log_lines[-16:]:
            ttyout.write(line)
            ttyout.flush()


async def main():
    term = Terminal()
    ttyin = open("/dev/tty", "r")
    ttyout = open("/dev/tty", "w")

    await asyncio.gather(ui_loop(term, ttyin, ttyout), tty_loop(term, ttyout))


if __name__ == "__main__":
    asyncio.run(main())
