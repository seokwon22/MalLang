import argparse
import torch

from .data import *
from .model.transformer import Transformer

def get_src(s):
    src = encode([tokenize_ko_sen(s)],ko_stoi)
    return torch.tensor(src)
def get_init_tgt():
    tgt = [[sos_token_idx]]
    return torch.tensor(tgt)

def predict(model, input):
    src = get_src(input).to(device)
    tgt = get_init_tgt().to(device)

    model.eval() # evaluation mode (deactivate dropout)
    with torch.no_grad():
        for _ in range(max_len):
            output = model(src,tgt)
            last_word = output[:,-1:,:].max(dim=-1)[1]

            # eos token을 만나면 끝냄
            if torch.equal(last_word, torch.tensor([[eos_token_idx]]).to(device)):
                break

            # next tgt
            tgt = torch.cat([tgt,last_word],dim=-1)

        # decode tgt
        tgt_words = decode(tgt,en_itos)
        output = " ".join(tgt_words[0])

        return output