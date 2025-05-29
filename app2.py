import gradio as gr
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import numpy as np
import os
import joblib
import pandas as pd # Sadece id2label için

# --- Sabitler ve Model Tanımlamaları ---
#class_names = ['cataract', 'diabetic_retinopathy', 'glaucoma','normal']
id2label = {0:'cataract', 1:'diabetic_retinopathy', 2:'glaucoma', 3:'normal'}
class_names = [id2label[i] for i in sorted(id2label.keys())]
NUM_CLASSES = len(class_names)

# ResNet18 Tabanlı Model Tanımı
class CustomResNet18(nn.Module):
    def __init__(self, num_classes=4):
        super().__init__()
        base = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        self.features = nn.Sequential(*list(base.children())[:-1])
        in_ftrs = base.fc.in_features
        self.classifier = nn.Sequential(
            nn.Linear(in_ftrs, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        return self.classifier(x)

# ReliefF Sonrası Basit Sınıflandırıcı Model Tanımı
class SimpleClassifierRelief(nn.Module):
    def __init__(self, input_features, num_classes):
        super().__init__()
        self.classifier = nn.Sequential(
            nn.Linear(input_features, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        return self.classifier(x)

# Cihaz belirleme
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# --- Modelleri Yükleme Fonksiyonları ---
# Gradio'da da yükleme işlemini bir kere yapacak şekilde fonksiyonları dışarıda tutabiliriz
def load_models_and_transformers():
    # Orijinal Model
    original_model = CustomResNet18(num_classes=NUM_CLASSES).to(device)
    original_model.load_state_dict(torch.load("best_model_resnet18_yeni.pth", map_location=device))
    original_model.eval()

    # ReliefF Model ve Transformerlar
    try:
        scaler = joblib.load('min_max_scaler.joblib')
        relief_transformer = joblib.load('relief_transformer.joblib')
    except FileNotFoundError:
        raise FileNotFoundError("MinMaxScaler veya ReliefF transformer dosyaları bulunamadı. Lütfen 'min_max_scaler.joblib' ve 'relief_transformer.joblib' dosyalarının uygulamanın bulunduğu dizinde olduğundan emin olun.")

    input_relief_features = relief_transformer.n_features_to_select
    relief_model = SimpleClassifierRelief(input_relief_features, NUM_CLASSES).to(device)
    relief_model.load_state_dict(torch.load("model_relief_classifier.pth", map_location=device))
    relief_model.eval()

    return original_model, relief_model, scaler, relief_transformer

# Modelleri ve transformer'ları uygulama başlangıcında bir kez yükle
original_model, relief_model, scaler, relief_transformer = load_models_and_transformers()

# --- Görüntü Dönüşümleri ---
preprocess_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# --- Tahmin Fonksiyonu (Gradio için ana işlev) ---
def predict_eye_condition(image: Image.Image):
    if image is None:
        return "Lütfen bir görüntü yükleyin.", "", {} , "" ,{}

    img_tensor = preprocess_transform(image).unsqueeze(0).to(device)

    # Orijinal Model Tahmini
    with torch.no_grad():
        original_output = original_model(img_tensor)
        original_probabilities = torch.softmax(original_output, dim=1)[0]
        original_predicted_idx = torch.argmax(original_probabilities).item()
        original_predicted_class = class_names[original_predicted_idx]
        original_confidence = original_probabilities[original_predicted_idx].item() * 100

    original_results = {class_names[i]: original_probabilities[i].item() for i in range(NUM_CLASSES)}
    original_pred_text = f"Hastalık: {original_predicted_class}\nGüven: %{original_confidence:.2f}"

    # ReliefF Özellik Azaltma Sonrası Model Tahmini
    with torch.no_grad():
        features = original_model.features(img_tensor)
        features = torch.flatten(features, 1).cpu().numpy()
        scaled_features = scaler.transform(features)
        relief_features = relief_transformer.transform(scaled_features)
        relief_features_tensor = torch.tensor(relief_features).float().to(device)

        relief_output = relief_model(relief_features_tensor)
        relief_probabilities = torch.softmax(relief_output, dim=1)[0]
        relief_predicted_idx = torch.argmax(relief_probabilities).item()
        relief_predicted_class = class_names[relief_predicted_idx]
        relief_confidence = relief_probabilities[relief_predicted_idx].item() * 100

    relief_results = {class_names[i]: relief_probabilities[i].item() for i in range(NUM_CLASSES)}
    relief_pred_text = f"Hastalık: {relief_predicted_class}\nGüven: %{relief_confidence:.2f}"

    return (
        "## Orijinal Model (ResNet18) Tahmini:",
        original_pred_text,
        original_results,
        "## ReliefF Sonrası Model Tahmini:",
        relief_results
    )

# --- Gradio Arayüzü Tanımlaması ---
# Giriş bileşenleri
input_image = gr.Image(type="pil", label="Göz Görüntüsü Yükle")

# Çıkış bileşenleri
# Gradio'da Markdown, Label ve BarPlot kullanacağız
output_original_title = gr.Markdown()
output_original_text = gr.Textbox(label="Orijinal Model Sonucu")
output_original_plot = gr.Label(label="Orijinal Model Olasılıkları")

output_relief_title = gr.Markdown()
output_relief_plot = gr.Label(label="ReliefF Model Olasılıkları") # Sadece plot gösterebiliriz, metin çıktı olarak aynı yerden gelebilir

# Arayüz oluşturma
demo = gr.Interface(
    fn=predict_eye_condition,
    inputs=input_image,
    outputs=[
        output_original_title,
        output_original_text,
        output_original_plot,
        output_relief_title,
        output_relief_plot
    ],
    title="Göz Hastalığı Teşhisi Uygulaması ",
    description="Yüklediğiniz göz görüntüsünü kullanarak farklı modellerle hastalık teşhisi yapar.",
    article="""
    Bu uygulama, makine öğrenimi modellerinin bir göz görüntüsünden olası hastalıkları nasıl teşhis edebileceğini göstermektedir.
    <br>
    <ul>
        <li><b>Orijinal Model:</b> ResNet18 tabanlı bir Evrişimsel Sinir Ağı (CNN) modelidir. Görüntülerden doğrudan görsel özellikler çıkarır ve sınıflandırır.</li>
        <li><b>ReliefF Sonrası Model:</b> Orijinal ResNet18'den çıkarılan özelliklere ReliefF algoritması uygulanarak en önemli özellikler seçildikten sonra eğitilen daha basit, tam bağlantılı bir yapay sinir ağı modelidir. Özellik azaltmanın model performansı üzerindeki etkisini gözlemlemek için kullanılır.</li>
    </ul>
    <br>
    <b>Uyarı:</b> Bu uygulama yalnızca bir demo amaçlıdır ve profesyonel tıbbi teşhisin yerine geçmez. Lütfen herhangi bir sağlık sorunu için yetkili bir sağlık uzmanına danışın.
    """,
    examples=[

    ]
)

if __name__ == "__main__":
    demo.launch()