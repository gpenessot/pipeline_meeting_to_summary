import os
import logging
import pandas as pd
from tqdm import tqdm
import moviepy.editor as mp
from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_silence

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

video_path = "videoplayback.mp4"
audio_path = "videoplayback.wav"

MIN_SILENCE=500
SILENCE_THRESH=-40

def split_on_silence(video_file_path=video_path, audio_file_path=audio_path, audio_format="wav", chunk_len_ms=100000, min_silence_len=MIN_SILENCE, silence_thresh=SILENCE_THRESH):
    """
    Split a video file into chunks based on periods of silence in the audio.

    Args:
        video_file_path (str, optional): The path of the video file to be split. Default is `video_path`.
        audio_file_path (str, optional): The path to save the extracted audio file. Default is `audio_path`.
        audio_format (str, optional): The format of the audio file. Default is "wav".
        chunk_len_ms (int, optional): The desired length of each audio chunk in milliseconds. Default is 100000.
        min_silence_len (int, optional): The minimum duration of silence required to consider it as a pause in speech. Default is `MIN_SILENCE`.
        silence_thresh (int, optional): The threshold level below which audio is considered as silence. Default is `SILENCE_THRESH`.

    Returns:
        None: The function does not return any value. The audio chunks are saved as separate files in the 'audio_chunks' directory.
    """
    try:
        logger.info(f'Read video file {video_file_path}.')
        video = mp.VideoFileClip(video_file_path)
        logger.info(f'Write audio file {audio_file_path}.')
        video.audio.write_audiofile(audio_file_path)
        logger.info(f'Read audio file {video_file_path}.')
        sound = AudioSegment.from_file(file=audio_file_path, format=audio_format)
    except Exception as e:
        print(f"Error reading audio file: {e}")
        return
    
    logger.info('Looking for pauses in speech, to make perfect chunks')
    silent_ranges = detect_silence(sound, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    df_silent = pd.DataFrame(data=silent_ranges, columns=['start_ms', 'end_ms'])
    df_silent['modulo'] = df_silent['end_ms'] // chunk_len_ms
    
    logger.info('Calculating best chunk lengths')
    bornes_max = [df_silent[df_silent['modulo'] == i]['end_ms'].max() for i in tqdm(df_silent['modulo'].unique())]
    
    # Create a directory to save the audio chunks
    output_dir = 'audio_chunks'
    os.makedirs(output_dir, exist_ok=True)
    
    if bornes_max and len(sound):
        bornes_final = list(zip([0, *bornes_max], [*bornes_max, len(sound)]))
        file_prefix = 'chunk'
        logger.info('Exporting audio chunks')
        [sound[bornes_final[i][0]:bornes_final[i][1]].export(os.path.join(output_dir,f'{file_prefix}-{i}.wav'), format=audio_format) for i in tqdm(range(len(bornes_final)))]
        
        
if __name__ == '__main__':
    split_on_silence()