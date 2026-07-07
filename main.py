import asyncio

from scanner.cli.application import CLI


def main():

    cli = CLI()

    asyncio.run(cli.run())


if __name__ == "__main__":
    main()