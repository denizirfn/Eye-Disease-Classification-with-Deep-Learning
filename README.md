Derin Öğrenme ile Çoklu Göz Hastalığı Sınıflandırması
Bu proje, fundus görüntüleri kullanarak Diyabetik Retinopati, Katarakt, Glokom ve Normal olmak üzere dört farklı göz hastalığının otomatik olarak teşhis edilmesi amacıyla geliştirilmiş derin öğrenme modellerini içermektedir. Proje, veri ön işleme, çeşitli CNN mimarilerinin transfer öğrenme ile adaptasyonu, boyut indirgeme teknikleri ve kullanıcı dostu bir Gradio arayüzü ile kapsamlı bir yapay zeka destekli teşhis sistemi sunmaktadır.

🚀 Proje Amacı
Göz hastalıklarının erken teşhisi, tedavi başarısı için kritik öneme sahiptir. Bu proje, fundus görüntülerinden otomatik olarak hastalık tespiti yaparak hem sağlık profesyonellerine destek olmayı hem de teşhis süreçlerini hızlandırmayı hedeflemektedir. Derin öğrenme tabanlı yaklaşımlar ve boyut indirgeme teknikleri kullanılarak verimli ve doğru bir sınıflandırma sistemi oluşturulmuştur.

✨ Özellikler
Çoklu Hastalık Sınıflandırması: Diyabetik Retinopati, Katarakt, Glokom ve Normal olmak üzere 4 farklı göz durumu sınıflandırması.
Derin Öğrenme Modelleri: ImageNet üzerinde önceden eğitilmiş ResNet-18, DenseNet-121, MobileNetV2, EfficientNet-B0 ve EfficientNet-B3 modellerinin transfer öğrenme ile ince ayarı.
Kapsamlı Veri Ön İşleme: Görüntü boyutlandırma, RGB formatına dönüştürme ve aşırı öğrenmeyi engellemek için zengin veri artırma teknikleri (yatay/dikey çevirme, döndürme, renk oynatımı).
Stratifiye Veri Bölme: Eğitim, doğrulama ve test setlerinin, sınıf dağılımlarını koruyarak %70 eğitim, %10 doğrulama ve %20 test oranlarında ayrılması.
Hiperparametre Optimizasyonu: Her model için batch boyutu, optimizatör, dondurulmuş katman sayısı, öğrenme oranı ve erken durdurma sabrı gibi hiperparametrelerin manuel olarak optimize edilmesi.
Boyut İndirgeme ve Özellik Çıkarımı: En iyi performansı gösteren ResNet-18 modelinden özellik çıkarımı ve bu özellikler üzerinde PCA (Temel Bileşen Analizi) ile Relief yöntemleri kullanılarak boyut indirgeme.
Basit Sınıflandırıcılar: Boyutu indirgenmiş özellikler üzerinde eğitilmiş hafif bir tam bağlantılı sinir ağı modeli ile performans değerlendirmesi.
Kullanıcı Arayüzü (Gradio): Modellerin kolayca test edilebilmesi ve tahmin sonuçlarının görselleştirilmesi için interaktif bir web arayüzü.

Sonuçlar
Derin Öğrenme Modeli Performansları
Projede kullanılan beş farklı CNN mimarisinin test seti üzerindeki performans metrikleri aşağıda özetlenmiştir.
Model Adı	Test Doğruluğu (%)
ResNet-18:	93.02
MobileNetV2	:91.67
EfficientNet-B0:	88.05
EfficientNet-B3	:88.05
DenseNet-121	:90.52

Boyut İndirgeme Sonrası Performans
ResNet-18'den çıkarılan özellikler üzerinde PCA ve Relief yöntemlerinin uygulanmasının ardından basit bir tam bağlantılı sinir ağının sınıflandırma performansları:
Yöntem	Test Doğruluğu (%)
Orijinal ResNet-18:	93.36
PCA Sonrası:	93.16
Relief Sonrası	:93.25
Bu sonuçlar, boyut indirgeme sonrası bile orijinal derin öğrenme modeline yakın bir sınıflandırma performansı elde edilebildiğini göstermektedir. Özellikle Relief yöntemi, seçilen özelliklerin ayırt ediciliğini korumada başarılı olmuştur.

