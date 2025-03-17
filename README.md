# Audio Splitter

A Python script that splits audio files into segments based on silence detection.

## Features

- Split audio files based on silence detection
- Customizable silence length and threshold
- Progress bar visualization
- Error handling and user-friendly interface

## Requirements

- Python 3.x
- Required packages:
  - pydub
  - rich

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install pydub rich
```

## Usage

1. Run the script:
```bash
python separador.py
```

2. Follow the prompts:
   - Enter the path to your audio file
   - Enter minimum silence length (recommended: 1000ms)
   - Enter silence threshold in dB (recommended: -40dB)

3. The script will create a new folder called "segmentos" containing the split audio files.

## Parameters

- **Silence Length**: The minimum length of silence (in milliseconds) to be considered as a splitting point
- **Silence Threshold**: The maximum amplitude (in dB) to be considered as silence

## Output

The script creates numbered audio segments (audio_1.mp3, audio_2.mp3, etc.) in a "segmentos" subfolder.

## Error Handling

The script includes error handling for:
- Invalid file paths
- Invalid input parameters
- Processing errors
