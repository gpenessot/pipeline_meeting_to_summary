import luigi
import subprocess
from extract_audio import split_on_silence
from convert_audio_to_text import transcript_audio_to_text

class ExtractAudio(luigi.Task):
    def output(self):
        return {
            'wav': luigi.LocalTarget('./videoplayback.wav'),
            'chunks': luigi.LocalTarget('./audio_chunks')
        }

    def run(self):
        split_on_silence()


class TextExtraction(luigi.Task):
    def requires(self):
        return ExtractAudio()

    def output(self):
        return luigi.LocalTarget('./text_extraction')

    def run(self):
        transcript_audio_to_text()


class Punctuation(luigi.Task):
    def requires(self):
        return TextExtraction()

    def output(self):
        return luigi.LocalTarget('./text_punctuation')

    def run(self):
        subprocess.run(["python", "punctuation.py"])


class SummarizeText(luigi.Task):
    def requires(self):
        return Punctuation()

    def output(self):
        return luigi.LocalTarget('./summary.txt')

    def run(self):
        subprocess.run(["python", "summarize_text.py"])

if __name__ == "__main__":
    luigi.build([SummarizeText()], local_scheduler=True)