import sys
import os
import moviepy.editor as mp

def extract_audio_from_video(video_path, 
                             audio_format='wav',
                             codec='pcm_s16le'):
    """This function extracts the audio from a video file and 
    saves it as a separate audio file in the specified format.

    Args:
        video_path (_type_): The path of the video file from which the audio needs to be extracted.
        audio_format (str, optional): The format in which the audio should be saved. Defaults to 'wav'.
    """
    try :
        my_clip = mp.VideoFileClip(video_path)
        name = os.path.splitext(video_path)[0]
        my_clip.audio.write_audiofile(name+'.'+audio_format, 
                                      codec=codec)
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    
if __name__ == '__main__':
    extract_audio_from_video(video_path=sys.argv[1],
                             audio_format=sys.argv[2])
    
    