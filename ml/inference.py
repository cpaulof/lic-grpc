import torch
import torch.nn.functional as F
from tokenizers import Tokenizer

from . import model
import config

tokenizer = Tokenizer.from_file(config.ML_TOKENIZER_PATH)
tokenizer.enable_truncation(model.SEQ_LENGTH-1)

class InferenceModel:
    def __init__(self):
        self.model = model.load_model()
        print('model loaded!')
    
    def process(self, text):
        text = text.strip()
        enc = tokenizer.encode(text)
        inputs = torch.tensor([1]+enc.ids)
        target = torch.tensor(enc.ids + [2])
        mask = torch.tensor(enc.attention_mask)
        inputs = F.pad(inputs, [0, model.SEQ_LENGTH - len(inputs)])
        target = F.pad(target, [0, model.SEQ_LENGTH - len(target)])
        mask = F.pad(mask, [0, model.SEQ_LENGTH - len(mask)])
        return inputs, target, mask

    def __call__(self, text):
        with torch.no_grad():
            tokens, _, _ = self.process(text.lower())
            tokens = tokens.unsqueeze(0)
            return self.model(tokens).softmax(-1).squeeze(0).numpy()
        