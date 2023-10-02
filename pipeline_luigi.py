import luigi
import logging
import subprocess
logging.basicConfig(level=logging.INFO)

class ExtractAudio(luigi.Task):
    def requires(self):
        return []

    def run(self):
        logging.info("Running ExtractAudio task")
        subprocess.run(["python", "extract_audio.py"])

class ConvertAudioToText(luigi.Task):
    def requires(self):
        return [ExtractAudio()]

    def run(self):
        logging.info("Running ConvertAudioToText task")
        subprocess.run(["python", "convert_audio_to_text.py"])

class Punctuation(luigi.Task):
    def requires(self):
        return [ConvertAudioToText()]

    def run(self):
        logging.info("Running Punctuation task")
        subprocess.run(["python", "punctation.py"])

class Summary(luigi.Task):
    def requires(self):
        return [Punctuation()]

    def run(self):
        logging.info("Running Summary task")
        subprocess.run(["python", "summary.py"])

if __name__ == "__main__":
    luigi.build([Summary()], local_scheduler=True)
    luigi.run()