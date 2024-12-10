from graph_utils import load_graph_from_graphml
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# Check if GPU is available
def get_model_and_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
    model = AutoModelForSequenceClassification.from_pretrained("bucketresearch/politicalBiasBERT").to(device)
    return model, tokenizer

def run_inference(model, tokenizer, text):
    inputs = tokenizer(text, return_tensors="pt").to("cuda")

    outputs = model(**inputs)
    logits = outputs.logits
    probabilities = logits.softmax(dim=-1).tolist()[0]
    return probabilities

def get_classification(model, tokenizer, text):
    left, _, right = run_inference(model, tokenizer, text)
    return right - left

# G = load_graph_from_graphml('./graph_datasets/election_10000_graph')
