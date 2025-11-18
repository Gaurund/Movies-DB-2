from tkinter import (
    Toplevel,
    messagebox,
    ttk,
    filedialog,
    simpledialog,
)

from src.file_ops import DeviceFiles
from src.db_ops import DBDev, DBFileMovie


class View:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title("Фильмотека")
        self.root.geometry("1200x800")
        self.tree_data = []
        # self.first_render()

    def first_render(self) -> None:
        self.top_frame_render()
        self.left_frame_render()
        self.right_frame_render()
        self.status_bar_render()

    def top_frame_render(self):
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.grid(column=0, row=0, columnspan=2)

        self.btn_scan_disk = ttk.Button(self.top_frame, text="Сканировать путь...")
        self.btn_match_file = ttk.Button(self.top_frame, text="Сопоставить")

        self.btn_scan_disk.grid(column=0, row=0)
        self.btn_match_file.grid(column=1, row=0)

    def left_frame_render(self):
        self.left_frame = ttk.Frame(self.root)
        self.left_frame.grid(column=0, row=1)

        tree_columns = {
            "#0": {"label": "Имя", "name": "name", "stretch": True, "width": "300"},
            "#1": {
                "label": "Время",
                "name": "duration",
                "stretch": False,
                "width": "60",
            },
            "#2": {
                "label": "Год",
                "name": "premiere_date",
                "stretch": False,
                "width": "40",
            },
        }
        self.tree_view = ttk.Treeview(
            self.left_frame, columns=[v["name"] for v in tree_columns.values()]
        )
        for k, v in tree_columns.items():
            self.tree_view.column(k, stretch=v["stretch"], width=v["width"])
            self.tree_view.heading(k, text=v["label"])
        self.insert_items_in_tree()
        self.tree_view.grid(column=0, row=0)

    def insert_items_in_tree(self):
        for i, disk in enumerate(self.tree_data):
            disk_name = disk.name
            if disk_name is None:
                disk_name = str(f"Диск id: {disk.id}")
            p = self.tree_view.insert(parent="", index=i, text=disk_name, open=True)
            for j, f in enumerate(disk.files, start=(i * 1000)):
                if f.name_russian is not None:
                    text = f.name_russian
                elif f.name_original is not None:
                    text = f.name_original
                else:
                    text = f.file_name
                c = self.tree_view.insert(
                    parent=p,
                    index=j,
                    text=text,
                    values=[f.duration, f.premiere_date]
                )

    def right_frame_render(self):
        self.right_frame = ttk.Frame(self.root)
        self.right_frame.grid(column=1, row=1)

    def display_movie_frame(self):
        self.lbl_device = ttk.Label(self.right_frame, text="Носитель:")
        self.lbl_path = ttk.Label(self.right_frame, text="Путь:")
        self.lbl_file_name = ttk.Label(self.right_frame, text="Имя файла:")
        self.lbl_original_name = ttk.Label(
            self.right_frame, text="Оригинальное название:"
        )
        self.lbl_russian_name = ttk.Label(self.right_frame, text="Русское название:")
        self.lbl_year = ttk.Label(self.right_frame, text="Год премьеры:")
        self.lbl_genres = ttk.Label(self.right_frame, text="Жанры:")
        self.lbl_director = ttk.Label(self.right_frame, text="Режиссёр:")
        self.lbl_actors = ttk.Label(self.right_frame, text="В ролях:")

        self.lbl_device.grid(column=0, row=0, sticky="e")
        self.lbl_path.grid(column=0, row=1, sticky="e")
        self.lbl_file_name.grid(column=0, row=2, sticky="e")
        self.lbl_original_name.grid(column=0, row=3, sticky="e")
        self.lbl_russian_name.grid(column=0, row=4, sticky="e")
        self.lbl_year.grid(column=0, row=5, sticky="e")
        self.lbl_genres.grid(column=0, row=6, sticky="e")
        self.lbl_director.grid(column=0, row=7, sticky="e")
        self.lbl_actors.grid(column=0, row=8, sticky="e")

    def status_bar_render(self):
        pass

    def setup_callbacks(self, callbacks: dict) -> None:
        self.btn_scan_disk.config(command=callbacks["press_scan_dir_path"])
        self.btn_match_file.config(command=callbacks["press_match_file"])
        # self.get_tree_data = callbacks["get_tree_data"]

    def directory_request(self) -> str:
        dir_path = filedialog.askdirectory(initialdir="D:/TEMP/v")
        return dir_path

    def new_device_name_request(self, title, prompt) -> str | None:
        new_name = simpledialog.askstring(title=title, prompt=prompt)
        return new_name

    def display_message_box(self, message: str = "Успех.", default="ok", icon="info"):
        message_box = messagebox.Message(
            parent=self.root, default=default, message=message, icon=icon
        )
        message_box.show()

    def choose_name(self, path_name: str, file_name: str) -> str:
        print(path_name + "\\" + file_name)
        dialog = Toplevel(master=self.root)
        frame = ttk.Frame(master=dialog)
        btn_path = ttk.Button(master=frame, text=path_name)
        btn_file = ttk.Button(master=frame, text=file_name)

        dialog.grid()
        frame.grid()
        btn_path.grid(column=0, row=0)
        btn_file.grid(column=0, row=1)
        # Получить варианты имён и задать пользователю вопрос
        # какой из трёх вариантов выбрать для поиска:
        # имя папки
        # имя файла
        # свой вариант
        return ""
