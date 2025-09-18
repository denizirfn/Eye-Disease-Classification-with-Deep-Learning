<img width="339" height="282" alt="image" src="https://github.com/user-attachments/assets/fabbb3e6-b9c9-4517-b803-6802c4e6dcf0" /># 👁️ Derin Öğrenme ile Çoklu Göz Hastalığı Sınıflandırması

Bu bölümde, **Diyabetik Retinopati, Katarakt, Glokom ve Normal** olmak üzere dört sınıfı kapsayan bir fundus görüntüsü sınıflandırma sistemi geliştirilmiştir.  
Çalışmada derin öğrenme tabanlı **transfer öğrenme yöntemleri** kullanılmış, farklı CNN mimarileri karşılaştırılmış ve en iyi model seçilmiştir.

---

## 📂 1. Veri Seti Hazırlığı ve Etiketleme
- Kaggle’dan elde edilen veri seti kullanılmıştır.
- Veri setinde 4 farklı sınıf bulunmaktadır:
  - **Diyabetik Retinopati (DR)**
  - **Katarakt**
  - **Glokom**
  - **Normal**

  
## 🖼️ 2. Görüntü Ön İşleme ve Veri Artırma
- Tüm görseller **RGB** formatına dönüştürülmüştür.
- Görseller **224x224 piksel** boyutuna ölçeklenmiştir.
- Eğitim sırasında **veri artırma (augmentation)** uygulanmıştır:
- %50 olasılıkla yatay ve dikey çevirme
- ±15° rastgele döndürme
- Parlaklık, kontrast ve doygunlukta %20’ye kadar değişiklik
- Normalizasyon: Görseller [0,1] aralığına ölçeklenmiştir.
- **Doğrulama ve test setleri** için sadece yeniden boyutlandırma uygulanmıştır.

  ## 🔀 3. Veri Setinin Bölünmesi
- Stratified split yöntemi kullanılmıştır (sınıf oranları korunmuştur).
- Bölünme oranları:
- %70 Eğitim
- %10 Doğrulama
- %20 Test
- **PyTorch DataLoader** ile veri yükleme yapılmıştır.
- Eğitim seti shuffle=True ile karıştırılmıştır, test seti sabit tutulmuştur.

## 🧠 4. Kullanılan Derin Öğrenme Modelleri
Beş farklı **önceden eğitilmiş CNN mimarisi** transfer öğrenme yöntemiyle uyarlanmıştır:
- ResNet-18
- DenseNet-121
- MobileNetV2
- EfficientNet-B0
- EfficientNet-B3

Her modelde:
- Sınıf sayısı = 4 olacak şekilde son katman güncellenmiştir.
- **Fine-tuning** uygulanmıştır (son katmanlar eğitilebilir bırakılmıştır).
- Optimize edilen hiperparametreler:
- Batch Size
- Optimizer (Adam, AdamW)
- Frozen Layer sayısı
- Learning Rate
- Dropout oranı
- Early Stopping patience

## ⚙️ Hiperparametreler

| Model Adı   | Batch Size | Optimizer | Dondurulan Katman Sayısı | Learning Rate | Dropout | Patience |
|-------------|------------|-----------|---------------------------|---------------|---------|----------|
| ResNet18    | 32         | AdamW     | Son 50                   | 1e-5, 8e-4    | 0.5     | 3        |
| MobileNetV2 | 32         | Adam      | Son 50                   | 3e-5, 8e-4    | 0.5     | 5        |
| EfficientB0 | 32         | AdamW     | Son 50                   | 3e-5, 5e-4    | 0.5     | 3        |
| EfficientB3 | 64         | Adam      | Son 25                   | 3e-5, 5e-4    | 0.5     | 3        |
| DenseNet121 | 64         | AdamW     | Son 25                   | 3e-5, 8e-4    | 0.5     | 3        |


## 📊 5. Model Performansı
Her model, doğruluk (Accuracy) ve F1-score metrikleri ile değerlendirilmiştir.

| Model         | Accuracy | Test Accuracy |
|---------------|----------|---------------|
| **ResNet18**  | %93.36   | %93.02        |
| MobileNetV2   | %90.20   | %91.67        |
| EfficientNetB0| %90.28   | %91.70        |
| EfficientNetB3| %91.35   | %88.05        |
| DenseNet121   | %90.28   | %90.52        |

📌 Görseller:  
ResNet18 Modelinin Eğitim, Doğrulama ve Test Seti Performans Metrikleri:
- *<img width="684" height="244" alt="image" src="https://github.com/user-attachments/assets/e5b55292-4ed9-4734-90fa-520fc142ccd2" />

Mobilenetv2 Modelinin Eğitim, Doğrulama ve Test Seti Performans Metrikleri:
- *<img width="678" height="253" alt="image" src="https://github.com/user-attachments/assets/03d82bfb-7376-4764-8da2-3a0524c2ee89" />

Efficientb0 Modelinin Eğitim, Doğrulama ve Test Seti Performans Metrikleri:
- *<img width="844" height="266" alt="image" src="https://github.com/user-attachments/assets/a92b0763-c863-4f64-8bdf-043cc066e8ef" />

Efficientb3 Modelinin Eğitim, Doğrulama ve Test Seti Performans Metrikleri:
- *<img width="684" height="221" alt="image" src="https://github.com/user-attachments/assets/a8d924f2-4065-4383-aeef-9d3773dd8015" />

