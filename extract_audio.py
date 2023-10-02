from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_silence
import pandas as pd
from tqdm import tqdm
import os

audio_path = "videoplayback.wav"
MIN_SILENCE=500
SILENCE_THRESH=-40
def split_on_silence(audio_file_path=audio_path, audio_format="wav", chunk_len_ms=100000, min_silence_len=MIN_SILENCE, silence_thresh=SILENCE_THRESH):
    """
    Splits an audio file into chunks based on silence intervals detected in the audio.

    Args:
        audio_file_path (str): The path to the audio file.
        audio_format (str, optional): The format of the audio file. Default is "wav".
        chunk_len_ms (int, optional): The length of each chunk in milliseconds. Default is 120000 (2 minutes).
        min_silence_len (int, optional): The minimum duration of silence required to be considered as a silence interval. Default is the value of `MIN_SILENCE` variable.
        silence_thresh (int, optional): The threshold value for silence detection. Default is the value of `SILENCE_THRESH` variable.

    Returns:
        None

    Raises:
        None

    Example Usage:
        split_on_silence('audio.wav', audio_format='wav', chunk_len_ms=120000, min_silence_len=MIN_SILENCE, silence_thresh=SILENCE_THRESH)
    """
    try:
        sound = AudioSegment.from_file(file=audio_file_path, format=audio_format)
    except Exception as e:
        print(f"Error reading audio file: {e}")
        return
    
    print('Looking for pauses in speech, to make perfect chunks')
    silent_ranges = detect_silence(sound, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    df_silent = pd.DataFrame(data=silent_ranges, columns=['start_ms', 'end_ms'])
    df_silent['modulo'] = df_silent['end_ms'] // chunk_len_ms
    
    print('Calculating best chunk lengths')
    bornes_max = [df_silent[df_silent['modulo'] == i]['end_ms'].max() for i in tqdm(df_silent['modulo'].unique())]
    
    # Create a directory to save the audio chunks
    output_dir = 'audio_chunks'
    os.makedirs(output_dir, exist_ok=True)
    
    if bornes_max and len(sound):
        bornes_final = list(zip([0, *bornes_max], [*bornes_max, len(sound)]))
        file_prefix = 'chunk'
        print('Exporting audio chunks')
        [sound[bornes_final[i][0]:bornes_final[i][1]].export(os.path.join(output_dir,f'{file_prefix}-{i}.wav'), format=audio_format) for i in tqdm(range(len(bornes_final)))]
        
        
if __name__ == '__main__':
    split_on_silence()