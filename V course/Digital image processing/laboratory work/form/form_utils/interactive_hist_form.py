from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class HistogramCanvas(FigureCanvas):
    def __init__(self, hist_data: dict, parent=None):
        fig = Figure(figsize=(6, 4))
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

        self.hist_data = hist_data
        self._draw_hist()
        self._connect_hover()

    def _draw_hist(self):
        xs = sorted(self.hist_data.keys())
        ys = [self.hist_data[x] for x in xs]

        self.bars = self.ax.bar(xs, ys, width=1)
        self.ax.set_title("Гистограмма амплитуд")
        self.ax.set_xlabel("Амплитуда")
        self.ax.set_ylabel("Частота")

        self.draw()

    def _connect_hover(self):
        self.annot = self.ax.annotate(
            "",
            xy=(0, 0),
            xytext=(10, 10),
            textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->"),
        )
        self.annot.set_visible(False)

        self.mpl_connect("motion_notify_event", self._on_hover)

    def _on_hover(self, event):
        vis = self.annot.get_visible()
        if event.inaxes == self.ax:
            for bar in self.bars:
                if bar.contains(event)[0]:
                    x = bar.get_x()
                    y = bar.get_height()
                    self.annot.xy = (x, y)
                    self.annot.set_text(f"A={int(x)}\nP={y:.4f}")
                    self.annot.set_visible(True)
                    self.draw_idle()
                    return
        if vis:
            self.annot.set_visible(False)
            self.draw_idle()
