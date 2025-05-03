from fastapi import FastAPI, File, UploadFile
import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl
from torchvision import transforms
from torchvision.models import densenet201
from PIL import Image
import io
import unidic
import numpy as np

#インスタンス化
app = FastAPI()

#推論用のネットワークの定義
class Net1(pl.LightningModule):

    def __init__(self):
        super().__init__()

        self.feature = densenet201(pretrained=True)
        self.fc = nn.Linear(1000, 5)

    def forward(self, x):
        h = self.feature(x)
        h = self.fc(h)
        return h

#推論モードでインスタンス化
net1 = Net1().cpu().eval()

#学習済モデルの重みを読み込む
model_path1 = r"C:\Users\zabie\OneDrive\ドキュメント\誠 2024\課題の提出\image_densenet201c.pt"
net1.load_state_dict(torch.load(model_path1, map_location=torch.device('cpu')))

#推論時はデータ拡張なし。学習済モデルに合わせた前処理を追加
transform_valtest = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

#推論する関数の作成
def predict(image):
    img = transform_valtest(image)
    img = img.unsqueeze(0)
    with torch.no_grad():
        y = net1(img)
    return y.softmax(dim=-1)


import pytorch_lightning as pl
from transformers import BertModel, BertJapaneseTokenizer
bert_model_name = 'cl-tohoku/bert-base-japanese-whole-word-masking'
bert_tokenizer = BertJapaneseTokenizer.from_pretrained(bert_model_name)
import torch
from torch import nn
from pydantic import BaseModel
from typing import List

class Net2(pl.LightningModule):
    def __init__(self,
                 bert_model_name='cl-tohoku/bert-base-japanese-whole-word-masking',
                 num_classes=5):
        super().__init__()

        self.save_hyperparameters() # ハイパーパラメータを保存
        self.bert = BertModel.from_pretrained(bert_model_name)
        self.dropout = nn.Dropout(0.1)
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_classes)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs[1]  # [CLS] token の embedding
        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)
        return logits
    
#推論モードでインスタンス化
net2 = Net2().cpu().eval()  

#学習済モデルの重みを読み込む
model_path2 = r"C:\Users\zabie\OneDrive\ドキュメント\誠 2024\課題の提出\text_bert2.pt"
net2.load_state_dict(torch.load(model_path2, map_location=torch.device('cpu')))

class TextRequest(BaseModel):
    text: str

#テキストの前処理の関数を作成
def expect(text: str) -> List[float]:
    text = ''.join(text)
    encodings = bert_tokenizer(text, return_tensors='pt', padding='max_length', max_length=100, truncation=True)
    with torch.no_grad():
        output = net2(encodings['input_ids'], encodings['attention_mask'])
    return output.softmax(dim=-1)

@app.post("/propose/")
async def analyze_text(request: TextRequest):
    expectation = expect(request.text)
    return {"expectation": expectation.tolist()}


# 画像の適格性の確認を行うため、エンコーディング層の定義
class Encoder(pl.LightningModule):

    # 畳み込み層の定義
    def __init__(self):
        super().__init__()

        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(16)
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.conv3 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(64)

    # 順伝播の流れの定義
    def forward(self, x):
        h = self.conv1(x)
        h = self.bn1(h)
        h = F.relu(h)
        h = F.max_pool2d(h, kernel_size=2, stride=2)
        h = self.conv2(h)
        h = self.bn2(h)
        h = F.relu(h)
        h = F.max_pool2d(h, kernel_size=2, stride=2)
        h = self.conv3(h)
        h = self.bn3(h)
        h = F.relu(h)
        h = F.max_pool2d(h, kernel_size=2, stride=2)
        return h
    
# デコーディング層の定義
class Decoder(pl.LightningModule):

    # 転置畳み込み
    def __init__(self):
        super().__init__()

        self.convt1 = nn.ConvTranspose2d(64, 32, kernel_size=2, stride=2)
        self.bn1 = nn.BatchNorm2d(32)
        self.convt2 = nn.ConvTranspose2d(32, 16, kernel_size=2, stride=2)
        self.bn2 = nn.BatchNorm2d(16)
        self.convt3 = nn.ConvTranspose2d(16, 3, kernel_size=2, stride=2) # 3チャネル（RGB 画像）の出力
        self.bn3 = nn.BatchNorm2d(3)

    # 順伝播の流れ
    def forward(self, x):
        h = self.convt1(x)
        h = self.bn1(h)
        h = F.relu(h)
        h = self.convt2(h)
        h = self.bn2(h)
        h = F.relu(h)
        h = self.convt3(h)
        h = self.bn3(h)
        h = F.sigmoid(h)
        return h

class AutoEncoder(pl.LightningModule):

    # encoder, decoder を合体
    def __init__(self):
        super().__init__()

        self.encoder = Encoder()
        self.decoder = Decoder()

    # 順伝播
    def forward(self, x):
        h = self.encoder(x)
        h = self.decoder(h)
        return h
    
# 推論モードでインスタンス化
net3 = AutoEncoder().cpu().eval() 

#学習済モデルの重みを読み込む
model_path3 = r"C:\Users\zabie\OneDrive\ドキュメント\誠 2024\課題の提出\autoencoderB.pt"
net3.load_state_dict(torch.load(model_path3, map_location=torch.device('cpu')))

#推論時はデータ拡張なし。前処理のみ。
transform_test = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor()
])

#画像が閾値内にあるかどうかを調べる関数の定義
def confirm(image):
    img = transform_test(image)
    img = img.unsqueeze(0)
    with torch.no_grad():
        y = net3(img)
        loss = F.mse_loss(y, img, reduction='none')
        sum_loss = np.sum(loss.detach().numpy(), axis=(1, 2, 3))
        if sum_loss < 1159:
            return "accept"
        else:
            return "reject"

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    content = await file.read()
    image = Image.open(io.BytesIO(content))
    prediction = predict(image)
    confirmation = confirm(image)
    
    return {
        "prediction": prediction.tolist(),
        "confirmation": confirmation
        }

