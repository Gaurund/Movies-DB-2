from tkinter import (
    StringVar,
    Toplevel,
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
        self.btn_match_file = ttk.Button(self.top_frame, text="Сопоставить")

        self.btn_scan_disk.grid(column=0, row=0)
        self.btn_match_file.grid(column=1, row=0)

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
        self.btn_match_file.config(command=callbacks["press_match_file"])

    def directory_request(self) -> str:
        dir_path = filedialog.askdirectory(initialdir="D:/TEMP/v")
        return dir_path

    def new_device_name_request(self, title: str, prompt: str, command) -> None:
        def push_it():
            new_name = self.input.get()
            command(new_name)
        
        self.clear_frame(frame=self.right_frame)
        self.right_frame.grid(column=1, row=1)
        self.label_title = ttk.Label(self.right_frame, text=title)
        self.label_prompt = ttk.Label(self.right_frame, text=prompt)

        self.input = StringVar()
        self.entry_prompt = ttk.Entry(
            self.right_frame, textvariable=self.input, width=40
        )

        self.btn_enter = ttk.Button(self.right_frame, command=push_it, text="Ввод")

        self.label_title.grid(column=0, row=0)
        self.label_prompt.grid(column=0, row=1)
        self.entry_prompt.grid(column=0, row=2)
        self.btn_enter.grid(column=0, row=3)

    def show_message_box(self, message: str = "Успех.", default="ok", icon="info"):
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

    def clear_frame(self, frame: ttk.Frame) -> None:
        """
        Clears the given frame by destroying all child widgets.
        """
        for child in frame.winfo_children():
            child.destroy()
