class View:
    def __init__(self, controller, logger) -> None:
        self.controller = controller
        self.log = logger

    def main(self) -> None:
        # while True:
            self.greetings()
            choice: str = self.user_input("Введите номер пункта: ")
            match choice:
                case "1":
                    print("Вы выбрали сканировать путь...")
                    self.scan_path()
                case "2":
                    print("Вы выбрали просмотр")
                    self.show_movies()

    def greetings(self) -> None:
        msg = """* Домашная фильмотека *
1. Сканировать путь.
2. Просмотреть
"""
        print(msg)

    def user_input(self, msg: str) -> str:
        choice = input(msg)
        return choice

    def scan_path(self) -> None:
        init_path: str = self.user_input("Введите путь для сканирования: ")
        if not self.controller.check_disk(init_path):
            print("Данный диск отсутствует в базе данных. ")
            disk_name: str = input("Введите имя для данного диска: ")
            self.controller.insert_disk(init_path, disk_name)
        try:
            self.controller.store_movies_from_path(init_path)
        except Exception as e:
            # print(e,"В данном месте нет файлов с видео.")
            self.log.logger.debug(e)

    def show_movies(self) -> None:
        files = self.controller.get_db_files()
        for disk in files:
            print(f"Диск: {files[disk]["disk_name"]}:")
            for f in files[disk]["files"]:
                print(f" << {files[disk]["files"][f]["file_name"]} >> ", end="\t")

