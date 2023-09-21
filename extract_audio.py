import moviepy.editor as mp
import sys

def extract_audio_from_video(video_path, 
                             audio_format='wav'):
    my_clip = mp.VideoFileClip(video_path)
    name = video_path.split('.')[0]
    print('name : ', name)
    my_clip.audio.write_audiofile(name+'.'+audio_format, 
                                  codec='pcm_s16le')
    
if __name__ == '__main__':
    print(sys.argv[1])
    print(sys.argv[2])
    extract_audio_from_video(video_path=sys.argv[1],
                             audio_format=sys.argv[2])
    
    