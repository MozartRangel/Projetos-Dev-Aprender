import os
import shutil
import time
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class DownloadHandler(FileSystemEventHandler):
    TEMP_EXTENSIONS = {".crdownload", ".part", ".tmp"}

    def __init__(self, download_path):
        self.download_path = download_path

    def on_created(self, event):
        if event.is_directory:
            return

        self._handle_path(event.src_path)

    def on_moved(self, event):
        if event.is_directory:
            return

        self._handle_path(event.dest_path)

    def _handle_path(self, file_path):
        if self._is_temporary_download(file_path):
            return

        if not self._wait_until_ready(file_path):
            print(f"Arquivo nao ficou pronto a tempo: {file_path}")
            return

        self.move_file(file_path)

    def _is_temporary_download(self, file_path):
        return Path(file_path).suffix.lower() in self.TEMP_EXTENSIONS

    def _wait_until_ready(self, file_path, timeout=30, poll_interval=0.5):
        deadline = time.time() + timeout
        previous_size = -1

        while time.time() < deadline:
            if not os.path.exists(file_path):
                time.sleep(poll_interval)
                continue

            try:
                current_size = os.path.getsize(file_path)
            except OSError:
                time.sleep(poll_interval)
                continue

            if current_size > 0 and current_size == previous_size:
                return True

            previous_size = current_size
            time.sleep(poll_interval)

        return False

    def move_file(self, file_path):
        try:
            if not os.path.exists(file_path):
                return

            file_name = os.path.basename(file_path)
            file_ext = os.path.splitext(file_name)[1].lower().strip('.')

            if not file_ext:
                folder_name = "sem_extensao"
            else:
                folder_name = file_ext

            folder_path = os.path.join(self.download_path, folder_name)

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            dest_path = os.path.join(folder_path, file_name)

            # Adiciona número se arquivo já existe
            if os.path.exists(dest_path):
                name, ext = os.path.splitext(file_name)
                counter = 1
                while os.path.exists(os.path.join(folder_path, f"{name}_{counter}{ext}")):
                    counter += 1
                dest_path = os.path.join(folder_path, f"{name}_{counter}{ext}")

            shutil.move(file_path, dest_path)
            print(f"Movido: {file_name} -> {folder_name}/")
        except Exception as e:
            print(f"Erro ao mover arquivo: {e}")

    def organize_existing_files(self):
        for entry in os.scandir(self.download_path):
            if not entry.is_file():
                continue
            self._handle_path(entry.path)


class DownloadOrganizerTrayApp:
    def __init__(self, download_path):
        self.download_path = download_path
        self.event_handler = DownloadHandler(download_path)
        self.observer = None
        self.is_running = False
        self.current_status = "parado"

        self.root = tk.Tk()
        self.root.withdraw()
        self.root.title("Organizador de Downloads")

        self.status_window = tk.Toplevel(self.root)
        self.status_window.title("Organizador de Downloads")
        self.status_window.geometry("320x140")
        self.status_window.resizable(False, False)
        self.status_window.withdraw()
        self.status_window.protocol(
            "WM_DELETE_WINDOW", self.hide_status_window)

        self.status_var = tk.StringVar(value="Status: parado")

        label = tk.Label(self.status_window,
                         textvariable=self.status_var, font=("Segoe UI", 11))
        label.pack(pady=(20, 12))

        button_frame = tk.Frame(self.status_window)
        button_frame.pack()

        self.start_button = tk.Button(
            button_frame, text="Iniciar", width=12, command=self.start_monitoring)
        self.start_button.pack(side=tk.LEFT, padx=(0, 8))

        self.stop_button = tk.Button(
            button_frame, text="Parar", width=12, command=self.stop_monitoring)
        self.stop_button.pack(side=tk.LEFT)

        self.icon = pystray.Icon(
            "OrganizadorDownloads",
            self._create_tray_image(),
            "Organizador Downloads",
            menu=pystray.Menu(
                item("Abrir", self._menu_open_window, default=True),
                item("Parar", self._menu_stop_monitoring),
                item("Sair", self._menu_quit),
            ),
        )

    def _create_tray_image(self):
        image = Image.new("RGB", (64, 64), "#1f6feb")
        draw = ImageDraw.Draw(image)
        draw.rectangle((14, 12, 50, 52), fill="#ffffff")
        draw.rectangle((20, 18, 44, 24), fill="#1f6feb")
        draw.rectangle((20, 30, 44, 36), fill="#1f6feb")
        draw.rectangle((20, 42, 36, 48), fill="#1f6feb")
        return image

    def _update_status(self):
        self.status_var.set(f"Status: {self.current_status}")
        if self.is_running:
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
        else:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def start_monitoring(self):
        if self.is_running:
            return

        self.current_status = "trabalhando"
        self._update_status()
        self.event_handler.organize_existing_files()

        self.observer = Observer()
        self.observer.schedule(
            self.event_handler, self.download_path, recursive=False)
        self.observer.start()

        self.is_running = True
        self.current_status = "executando"
        self._update_status()
        print(f"Monitorando: {self.download_path}")

    def stop_monitoring(self):
        if not self.is_running:
            return

        self.observer.stop()
        self.observer.join()
        self.observer = None

        self.is_running = False
        self.current_status = "parado"
        self._update_status()
        print("Monitoramento parado")

    def show_status_window(self):
        self._update_status()
        self.status_window.deiconify()
        self.status_window.lift()
        self.status_window.focus_force()

    def hide_status_window(self):
        self.status_window.withdraw()

    def _menu_open_window(self, icon, menu_item):
        self.root.after(0, self.show_status_window)

    def _menu_stop_monitoring(self, icon, menu_item):
        self.root.after(0, self.stop_monitoring)

    def _menu_quit(self, icon, menu_item):
        self.root.after(0, self.quit)

    def quit(self):
        self.stop_monitoring()
        self.icon.stop()
        self.root.quit()

    def run(self):
        self.icon.run_detached()
        self.show_status_window()
        self.root.mainloop()


if __name__ == "__main__":
    download_path = str(Path.home() / "Downloads")
    app = DownloadOrganizerTrayApp(download_path)
    app.run()
