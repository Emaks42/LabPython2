from src.bash_processor import BashProcessor
from src.constants import BASE_DIR_FOR_MAIN


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """

    print("Добро пожаловать в эмулятор bash, если хотите завершить процесс введите exit")
    bash_proc = BashProcessor(BASE_DIR_FOR_MAIN)
    inp_fail = False
    while True:
        try:
            if not inp_fail:
                inp = input(bash_proc.get_current_directory() + " $ ")
            else:
                inp = input()
            if inp.strip() == "exit":
                break
            print(bash_proc.command(inp), end="")
            inp_fail = False
        except EOFError:
            inp_fail = True


if __name__ == "__main__":
    main()
