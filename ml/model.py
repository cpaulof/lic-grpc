import torch
import torch.nn as nn
import torch.nn.functional as F

import config

SEQ_LENGTH = 350
CLASS_NAMES = ['0', '1']
VOCAB_SIZE = 5000

emb_dim = 16
attn_heads = 4
ffn_inner_dim = 64
num_layers = 4


class Layer(nn.Module):
    def __init__(self):
        super(Layer, self).__init__()
        self.norm1 = nn.LayerNorm(emb_dim)
        self.norm2 = nn.LayerNorm(emb_dim)

        self.attn_head1 = nn.MultiheadAttention(emb_dim, attn_heads, batch_first=True)
        
        self.pq = nn.Linear(emb_dim, emb_dim, bias=False)
        self.pk = nn.Linear(emb_dim, emb_dim, bias=False)
        self.pv = nn.Linear(emb_dim, emb_dim, bias=False)
        
        self.linear1 = nn.Linear(emb_dim, ffn_inner_dim, bias=False)
        self.linear2 = nn.Linear(ffn_inner_dim, emb_dim, bias=False)

        self.attn_mask = nn.Transformer.generate_square_subsequent_mask(emb_dim)
        
        
    def forward(self, x):
        skip = x
        x = self.norm1(x)
        q, k, v = self.pq(x), self.pk(x), self.pv(x)
        x = self.attn_head1(q, k, v, need_weights=False, is_causal=True, attn_mask=self.attn_mask)[0]
        x = x + skip
        skip = x
        x = self.norm2(x)
        
        x = self.linear1(x)
        x = F.gelu(x)
        x = self.linear2(x)

        x += skip
        return x

class OutputLayer(nn.Module):
    def __init__(self, out1):
        super(OutputLayer, self).__init__()
        self.dropout1 = nn.Dropout(p=0.2)
        # self.dropout2 = nn.Dropout(p=0.2)
        self.linear1 = nn.Linear(emb_dim, emb_dim)
        self.norm1 = nn.LayerNorm(emb_dim)
        self.flat = nn.Flatten(1)
        self.gelu1 = nn.LeakyReLU(0.15)
        self.linear2 = nn.Linear(SEQ_LENGTH*emb_dim, len(CLASS_NAMES), bias=False)

    def forward(self, x):
        # x = self.dropout1(x)
        x = self.linear1(x)
        x = self.norm1(x)
        x = self.gelu1(x)
        x = self.dropout1(x)
        x = self.flat(x)
        x = self.linear2(x)
        return x
        
        
    
class Model(nn.Module):
    def __init__(self, _type):
        super(Model, self).__init__()
        assert _type in ('TUNING', 'PT')
        self.embeddings = nn.Embedding(VOCAB_SIZE, emb_dim)
        self.pos_emb = nn.Linear(emb_dim, emb_dim)

        self.attn_layers = nn.ModuleList([Layer() for i in range(num_layers)])

        self.norm1 = nn.LayerNorm(emb_dim)
        
        self.linear1 = nn.Linear(emb_dim, VOCAB_SIZE)
        self.output = None
        self._type = _type
        if self._type != 'PT':
            self.output = OutputLayer(256)
        
        
    def forward(self, x):
        x = self.embeddings(x)
        x = self.pos_emb(x) + x
        x/=emb_dim**0.5
        for layer in self.attn_layers:
            x = layer(x)
            
        x = self.norm1(x)
        
        if self.output is not None:
            x = self.output(x)
        else:
            x = torch.matmul(x, self.embeddings.weight.T)
        
        return x


def load_model():
    model = Model("TUNING")
    model.load_state_dict(torch.load(config.ML_MODEL_WEIGHTS_PATH, weights_only=True))
    model.eval()
    return model
