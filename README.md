# AudioPolish
*AudioPolish* is an advanced audio processing tool designed for voiceover production and audio enhancement. It offers a comprehensive suite of operations—including noise reduction, echo reduction, reverb reduction, volume normalization, and volume compression—organized in a modular and expandable architecture. The tool supports both single-file and batch processing modes and features an intuitive GUI built with Tkinter, complete with real-time visualizations, a progress bar, and a detailed operation log.

# Features
- **Multiple Audio Enhancement Operations:**

  - Noise Reduction: Clean up background noise using spectral gating techniques.
  - Echo Reduction: Reduce unwanted echoes using adaptive filtering.
  - Reverb Reduction: Minimize room reverberation with state-of-the-art algorithms.
  - Volume Normalization: Normalize loudness using ITU BS.1770 standards (via pyloudnorm).
  - Volume Compression: Apply dynamic range compression to even out levels and enhance clarity.

- **Flexible Processing Modes:**
  - Single File Mode: Process individual audio files with visual feedback (waveform visualization before and after processing).
  - Batch Processing Mode: Process entire folders of audio files, with the output files retaining their original names.

- **User-Friendly GUI:**
  - Intuitive import/export and folder selection controls.
  - Scrollable log section that provides detailed status updates for each file and operation.
  - A progress bar that visually tracks processing progress.

- Modular Architecture:
  - Each processing operation is implemented as a separate module, making it easy to expand and integrate new features in the future.

# Why AudioPolish?
AudioPolish is tailored for professionals and enthusiasts who require high-quality audio enhancement without the need for complex, resource-intensive deep learning models. Whether you're cleaning up voiceovers, podcasts, or other recordings, AudioPolish provides a reliable, efficient, and scalable solution that adheres to industry best practices.

# Getting Started
**Prerequisites**
  - Python 3.11
  - The following Python libraries:
    - Tkinter (usually included with Python)
    - Matplotlib
    - pyloudnorm
    - pyroomacoustics
    - SoundFile
    - Others as specified in requirements.txt

**Installation**

**1. Clone the Repository:**
```bash
git clone https://github.com/yourusername/AudioPolish.git
cd AudioPolish
```
**2. Install Dependencies:**
```bash
pip install -r requirements.txt
```
**3. Run the Application:**
```bash
python main.py
```

# Usage
**1. Select Processing Mode:**
  - Choose Single File Mode to process one audio file at a time.
  - Choose Batch Processing Mode to process all audio files in a selected folder.

**2. Import/Export:**
  - In single file mode, import an audio file and set the output file.
  - In batch mode, select the input folder and output folder. Processed files will retain their original names.

**3. Select Operations:**

  - Check the boxes for the operations you want to apply. The operations will be applied in the following industry-standard order:
    1. Noise Reduction
    2. Echo Reduction
    3. Reverb Reduction
    4. Volume Normalization
    5. Volume Compression

 **4. Apply and Visualize:**
  - Click "Apply Selected Operations" to process the file(s).
  - In single file mode, both the original and processed waveforms are visualized.
  - The progress bar and log section provide real-time feedback on the processing status.

**5. Open Output Folder (Batch Mode):**
  - Use the "Open Output Folder" button to quickly view the processed files.

# Future Enhancements
- Additional Processing Operations:

  Easily add new audio enhancement features (e.g., multiband compression, advanced echo cancellation) thanks to the modular design.

- Enhanced Visualization:

  Integrate spectrogram or frequency-domain visualizations for more detailed audio analysis.

- Custom Presets:

  Allow users to save and load custom processing pipelines for different audio scenarios.

# Contributing
Contributions are welcome! Please feel free to submit issues, suggest improvements, or create pull requests to help expand AudioPolish.

# License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/KunalSamad/AudioPolish/blob/main/LICENSE.txt) file for details.
