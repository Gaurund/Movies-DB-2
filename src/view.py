from tkinter import (
    messagebox,
    ttk,
    filedialog,
    simpledialog,
)

from src.file_ops import DeviceFiles


class View:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title("Фильмотека")
        self.root.geometry("1200x800")
        # self.root.grid(column=0, row=0)

        self.top_frame_render()
        self.left_frame_render()
        self.right_frame_render()
        self.status_bar_render()

    def top_frame_render(self):
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.grid(column=0, row=0, columnspan=2)

        self.btn_scan_disk = ttk.Button(self.top_frame, text="Сканировать путь...")
        self.btn_scan_disk.grid(column=0, row=0)

        self.btn_ok_msg = ttk.Button(self.top_frame, text="TEST")
        self.btn_ok_msg.grid(column=1, row=0)

    def left_frame_render(self):
        self.left_frame = ttk.Frame(self.root)

        self.left_frame.grid(column=0, row=1)

        self.label_left = ttk.Label(self.left_frame, text="LEFT")

        self.label_left.grid(column=0, row=0)

    def right_frame_render(self):
        self.right_frame = ttk.Frame(self.root)
        self.right_frame.grid(column=1, row=1)

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
        self.btn_ok_msg.config(command=callbacks["press_ok"])

    def directory_request(self) -> str:
        dir_path = filedialog.askdirectory(initialdir="D:/TMP/0")
        return dir_path

    def new_device_name_request(self, title, prompt) -> str | None:
        new_name = simpledialog.askstring(title=title, prompt=prompt)
        return new_name

    def show_repeated_files(self, alread_in_db: DeviceFiles):
        pass

    def show_ok(self, message: str = "Успех."):
        message_box = messagebox.Message(
            parent=self.root, default="ok", message=message, icon="info"
        )
        message_box.show()
