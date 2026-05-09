import asyncio
import sys
from blessed import Terminal


async def ui_loop(term):
    while True:
        if sys.stdin.isatty():
            user_input = await asyncio.to_thread(prompt_input)
            print(f"You entered: {user_input}")
        else:
            ttyin = open("/dev/tty", "r")
            ttyout = open("/dev/tty", "w")
            user_input = await asyncio.to_thread(prompt_input, ttyin, ttyout)
            # user_input = await session.prompt_async("Enter input(notty): ")
            print(f"You entered: {user_input}")


async def tty_loop(term):
    while True:
        if not sys.stdin.isatty():
            await asyncio.to_thread(read_lines)
        else:
            return


def prompt_input(ttyin=None, ttyout=None):
    if ttyin is None:
        i = input("Enter input: ")
        return i
    else:
        with ttyin, ttyout:
            ttyout.write("Enter input (ttyfile): ")
            ttyout.flush()
            i = ttyin.readline().rstrip("\n")
            return i


def read_lines():
    for line in sys.stdin:
        print(line)


async def main():
    term = Terminal()

    await asyncio.gather(
        ui_loop(term),
        tty_loop(term)
    )

if __name__ == "__main__":
    asyncio.run(main())
