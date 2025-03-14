import numpy as np
import pyloudnorm as pyln

def apply_volume_normalization(audio_data, sample_rate, target_lufs=-16.0):
    """
    Normalizes the volume of the audio signal to the target LUFS level using ITU BS.1770 standard.
    
    Parameters:
        audio_data (np.ndarray): 1D array of audio samples (range typically in [-1, 1]).
        sample_rate (int): Sampling rate of the audio.
        target_lufs (float): The target integrated loudness in LUFS (default is -16 LUFS for voiceovers).
    
    Returns:
        np.ndarray: Volume-normalized audio data.
    """
    # Create a loudness meter instance from pyloudnorm
    meter = pyln.Meter(sample_rate)
    
    # Measure the integrated loudness of the input audio
    loudness = meter.integrated_loudness(audio_data)
    
    # Calculate the gain required to reach the target loudness
    gain = target_lufs - loudness
    
    # Apply gain (convert dB gain to linear scaling)
    linear_gain = 10**(gain / 20)
    
    # Normalize audio
    normalized_audio = audio_data * linear_gain
    
    # Optionally, clip to ensure the signal remains in the valid range
    normalized_audio = np.clip(normalized_audio, -1, 1)
    return normalized_audio
