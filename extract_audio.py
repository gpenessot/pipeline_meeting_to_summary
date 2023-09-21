import moviepy.editor as mp

rn = my_clip = mp.VideoFileClip('reunion_des_referents_20230913.mp4')
my_clip.audio.write_audiofile('reunion_des_referents_20230913.wav')