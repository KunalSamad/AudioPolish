import sys
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore
import soundfile as sf

class AudioVisualizer(QtWidgets.QMainWindow):
    def __init__(self, audio_file, chunk_size=1024, update_interval=100):
        """
        Initializes the real-time audio visualizer.
        
        Parameters:
            audio_file (str): Path to the audio file to visualize.
            chunk_size (int): Number of samples to update per timer tick.
            update_interval (int): Update interval in milliseconds.
        """
        super().__init__()
        self.setWindowTitle("Real-time Audio Visualization")
        
        # Create a PlotWidget for visualization.
        self.plot_widget = pg.PlotWidget()
        self.setCentralWidget(self.plot_widget)
        self.plot_widget.setYRange(-1, 1)
        self.plot = self.plot_widget.plot()
        
        # Load the audio file.
        self.audio_data, self.sample_rate = sf.read(audio_file)
        if self.audio_data.ndim > 1:
            self.audio_data = self.audio_data[:, 0]
        if self.audio_data.size == 0:
            raise ValueError("Audio data is empty.")
        
        print("Audio length in samples:", len(self.audio_data))
        
        self.chunk_size = chunk_size
        self.ptr = 0
        
        # Setup a timer to update the plot.
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(update_interval)

    def update_plot(self):
        """
        Updates the plot with the next chunk of audio data.
        """
        if self.ptr < len(self.audio_data):
            # Get the next chunk of samples.
            chunk = self.audio_data[self.ptr:self.ptr+self.chunk_size]
            # Update the plot.
            self.plot.setData(chunk)
            self.ptr += self.chunk_size
            print("Pointer:", self.ptr)  # Debug print
        else:
            self.timer.stop()
            print("Visualization finished.")

def main():
    app = QtWidgets.QApplication(sys.argv)
    # Make sure to update this path to point to an existing audio file.
    audio_file = "your_audio_file.wav"
    visualizer = AudioVisualizer(audio_file)
    visualizer.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
