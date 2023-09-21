import luigi
import subprocess

# Define a Luigi Task to Extract Audio
class ExtractAudioTask(luigi.Task):
    video_path = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget("audio.mp3")

    def run(self):
        # Replace this command with your actual extraction command
        extraction_command = ["python", "extract_audio.py", self.video_path, "audio.mp3"]
        subprocess.run(extraction_command, check=True)

# Define a Luigi Task to Convert Audio to Text
class ConvertAudioToTextTask(luigi.Task):
    def requires(self):
        return ExtractAudioTask(video_path="video.mp4")

    def output(self):
        return luigi.LocalTarget("output.txt")

    def run(self):
        # Replace this command with your actual conversion command
        conversion_command = ["python", "convert_audio_to_text.py", "audio.mp3", "output.txt"]
        subprocess.run(conversion_command, check=True)

if __name__ == "__main__":
    luigi.build([ConvertAudioToTextTask()], local_scheduler=True)
