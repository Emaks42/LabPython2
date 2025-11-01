from src.bash_processor import BashProcessor
from constants import BASE_DIR_FOR_MAIN


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """

    print("Добро пожаловать в эмулятор bash, если хотите завершить процесс введите exit")
    bash_proc = BashProcessor(BASE_DIR_FOR_MAIN)
    while True:
        inp = input(bash_proc.get_current_directory() + ">")
        if inp.strip() == "exit":
            break
        print(bash_proc.command(inp), end="")


if __name__ == "__main__":
    main()
