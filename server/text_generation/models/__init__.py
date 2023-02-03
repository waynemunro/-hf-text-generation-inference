import torch

from transformers import AutoConfig
from typing import Optional

from text_generation.models.model import Model
from text_generation.models.causal_lm import CausalLM
from text_generation.models.bloom import BLOOM, BLOOMSharded
from text_generation.models.seq2seq_lm import Seq2SeqLM
from text_generation.models.galactica import Galactica, GalacticaSharded
from text_generation.models.santacoder import SantaCoder
from text_generation.models.gpt_neox import GPTNeox, GPTNeoxSharded
from text_generation.models.opt import OPT, OPTSharded

__all__ = [
    "Model",
    "BLOOM",
    "BLOOMSharded",
    "CausalLM",
    "Seq2SeqLM",
    "Galactica",
    "GalacticaSharded",
    "SantaCoder",
    "GPTNeox",
    "GPTNeoxSharded",
    "OPT",
    "OPTSharded",
    "get_model",
]

# The flag below controls whether to allow TF32 on matmul. This flag defaults to False
# in PyTorch 1.12 and later.
torch.backends.cuda.matmul.allow_tf32 = True

# The flag below controls whether to allow TF32 on cuDNN. This flag defaults to True.
torch.backends.cudnn.allow_tf32 = True


def get_model(
    model_id: str, revision: Optional[str], sharded: bool, quantize: bool
) -> Model:
    config = AutoConfig.from_pretrained(model_id, revision=revision)

    if model_id.startswith("facebook/galactica"):
        if sharded:
            return GalacticaSharded(model_id, revision, quantize=quantize)
        else:
            return Galactica(model_id, revision, quantize=quantize)
    elif "santacoder" in model_id:
        return SantaCoder(model_id, revision, quantize)
    elif config.model_type == "bloom":
        if sharded:
            return BLOOMSharded(model_id, revision, quantize=quantize)
        else:
            return BLOOM(model_id, revision, quantize=quantize)
    elif config.model_type == "gpt_neox":
        if sharded:
            return GPTNeoxSharded(model_id, revision, quantize=quantize)
        else:
            return GPTNeox(model_id, revision, quantize=quantize)
    elif config.model_type == "opt":
        if sharded:
            return OPTSharded(model_id, revision, quantize=quantize)
        else:
            return OPT(model_id, revision, quantize=quantize)
    else:
        if sharded:
            raise ValueError("sharded is not supported for AutoModel")
        try:
            return CausalLM(model_id, revision, quantize=quantize)
        except Exception:
            return Seq2SeqLM(model_id, revision, quantize=quantize)
