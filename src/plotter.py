import queue
import tkinter as tk
from src.config import config
from src.singleton import singleton


@singleton
class Plotter:
    def __init__(
            self,
            title,
    ):
        if not config.plotter.show:
            return

        self.queue = queue.Queue(maxsize=config.plotter.span)

        self.root = tk.Tk()
        self.root.title(title)

        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the dimensions and position for the first half of the screen
        window_width = screen_width // 2
        window_height = screen_height
        x_offset = 0
        y_offset = 0

        # Set the window size and position (width x height + x_offset + y_offset)
        self.root.geometry(f'{window_width}x{window_height}+{x_offset}+{y_offset}')

        self.figure = tk.Canvas(self.root, bg='white')
        self.figure.pack(fill=tk.BOTH, expand=True)

        self.update_plot()

    def update_plot(self):
        if not config.plotter.show:
            return

        self.figure.delete('all')

        width = self.figure.winfo_width()
        height = self.figure.winfo_height()

        if width > 1 and height > 1:
            padding = 10
            chart_width = width - 2 * padding
            chart_height = height - 2 * padding

            data = list(self.queue.queue)
            max_len = max(data) if data else 1
            points = []

            for i, length in enumerate(data):
                x = padding + i * chart_width / (config.plotter.span - 1)
                y = height - (padding + length * chart_height / max_len)
                points.append(x)
                points.append(y)

            if len(points) > 2:
                self.figure.create_line(points, fill='black', smooth=True, width=2)

            # Draw axes
            self.figure.create_line(padding, height - padding, width - padding, height - padding, fill='black')
            self.figure.create_line(padding, height - padding, padding, padding, fill='black')

        self.root.after(int(1000 / config.camera.fps), self.update_plot)

    def start(self):
        if not config.plotter.show:
            return

        self.root.mainloop()

    def update(self, item):
        if not config.plotter.show:
            return

        if self.queue.full():
            # Remove oldest item if queue is full
            self.queue.get_nowait()
        self.queue.put(item)


plotter = Plotter(
    title='Real-Time Frame Lengths',
)
