import torch
import torchaudio

from transformers import AutoModelForCTC, Wav2Vec2ProcessorWithLM


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

model = AutoModelForCTC.from_pretrained("bhuang/asr-wav2vec2-french").to(device)
processor_with_lm = Wav2Vec2ProcessorWithLM.from_pretrained("bhuang/asr-wav2vec2-french")
model_sample_rate = processor_with_lm.feature_extractor.sampling_rate

wav_path = "reunion_des_referents_20230913.wav"  # path to your audio file
waveform, sample_rate = torchaudio.load(wav_path)
waveform = waveform.squeeze(axis=0)  # mono

# resample
if sample_rate != model_sample_rate:
    resampler = torchaudio.transforms.Resample(sample_rate, model_sample_rate)
    waveform = resampler(waveform)

# normalize
input_dict = processor_with_lm(waveform, sampling_rate=model_sample_rate, return_tensors="pt")

with torch.inference_mode():
    logits = model(input_dict.input_values.to(device)).logits

predicted_sentence = processor_with_lm.batch_decode(logits.cpu().numpy()).text[0]

with open('extracted_text', 'w') as f:
    f.write(predicted_sentence)
    f.close()