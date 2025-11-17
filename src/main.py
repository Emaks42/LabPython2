from src.bash_processor import BashProcessor
from src.constants import BASE_DIR_FOR_MAIN
from flask import Flask

app = Flask(__name__)
bash_proc = BashProcessor(BASE_DIR_FOR_MAIN)


@app.route('/')
def home():
    return bash_proc.command("ls /app")


def main() -> None:
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == "__main__":
    main()
