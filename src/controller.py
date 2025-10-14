from src.file_ops import get_dev_files, RealFile, Device, DeviceFiles
from src.db_ops import DB_connection
from src.view import View


class Controller:
    def __init__(self, db_connection: DB_connection, view: View) -> None:
        self.conn = db_connection
        self.view = view

        self.view.setup_callbacks(
            {
                "press_scan_dir_path": self.scan_dir_path,
                "press_ok": self.show_ok,  # Только для теста
            }
        )

    def show_ok(self):
        self.view.show_message_box()

    def scan_dir_path(self) -> None:
        dir_path = self.view.directory_request()
        if not dir_path == "":
            # Нужная обработка на случай отмены
            dev_files = get_dev_files(path_str=dir_path)
            if len(dev_files.files) == 0:
                self.view.show_message_box("По указанному пути нет видео файлов.")
            else:
                self.insert_files_in_db(dev_files)

    def insert_files_in_db(self, dev_files: DeviceFiles) -> None:
        if self.is_dev_in_db(dev_files.device.st_dev) is None:
            new_name = self.get_new_device_name()
            self.conn.insert_disk(
                name=new_name,
                capacity=dev_files.device.capacity,
                free=dev_files.device.free,
                st_dev=dev_files.device.st_dev,
            )
        already_in_db = self.conn.insert_files(dev_files=dev_files)
        if len(already_in_db.files) == 0:
            message = "Путь успешно отсканирован. Файлы внесены в фильмотеку."

        elif len(already_in_db.files) == len(dev_files.files):
            message = (
                "По указанному пути все файлы уже были внесены в фильмотеку ранее."
            )

        else:
            message = "Следующие файлы уже были в базе данных:\n"
            for i, file in enumerate(already_in_db.files):
                message += "\n" + file.name
                if i == 10:
                    message += "\n..."
                    break
        self.view.show_message_box(message=message)

    def get_new_device_name(self) -> str:
        title = "Обнаружен новый диск"
        prompt = "Введите название для диска: "
        while True:
            name = self.view.new_device_name_request(title=title, prompt=prompt)
            if not name:
                title = "Название обязательно"
                prompt = "Пожалуйста, введите название для нового диска: "
            elif self.is_dev_name_exists(name):
                title = "Обнаружено совпадение"
                prompt = "Такое имя уже есть в базе данных. Пожалуйста, введите другое название для нового диска: "
            else:
                return name

    def is_dev_in_db(self, st_dev: str) -> int | None:
        return self.conn.get_disk_by_stat(st_dev=st_dev)

    def is_dev_name_exists(self, name: str) -> bool:
        return self.conn.is_dev_name_exists(name)
