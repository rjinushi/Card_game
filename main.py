# title:
# author:
# desc:
# site:
# license:
# version: 0.0.0


from rich.traceback import install
install(show_locals=True)  # 例外発生時のローカル変数を表示


from src.App import App

if __name__ == "__main__":
    App()