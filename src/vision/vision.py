import os

from dotenv import load_dotenv, find_dotenv

def main():
    load_dotenv(find_dotenv())

    print(os.getenv("TOPIC"))


if __name__ == '__main__':
    main()