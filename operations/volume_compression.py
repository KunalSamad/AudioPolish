import numpy as np

def apply_volume_compression(audio_data, sample_rate, 
                             threshold_dB=-20.0, ratio=4.0, 
                             attack=0.01, release=0.1, knee=5.0):
    """
    Applies dynamic range compression to the audio signal.
    
    Parameters:
        audio_data (np.ndarray): 1D array of normalized audio samples (range [-1, 1]).
        sample_rate (int): Sampling rate of the audio.
        threshold_dB (float): Threshold in dB above which compression is applied (default: -20 dB).
        ratio (float): Compression ratio (default: 4:1).
        attack (float): Attack time in seconds (default: 0.01 s).
        release (float): Release time in seconds (default: 0.1 s).
        knee (float): Knee width in dB (default: 5 dB).
        
    Returns:
        np.ndarray: The compressed audio signal.
    """
    eps = 1e-8  # small constant to prevent log(0)
    output = np.zeros_like(audio_data)
    envelope = np.zeros_like(audio_data)
    gain = np.zeros_like(audio_data)
    
    # Time constant coefficients for smoothing (attack and release)
    alpha_attack = np.exp(-1.0 / (sample_rate * attack))
    alpha_release = np.exp(-1.0 / (sample_rate * release))
    
    env = 0.0  # initialize envelope
    
    for i, sample in enumerate(audio_data):
        rectified = abs(sample)
        # Apply attack or release smoothing based on whether the current rectified signal is rising or falling.
        if rectified > env:
            env = alpha_attack * env + (1 - alpha_attack) * rectified
        else:
            env = alpha_release * env + (1 - alpha_release) * rectified
        envelope[i] = env
        
        # Convert the envelope value to dB.
        level_dB = 20 * np.log10(env + eps)
        
        # Calculate gain reduction based on the level relative to threshold and knee.
        if level_dB < threshold_dB - knee / 2:
            # Below knee region: no compression.
            gain_dB = 0.0
        elif level_dB > threshold_dB + knee / 2:
            # Above knee region: full compression.
            gain_dB = threshold_dB - level_dB + (level_dB - threshold_dB) / ratio
        else:
            # Within the knee region: apply a smooth quadratic interpolation.
            delta = level_dB - (threshold_dB - knee / 2)
            gain_dB = -((1 / ratio - 1) * (delta ** 2) / (2 * knee))
        
        # Convert gain from dB to linear scale.
        current_gain = 10 ** (gain_dB / 20)
        gain[i] = current_gain
        
        # Apply the gain to the current sample.
        output[i] = sample * current_gain
    
    # Clip the output to ensure it stays within the normalized range [-1, 1].
    output = np.clip(output, -1, 1)
    return output
