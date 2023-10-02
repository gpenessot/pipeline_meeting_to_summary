import luigi

class ExtractAudio(luigi.Task):
    def requires(self):
        return []

    def run(self):
        import subprocess
        subprocess.run(["python", "extract_audio.py"])

class ConvertAudioToText(luigi.Task):
    def requires(self):
        return [ExtractAudio()]

    def run(self):
        import subprocess
        subprocess.run(["python", "convert_audio_to_text.py"])

class Punctuation(luigi.Task):
    def requires(self):
        return [ConvertAudioToText()]

    def run(self):
        import subprocess
        subprocess.run(["python", "punctation.py"])

class Summary(luigi.Task):
    def requires(self):
        return [Punctuation()]

    def run(self):
        import subprocess
        subprocess.run(["python", "summary.py"])

if __name__ == "__main__":
    luigi.build([ExtractAudio(), ConvertAudioToText(), Punctuation(), Summary()], local_scheduler=True)
    luigi.run()