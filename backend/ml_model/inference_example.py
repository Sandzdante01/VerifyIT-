
import json
import joblib
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel

class HybridDebertaClassifier(nn.Module):
    def __init__(self, model_name, num_numeric_features, num_labels=3, dropout=0.2):
        super().__init__()
        self.text_model = AutoModel.from_pretrained(model_name)
        hidden_size = self.text_model.config.hidden_size
        self.numeric_net = nn.Sequential(
            nn.Linear(num_numeric_features, 32),
            nn.ReLU(),
            nn.Dropout(dropout)
        )
        self.classifier = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(hidden_size + 32, 128),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(128, num_labels)
        )

    def forward(self, input_ids=None, attention_mask=None, numeric_features=None):
        outputs = self.text_model(input_ids=input_ids, attention_mask=attention_mask)
        cls_embedding = outputs.last_hidden_state[:, 0, :]
        numeric_embedding = self.numeric_net(numeric_features.float())
        combined = torch.cat([cls_embedding, numeric_embedding], dim=1)
        logits = self.classifier(combined)
        return logits

def load_verifyit_model(model_dir):
    with open(f"{model_dir}/model_metadata.json", "r") as f:
        metadata = json.load(f)

    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    scaler = joblib.load(f"{model_dir}/numeric_feature_scaler.joblib")

    model = HybridDebertaClassifier(
        model_name=metadata["base_model_name"],
        num_numeric_features=len(metadata["numeric_columns"]),
        num_labels=metadata["num_labels"]
    )
    model.load_state_dict(torch.load(f"{model_dir}/hybrid_model_state_dict.pt", map_location="cpu"))
    model.eval()

    return model, tokenizer, scaler, metadata

def predict_claim(model, tokenizer, scaler, metadata, claim, evidence, numeric_feature_values):
    text = "[CLAIM] " + claim + " [EVIDENCE] " + evidence

    encoded = tokenizer(
        text,
        truncation=True,
        max_length=metadata["max_length"],
        return_tensors="pt"
    )

    numeric_scaled = scaler.transform([numeric_feature_values])
    numeric_tensor = torch.tensor(numeric_scaled, dtype=torch.float)

    with torch.no_grad():
        logits = model(
            input_ids=encoded["input_ids"],
            attention_mask=encoded["attention_mask"],
            numeric_features=numeric_tensor
        )
        probs = torch.softmax(logits, dim=1)[0]
        pred_id = int(torch.argmax(probs).item())
        confidence = float(probs[pred_id].item())

    label = metadata["id2label"][str(pred_id)]

    return {
        "label": label,
        "confidence": round(confidence * 100, 2),
        "probabilities": {
            metadata["id2label"][str(i)]: round(float(probs[i].item()) * 100, 2)
            for i in range(metadata["num_labels"])
        }
    }
