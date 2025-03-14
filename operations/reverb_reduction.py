import numpy as np
import librosa
from nara_wpe.wpe import wpe

def apply_reverb_reduction(audio_data, sample_rate, n_fft=512, hop_length=128, iterations=3):
    """
    Applies Weighted Prediction Error (WPE) dereverberation to reduce reverberation.

    Parameters:
        audio_data (np.ndarray): 1D array of time-domain audio samples normalized to [-1, 1].
        sample_rate (int): The sample rate of the audio.
        n_fft (int): FFT size for STFT computation (default: 512).
        hop_length (int): Hop length for STFT computation (default: 128).
        iterations (int): Number of WPE iterations (default: 3).

    Returns:
        np.ndarray: Dereverberated audio in the time domain.
    """
    # Compute the STFT of the audio
    stft_audio = librosa.stft(audio_data, n_fft=n_fft, hop_length=hop_length)
    
    # Apply the WPE algorithm
    # The function wpe takes a complex STFT matrix and returns a dereverberated version.
    dereverb_stft = wpe(stft_audio, iterations=iterations)
    
    # Convert the dereverberated STFT back to time-domain audio
    audio_dereverb = librosa.istft(dereverb_stft, hop_length=hop_length, length=len(audio_data))
    return audio_dereverb
