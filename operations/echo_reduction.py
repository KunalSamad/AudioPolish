import numpy as np
import pyroomacoustics as pra

def apply_echo_reduction(audio_data, sample_rate, filter_length=1024, mu=0.01, delay_ms=50):
    """
    Applies echo cancellation using an NLMS adaptive filter from Pyroomacoustics.
    
    This implementation uses a delayed version of the audio as a proxy for the far-end signal.
    It adapts an NLMS filter to cancel the echo.
    
    Parameters:
        audio_data (np.ndarray): 1D array of normalized audio samples (range [-1, 1]).
        sample_rate (int): Sample rate of the audio.
        filter_length (int): Length of the adaptive filter (default: 1024 samples).
        mu (float): Step size for the NLMS algorithm (default: 0.01).
        delay_ms (float): Estimated echo delay in milliseconds (default: 50 ms).
    
    Returns:
        np.ndarray: The echo-reduced audio signal.
    """
    # Calculate delay in samples.
    delay_samples = int(sample_rate * delay_ms / 1000)
    
    # Create a proxy far-end signal: a delayed version of the audio.
    # This is a simplification when no separate far-end reference is available.
    far_end = np.concatenate((np.zeros(delay_samples), audio_data[:-delay_samples]))
    
    # Initialize the NLMS adaptive filter from Pyroomacoustics.
    nlms = pra.adaptive.NLMS(filter_length, mu=mu)
    
    N = len(audio_data)
    y = np.zeros(N)  # Filter output
    e = np.zeros(N)  # Error signal (echo-cancelled output)
    x_buffer = np.zeros(filter_length)  # Input buffer for the filter
    
    # Process each sample.
    for n in range(N):
        # Update the input buffer with the current far-end sample.
        x_buffer = np.roll(x_buffer, 1)
        x_buffer[0] = far_end[n]
        
        # Compute filter output (estimated echo).
        y[n] = np.dot(nlms.w, x_buffer)
        
        # Compute error signal (desired minus estimated echo).
        e[n] = audio_data[n] - y[n]
        
        # Adapt the filter weights based on the error.
        nlms.adapt(x_buffer, e[n])
    
    # Clip the output to maintain the normalized range.
    return np.clip(e, -1, 1)
