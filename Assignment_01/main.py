from tokenizer import sentence_tokenizer,word_tokenizer
from datasets import load_dataset
from tqdm import tqdm

# Load the Hindi dataset from IndicCorpV2
dataset = load_dataset("ai4bharat/IndicCorpV2", "indiccorp_v2", split="hin_Deva",streaming=True)

# Tokenize the dataset and save to a file
output_file = "tokenized_hindi.txt" 
with open(output_file, "w", encoding="utf-8") as fout:
    for row in tqdm(dataset, desc="Tokenizing dataset"):
        text = row['text']
        # Sentence tokenize
        sentences = sentence_tokenizer(text)
        for sent in sentences:
            tokens = word_tokenizer(sent)
            fout.write(" ".join(tokens) + "\n")