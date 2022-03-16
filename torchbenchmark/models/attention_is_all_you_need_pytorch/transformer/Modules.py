import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional

__author__ = "Yu-Hsiang Huang"

class ScaledDotProductAttention(nn.Module):
    ''' Scaled Dot-Product Attention '''

    def __init__(self, temperature, attn_dropout=0.1):
        super().__init__()
        self.temperature = temperature
        self.dropout = nn.Dropout(attn_dropout)

    def forward(self, q, k, v, mask : Optional[torch.Tensor] = None):

        attn = torch.matmul(q / self.temperature, k.transpose(2, 3))

        if mask is not None:
            if attn.dtype == torch.float16:
                min_mask = torch.finfo(torch.float16).min
            else:
                min_mask = -1e9
            attn = attn.masked_fill(mask == 0, min_mask)

        attn = self.dropout(F.softmax(attn, dim=-1))
        output = torch.matmul(attn, v)

        return output, attn
