import logging
import torch
import torchaudio
from transformers import AutoModelForCTC, Wav2Vec2ProcessorWithLM
import os
import glob
import gc
import sys

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = AutoModelForCTC.from_pretrained("bhuang/asr-wav2vec2-french").to(device)
processor = Wav2Vec2ProcessorWithLM.from_pretrained("bhuang/asr-wav2vec2-french")
    
def transcript_audio_to_text(model=model, processor=processor, audio_format='wav', chunk_path='./audio_chunks', output_path='./text_extraction'):
    """
    Transcribes audio chunks to text using the Wav2Vec2 model.
    
    Args:
        audio_format (str): The format of the audio files. Defaults to 'wav'.
        chunk_path (str): The path to the audio chunks. Defaults to './audio_chunks'.
        output_path (str): The path to save the extracted text files. Defaults to 'text_extraction'.
    """
    model_sample_rate = processor.feature_extractor.sampling_rate
    chunk_list = glob.glob(os.path.join(chunk_path, '*.{}'.format(audio_format)))
    chunk_list.sort()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    print('Audio chunks to convert: %s', chunk_list)

    os.makedirs(output_path, exist_ok=True)

    with torch.inference_mode():
        for i, chunk in enumerate(chunk_list):
            logger.info('audio chunk: %s, file name: %s', i, chunk)
            waveform, sample_rate = torchaudio.load(chunk)
            waveform = waveform.squeeze(axis=0)  # mono

            if sample_rate != model_sample_rate:
                resampler = torchaudio.transforms.Resample(sample_rate, model_sample_rate)
                waveform = resampler(waveform)

            input_dict = processor(waveform, sampling_rate=model_sample_rate, return_tensors="pt")
            logits = model(input_dict.input_values[0].to(device)).logits

            #predicted_ids = torch.argmax(logits, dim=-1)
            #predicted_sentence = processor.batch_decode(predicted_ids)[0]
            predicted_sentence = processor.batch_decode(logits.cpu().numpy()).text[0]

            with open(os.path.join(output_path, "extracted_text_{'%04d'}.txt".format(i)), 'w') as f:
                f.write(predicted_sentence)

            gc.collect()
            torch.cuda.empty_cache()

    logger.info('All audio chunks have been transcripted !')

if __name__ == '__main__':
    transcript_audio_to_text()