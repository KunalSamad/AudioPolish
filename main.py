from gui import NoiseReducerGUI
from processing import AudioProcessor

def main():
    processor = AudioProcessor()
    app = NoiseReducerGUI(processor)
    app.mainloop()

if __name__ == "__main__":
    main()
