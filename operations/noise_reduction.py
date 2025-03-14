import noisereduce as nr

def apply_noise_reduction(audio_data, sample_rate):
    """
    Applies noise reduction using the noisereduce library.
    
    Parameters:
        audio_data (np.ndarray): Normalized audio samples in the range [-1, 1].
        sample_rate (int): Sample rate of the audio.
    
    Returns:
        np.ndarray: Processed (noise-reduced) audio data.
    """
    return nr.reduce_noise(y=audio_data, sr=sample_rate)
