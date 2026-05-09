import asyncio
import sys
from blessed import Terminal
from prompt_toolkit.input import create_input
from prompt_toolkit.output import create_output
from prompt_toolkit import PromptSession


async def ui_loop(term):
    tty_input = create_input(open("/dev/tty", "r"))
    tty_output = create_output(open("/dev/tty", "w"))
    session = PromptSession(input=tty_input, output=tty_output)
    while True:
        if sys.stdin.isatty():
            user_input = await asyncio.to_thread(prompt_input)
            print(f"You entered: {user_input}")
        else:
            user_input = await session.prompt_async("Enter input(notty): ")
            print(f"You entered: {user_input}")


async def tty_loop(term):
    while True:
        if not sys.stdin.isatty():
            await asyncio.to_thread(read_lines)
        else:
            return


def prompt_input():
    i = input("Enter input: ")
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
