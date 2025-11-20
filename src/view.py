from tkinter import (
    Tk,
    Toplevel,
    messagebox,
    ttk,
    filedialog,
    simpledialog,
)

from src.file_ops import DeviceFiles
from src.db_ops import DBDev, DBFileMovie


class View:
    def __init__(self, root: Tk) -> None:
        self.root = root
        self.root.title("Фильмотека")
        self.root.geometry("1200x800")
        self.root.grid_columnconfigure([0,1], weight=1)
        self.root.grid_rowconfigure([1,2], weight=1)

        self.tree_data = []

    def first_render(self) -> None:
        self.top_frame_render()
        self.left_frame_render()
        self.right_frame_render()
        self.status_bar_render()

    def top_frame_render(self):
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.grid(column=0, row=0, columnspan=2, sticky="nsw")
        self.top_frame.columnconfigure(0, weight=1)

        self.btn_scan_disk = ttk.Button(self.top_frame, text="Сканировать путь...")
        self.btn_match_empties = ttk.Button(
            self.top_frame, text="Сопоставить пустые файлы..."
        )

        self.btn_scan_disk.grid(column=0, row=0)
        self.btn_match_empties.grid(column=1, row=0)

    def left_frame_render(self):
        self.left_frame = ttk.Frame(self.root)
        self.left_frame.grid(column=0, row=1, sticky="NSEW")
        self.left_frame.columnconfigure([0,1], weight=1)
        self.left_frame.rowconfigure(0, weight=1)

        tree_columns = {
            "#0": {"label": "Имя", "name": "name", "stretch": True, "width": "400"},
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
            self.left_frame,
            columns=[v["name"] for v in tree_columns.values() if v["name"] != "name"],
        )
        for k, v in tree_columns.items():
            self.tree_view.column(k, stretch=v["stretch"], width=v["width"])
            self.tree_view.heading(k, text=v["label"])
        self.insert_items_in_tree()
        self.tree_view.grid(column=0, row=0, sticky="NSEW")
        # self.tree_view.grid_columnconfigure(2, weight=1)
        # self.tree_view.grid_rowconfigure(2, weight=1)

        self.tree_view_scrollbar_y = ttk.Scrollbar(
            master=self.left_frame, orient="vertical", command=self.tree_view.yview
        )
        self.tree_view_scrollbar_x = ttk.Scrollbar(
            master=self.left_frame, orient="horizontal", command=self.tree_view.xview
        )

        self.tree_view_scrollbar_y.grid(column=1, row=0, sticky="NSW")
        self.tree_view_scrollbar_x.grid(column=0, row=1, sticky="NEW")
        # self.tree_view_scrollbar_y.grid_columnconfigure(1, weight=1)
        # self.tree_view_scrollbar_y.grid_rowconfigure(1, weight=1)
        # self.tree_view_scrollbar_x.grid_columnconfigure(1, weight=1)
        # self.tree_view_scrollbar_x.grid_rowconfigure(1, weight=1)
        self.tree_view.configure(
            yscrollcommand=self.tree_view_scrollbar_y.set,
            xscrollcommand=self.tree_view_scrollbar_x.set,
        )

        self.l = ttk.Label(master=self.left_frame, text="---")
        self.l.grid(column=0, row=2)

        # self.tree_view.bind(
        #     "<<TreeviewSelect>>",
        #     lambda e: self.l.configure(text=self.tree_view.focus()),
        # )

    def insert_items_in_tree(self):
        for idx, disk in enumerate(self.tree_data, start=1):
            disk_name = disk.name
            if disk_name is None:
                disk_name = str(f"Диск id: {disk.id}")
            p = self.tree_view.insert(
                parent="", index=idx, iid=f"d{disk.id}", text=disk_name, open=True
            )
            for j, f in enumerate(disk.files, start=(idx * 1000)):
                if f.name_russian is not None:
                    text = f.name_russian
                elif f.name_original is not None:
                    text = f.name_original
                else:
                    text = f.file_name
                duration = f.duration if f.duration is not None else ""
                premiere_date = f.premiere_date if f.premiere_date is not None else ""
                c = self.tree_view.insert(
                    iid=f"f{f.file_id}",
                    parent=p,
                    index=j,
                    text=text,
                    values=[duration, premiere_date],
                )

    def right_frame_render(self):
        self.right_frame = ttk.Frame(self.root)
        self.right_frame.grid(column=1, row=1, sticky="nw")
        self.btn_match_file = ttk.Button(self.right_frame, text="Сопоставить")
        # self.btn_match_file.grid(column=0, row=3)
        # self.right_frame.columnconfigure(1, weight=1)

    def clear_frame(self, frame: ttk.Frame):
        for child in frame.winfo_children():
            child.destroy()

    def display_movie_frame(
        self, disk_dict: dict, file_dict: dict, movie_dict: dict | None, callback
    ):
        self.clear_frame(self.right_frame)
        self.lbl_device = ttk.Label(
            self.right_frame, text=f"Носитель: {disk_dict["disk_name"]}"
        )
        self.lbl_path = ttk.Label(
            self.right_frame, text=f"Путь: {file_dict["disk_path"]}"
        )
        self.lbl_file_name = ttk.Label(
            self.right_frame, text=f"Имя файла: {file_dict["file_name"]}"
        )

        self.lbl_device.grid(column=0, row=0, sticky="w")
        self.lbl_path.grid(column=0, row=1, sticky="w")
        self.lbl_file_name.grid(column=0, row=2, sticky="w")

        if movie_dict is not None:
            self.lbl_original_name = ttk.Label(
                self.right_frame,
                text=f"Оригинальное название: {movie_dict["name_original"]}",
            )
            self.lbl_russian_name = ttk.Label(
                self.right_frame, text=f"Русское название: {movie_dict["name_russian"]}"
            )
            self.lbl_duration = ttk.Label(
                self.right_frame, text=f"Продолжительность: {movie_dict["duration"]}"
            )
            self.lbl_year = ttk.Label(
                self.right_frame, text=f"Год премьеры: {movie_dict["premiere_date"]}"
            )
            self.lbl_genres = ttk.Label(self.right_frame, text="Жанры:")
            self.lbl_director = ttk.Label(self.right_frame, text="Режиссёр:")
            self.lbl_actors = ttk.Label(self.right_frame, text="В ролях:")

            self.lbl_original_name.grid(column=0, row=3, sticky="w")
            self.lbl_russian_name.grid(column=0, row=4, sticky="w")
            self.lbl_duration.grid(column=0, row=5, sticky="w")
            self.lbl_year.grid(column=0, row=6, sticky="w")
            self.lbl_genres.grid(column=0, row=7, sticky="w")
            self.lbl_director.grid(column=0, row=8, sticky="w")
            self.lbl_actors.grid(column=0, row=9, sticky="w")

        id = file_dict["id"]
        self.btn_match_file = ttk.Button(
            self.right_frame, text="Сопоставить", command=lambda: callback(id)
        )
        self.btn_match_file.grid(column=0, row=10, sticky="ws")

    def display_search_result(self, searched: dict):
        self.clear_frame(self.right_frame)
        if len(searched) == 0:
            self.lbl_warning = ttk.Label(
                self.right_frame,
                text="Ничего не найдено. Попробуйте изменить критерии поиска.",
            )
            self.lbl_warning.grid(column=0, row=0)
        else:
            self.lbl_warning = ttk.Label(
                self.right_frame,
                text="Найдены следующие вхождения.",
            )
            self.lbl_warning.grid(column=0, row=0)
            buttons = [ttk.Button(master=self.right_frame) for _ in range(len(searched))]
            i = 0
            for e in searched:
                buttons[i].config(text=f"{e["name"]} ({e["premiere_date"]})")
                buttons[i].grid(column=0, row=2 + i)
                i += 1


    def status_bar_render(self):
        pass

    def setup_callbacks(self, callbacks: dict) -> None:
        self.btn_scan_disk.config(command=callbacks["press_scan_dir_path"])
        self.btn_match_empties.config(command=callbacks["press_match_empties"])
        self.tree_view.bind(
            "<<TreeviewSelect>>",
            callbacks["tree_view_click"],
        )
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
        btn_path = ttk.Button(master=frame, text=path_name, command=lambda: path_name)
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

    def new_movie_name_request(self, title, prompt, init_val) -> str | None:
        new_name = simpledialog.askstring(
            title=title, prompt=prompt, initialvalue=init_val
        )
        return new_name
