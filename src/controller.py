from src.file_ops import get_dev_files, RealFile, Device, DeviceFiles
from src.db_ops import DB_connection
from src.view import View
from src.name_cleaner import name_cleaner


class Controller:
    def __init__(self, db_connection: DB_connection, view: View) -> None:
        self.conn = db_connection
        self.view = view

        tree_data = self.get_tree_data()
        self.view.tree_data = tree_data
        self.view.first_render()
        self.view.setup_callbacks(
            {
                "press_scan_dir_path": self.scan_dir_path,
                "press_match_file": self.match_file,
                "tree_view_click": self.tree_view_click,
            }
        )

    def scan_dir_path(self) -> None:
        """
        Scan the given path and populate DB.
        """
        dir_path = self.view.directory_request()
        if not dir_path == "":
            dev_files = get_dev_files(path_str=dir_path)
            if len(dev_files.files) == 0:
                self.view.display_message_box("По указанному пути нет видео файлов.")
            else:
                self.insert_files_in_db(dev_files)

    def insert_files_in_db(self, dev_files: DeviceFiles) -> None:
        """
        Populate DB with given files objects.
        """
        if self.is_dev_in_db(dev_files.device.st_dev) is None:
            new_name = self.get_new_device_name()
            self.conn.insert_disk(
                name=new_name,
                capacity=dev_files.device.capacity,
                free=dev_files.device.free,
                st_dev=dev_files.device.st_dev,
            )
        already_in_db = self.conn.insert_files(dev_files=dev_files)
        if len(already_in_db.files) == len(dev_files.files):
            message = (
                "По указанному пути все файлы уже были внесены в фильмотеку ранее."
            )
        else:
            message = "Путь успешно отсканирован. Файлы внесены в фильмотеку."
        self.view.display_message_box(message=message)

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

    def match_file(self):
        # Собрать в список все файлы из БД где нет файлов
        empties = self.conn.get_empties()
        # В цикле переберать файлы каждый раз предлагая завершить операцию
        for file in empties:
            # От файла нужно взять название папки и имя файла
            last_slash = file.disk_path.rindex("\\")
            path_name = file.disk_path[last_slash + 1 : :]
            # Очистить имя файла от всего лишнего
            file_name = name_cleaner(file.file_name)
            search_name = self.view.choose_name(path_name, file_name)
            # Получить имя для поиска обратно
        # Сформировать строку для поиска в IMDB
        # Получить список подходящих фильмов
        # Если список пустой, начать новый поиск с новым именем
        # Взять из списка подходящий фильм и открыв страницу, собрать все данные
        # Данные внести в БД
        print("Ждем")
        pass

    def get_tree_data(self):
        tree_data = self.conn.collect_tree_data()
        return tree_data

    def is_dev_in_db(self, st_dev: str) -> int | None:
        return self.conn.get_disk_by_stat(st_dev=st_dev)

    def is_dev_name_exists(self, name: str) -> bool:
        return self.conn.is_dev_name_exists(name)

    def tree_view_click(self, e):
        # Необходимо сделать обработку на тот случай если в фокусе не файл,
        # а диск
        # file_id = int(self.view.tree_view.focus())
        # file_dict = self.conn.get_file_by_id(file_id)
        selected: str = self.view.tree_view.focus()
        if "d" in selected:
            self.tree_view_disk_selected(selected)
        if "f" in selected:
            self.tree_view_file_selected(selected)


    def tree_view_disk_selected(self, iid: str):
        self.view.l.configure(text=iid)

    def tree_view_file_selected(self, iid: str):
        file_id = int(iid[1::])
        file_dict = self.conn.get_file_by_id(file_id)
        if file_dict is None:
            self.view.l.configure(text="Пусто", width=120) # Проработать возможность ошибки
            return
        disk_dict = self.conn.get_disk_dict_by_id(file_dict["disk_id"])
        if file_dict["movie_id"] is not None:
            movie_dict = self.conn.get_movie_by_id(file_dict["movie_id"])
        else:
            movie_dict = None
        self.view.display_movie_frame(disk_dict=disk_dict, file_dict=file_dict, movie_dict=movie_dict)
        # self.view.l.configure(text=file_dict, width=120) # 2 delete
        
