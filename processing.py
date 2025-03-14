import numpy as np
import soundfile as sf
from pydub import AudioSegment
from operations.noise_reduction import apply_noise_reduction

class AudioProcessor:
    def __init__(self):
        self.audio_data = None
        self.sample_rate = None

    def load_audio(self, filepath):
        """
        Loads an audio file (any format via pydub), converts it to mono,
        and normalizes the samples to [-1, 1].
        """
        audio = AudioSegment.from_file(filepath)
        audio = audio.set_channels(1)  # Force mono
        data = np.array(audio.get_array_of_samples()).astype(np.float32)
        self.audio_data = data / (2**15)
        self.sample_rate = audio.frame_rate

    def save_audio(self, filepath):
        """
        Saves the current audio_data as a 16-bit PCM WAV file.
        """
        if self.audio_data is None:
            raise ValueError("No audio loaded to save.")
        out_data = (self.audio_data * (2**15)).astype(np.int16)
        sf.write(filepath, out_data, self.sample_rate)

    def process_operation(self, operation):
        """
        Processes the audio data with the specified operation.
        For now, only 'Noise Reduction' is implemented.
        """
        if self.audio_data is None:
            raise ValueError("No audio loaded for processing.")
        if operation == "Noise Reduction":
            self.audio_data = apply_noise_reduction(self.audio_data, self.sample_rate)
        # Future operations (e.g., echo reduction) can be added here.