DenseNet121 Modelinin Eğitim, Doğrulama ve Test Seti Performans Metrikleri:
- *<img width="770" height="234" alt="image" src="https://github.com/user-attachments/assets/3688ba2c-8a53-480e-a19f-56aa02639b0b" />

📌 Görsel:
Resnet18 Modelinin kayıp ve doğrulama  grafikleri:
-*<img width="682" height="237" alt="image" src="https://github.com/user-attachments/assets/efa06e5c-d324-4449-bdd9-62e1e6430082" />

Mobilenetv2 Modelinin kayıp ve doğrulama  grafikleri:
-*<img width="624" height="219" alt="image" src="https://github.com/user-attachments/assets/074c339a-4c7e-4756-bb6d-3ab38ccaa3d7" />

Efficientb0 Modelinin kayıp ve doğrulama  grafikleri:
-*<img width="658" height="236" alt="image" src="https://github.com/user-attachments/assets/c93417ec-b1c8-4fae-8821-2562dbbeeff3" />

Efficientb3 Modelinin kayıp ve doğrulama  grafikleri:
-*<img width="606" height="214" alt="image" src="https://github.com/user-attachments/assets/688b0bee-dc7b-4c17-8861-d296aa4bbfff" />

DenseNet121 Modelinin kayıp ve doğrulama  grafikleri:
-*<img width="594" height="207" alt="image" src="https://github.com/user-attachments/assets/23fc05c6-61e8-4b78-b2af-13d539716851" />

---

## 🔎 6. Özellik Çıkarımı ve Boyut İndirgeme
- En başarılı model olan **ResNet18** kullanılarak **özellik vektörleri** çıkarılmıştır.
- Çıkarılan özellikler üzerinde iki yöntem uygulanmıştır:
- **PCA (Principal Component Analysis)**
  - %95 varyansı koruyacak şekilde boyut indirgeme yapılmıştır.
- **Relief**
  - En yüksek öneme sahip 100 öznitelik seçilmiştir.
- Daha sonra indirgenmiş özellikler üzerinde basit bir **tam bağlantılı yapay sinir ağı** ile sınıflandırma yapılmıştır.

📌 Görseller:  
PCA sonrası dağılım:
- *
  <img width="319" height="255" alt="image" src="https://github.com/user-attachments/assets/9c3f3cb8-242a-4cb7-89bd-193e09a3cb12" />
*
Relief  Sonrası  karmaşıklık matrisi
- *<img width="372" height="280" alt="image" src="https://github.com/user-attachments/assets/96da01b1-528f-4311-a494-07e38c008415" />
*  

| Model              | Accuracy |
|--------------------|----------|
| Orijinal ResNet18  | 0.9336   |
| PCA Sonrası        | 0.9316   |
| Relief Sonrası     | 0.9325   |

Bu sonuçlar, hem PCA hem de Relief ile boyut indirgeme yapıldıktan sonra bile, elde edilen özelliklerin 
orijinal derin öğrenme modeline yakın bir sınıflandırma performansı sergileyebildiğini göstermektedir. 
Bu durum, hem hesaplama verimliliği açısından önemli bir avantaj sağlayabilir hem de modelin 
öğrenmiş olduğu kritik bilgilerin boyut indirgeme sonrasında büyük ölçüde korunduğunu işaret eder. 
Özellikle Relief'in benzer performans sergilemesi, bu yöntemin seçilen özelliklerin ayırt ediciliğini 
korumadaki başarısını vurgulamaktadır. 
Her iki boyut indirgeme yaklaşımı da, yüksek boyutlu öz nitelik uzayını daha yönetilebilir bir boyuta 
indirgerken, sınıflandırma yeteneğinde önemli bir kayıp yaşanmadığını göstermiştir. Bu, derin öğrenme 
modellerinin ürettiği yüksek boyutlu özellik setlerinin, temel ayırt edici bilgileri taşıyan daha küçük bir 
alt kümesinin varlığını doğrular. Özellikle Relief, özelliklerin hedef değişkene göre önemini puanlayarak 
seçim yaptığı için, klinik olarak daha yorumlanabilir özelliklerin korunmasına yardımcı olabilir. Bu 
durum, modelin aldığı kararların arkasındaki nedenleri anlamak için potansiyel bir yol sunar ve tıbbi 
teşhis gibi kritik alanlarda şeffaflığı artırabilir.
---

## 💻 7. Kullanıcı Arayüzü
- **Gradio tabanlı arayüz** geliştirilmiştir.
- Kullanıcı bir fundus görüntüsü yükler → sistem tahmin yapar → sonuçlar olasılık dağılımları ile birlikte ekranda gösterilir.
- Aynı anda hem orijinal ResNet18 hem de boyut indirgeme sonrası modellerin tahminleri karşılaştırılabilir.

📌 Görseller: 
Arayüz Görüntüsü:
- *<img width="339" height="282" alt="image" src="https://github.com/user-attachments/assets/62970e79-369c-4b13-8366-4ad3f4c09955" />
*
Arayüz üzerinden yapılan tahmin görüntüsü:
- *<img width="338" height="301" alt="image" src="https://github.com/user-attachments/assets/5cc3af98-4831-449f-9585-c82f9bacf0ca" />
*  

---

## ⚠️ Not
Bu proje **yalnızca eğitim ve araştırma amaçlıdır**.  
Gerçek tıbbi teşhis için kullanılmamalıdır.
