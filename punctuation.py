from deepmultilingualpunctuation import PunctuationModel
import os
import glob

model = PunctuationModel()

if __name__ == '__main__':
    # Create a directory to save the audio chunks

    output_dir = 'text_punctuation'
    os.makedirs(output_dir, exist_ok=True)
    
    text_files_list = glob.glob(os.path.join('./text_extraction/','*.txt'))
    text_files_list.sort()
    
    for i, file in enumerate(text_files_list):
        print(f'fichier en cours {file} \n')
        with open(os.path.join(output_dir, f"text_with_punctation_{i}.txt"), 'w') as f:
            with open(file, 'r') as content:
                result=model.restore_punctuation(content.read())
                f.write(result)
        f.close()
        

