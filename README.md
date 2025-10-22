<div align="center">

# 💡 SWE-RAG Kod Asistanı  

### SWE-ReBench veri setine dayalı, Haystack ve Google Gemini entegrasyonu kullanılarak oluşturulmuş, Türkçe RAG (Retrieval-Augmented Generation) tabanlı kodlama ve hata düzeltme chatbot projesi.  

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![Haystack](https://img.shields.io/badge/Haystack-RAG%20Framework-orange)
![Google Gemini](https://img.shields.io/badge/Google-Gemini-yellow?logo=google)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Datasets-%23ffcc4d?logo=huggingface)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## 📋 Proje Hakkında  

Bu proje, yazılım mühendisliği problemlerine, hata düzeltmelerine (**patch**) ve kodlama ipuçlarına (**hints_text**) hızlıca yanıt bulmak amacıyla geliştirilmiştir.  

Kullanıcı sorguları, **Hugging Face** üzerindeki **SWE-ReBench** veri setinden yüklenen ilgili belgeler (Problem Açıklaması, İpucu, Yama Kodları) kullanılarak **Retrieval** aşamasında çekilir.  
Daha sonra **Google Gemini** modeli, bu bağlama dayanarak Türkçe yanıt üretir (**Generation**).  

---

## ⚙️ Temel Özellikler

- 📚 **Veri Seti:** `nebius/SWE-rebench` kullanılarak kodlama problemleri ve çözümleri endekslenir.  
- 🌐 **Çok Dilli Embedding:** Sorgular ve belgeler `paraphrase-multilingual-MiniLM-L12-v2` modeliyle vektör uzayına dönüştürülür.  
- 💬 **Streamlit Arayüzü:** Kullanımı kolay, interaktif bir sohbet ekranı sunar.  
- 🧠 **Google Gemini Entegrasyonu:** Türkçe yanıt üretimi ve bağlam analizi sağlar.  
- 🔍 **Debug Modu:** Kullanılan kaynak belgeleri (retriever çıktısı) arayüzde görüntüleme imkânı sunar.  

---

## 🛠️ Kullanılan Teknolojiler  

| Kategori | Teknoloji | Versiyon / Model | Amaç |
|-----------|------------|------------------|------|
| RAG Çerçevesi | **haystack-ai** | Son sürüm | RAG pipeline ve bileşen akışını yönetir |
| Büyük Dil Modeli | **google-genai-haystack** | gemini-2.5-flash | Bağlamdan Türkçe yanıt üretimi |
| Embedding Modeli | **sentence-transformers** | paraphrase-multilingual-MiniLM-L12-v2 | Belgeleri ve sorguları gömüntüleme |
| Vektör Deposu | **InMemoryDocumentStore (Haystack)** | - | Bellek içi hızlı endeksleme |
| Arayüz | **streamlit** | Son sürüm | Web tabanlı kullanıcı arayüzü |
| Veri Kaynağı | **datasets** | nebius/SWE-rebench | Veri yükleme ve hazırlama |
| Ortam Yönetimi | **python-dotenv** | - | API anahtarlarını yönetme |

---

## ⚙️ Kurulum ve Çalıştırma  

### 1️⃣ Ön Gereksinimler  
- Python 3.8 veya üstü  
- Google API anahtarı (**Gemini** modeli için)  
- Hugging Face erişim token’ı (**SWE-ReBench** veri seti için)

---

### 2️⃣ Bağımlılıkların Kurulumu  

Proje dizininde aşağıdaki komutu çalıştırın:  
```bash
pip install -r requirements.txt
3️⃣ Ortam Değişkenlerini Ayarlama
Proje klasöründe .env adlı bir dosya oluşturun ve içine kendi anahtarlarınızı yazın:

bash
Copy code
# Google Gemini API Anahtarınız
GOOGLE_API_KEY="SİZİN_GOOGLE_API_ANAHTARINIZ"

# Kullanılacak model
GENAI_MODEL="gemini-2.5-flash"

# Hugging Face Token'ınız
HF_TOKEN="SİZİN_HUGGING_FACE_TOKENINIZ"
4️⃣ Uygulamayı Başlatma
bash
Copy code
streamlit run project.py
Uygulama, veri setini yükleyip embedding işlemini tamamladıktan sonra tarayıcıda açılır.

🚀 Nasıl Kullanılır?
Arayüz açıldığında “✅ Vektör veritabanı başarıyla oluşturuldu!” mesajını bekleyin.
Sohbet kutusuna veri setiyle ilgili Türkçe sorularınızı yazın.

💬 Örnek Sorular
SWE-RAG Kod Asistanı'na aşağıdaki türde sorular yöneltebilirsiniz:
Model, SWE-ReBench veri setinde uygun belge bulamazsa Google Gemini modelinin genel bilgisini kullanarak yanıt üretir.

🔹 Kodlama ve Hatalar Hakkında
Bu hatayı nasıl düzeltebilirim?

TypeError ne demektir?

Python’da liste elemanlarını değiştirirken neden IndexError alınır?

Bir fonksiyonda recursion yerine iteration kullanmak neden daha verimli olabilir?

🔹 Patch (Yama) ve Düzeltmeler
Django projesindeki tarih hatasını düzelten patch ne yapıyor?

Bu patch’te hangi değişiklikler yapılmış?

Performans iyileştirmesi yapan bir patch örneği var mı?

🔹 Test Kodları
Test patch içinde assert kullanılan bir örnek var mı?

Başarısız testler nasıl düzeltilmiş?

🔹 Genel Programlama Soruları
Two pointers tekniği nedir?

List comprehension ne işe yarar?

try-except yapısı hangi hataları yakalar?

💡 İpucu:
Sohbet kutusuna Türkçe yazabilirsiniz.
Model bağlam bulamadığında genel programlama bilgisini kullanır.
Bağlam bulduğunda ise yanıt sonunda “Kaynaklar:” bölümü görünür.

🧪 Test Planı
Aşağıdaki tablo, SWE-RAG Kod Asistanı'nın farklı türdeki sorulara nasıl yanıt verdiğini gösterir.
Bu tabloyu, uygulamayı test ederken sırasıyla kullanabilirsiniz.

No	Soru	Beklenen Kaynak	Açıklama / Beklenen Davranış
1	Django projesindeki tarih hatasını düzelten patch ne yapıyor?	SWE-ReBench (patch)	Veri setinden gerçek patch içeriği getirir.
2	Test patch içinde assert kullanılan bir örnek var mı?	SWE-ReBench (test_patch)	“assert” içeren test belgelerini bulur.
3	Python’da liste elemanlarını değiştirirken neden IndexError alınır?	Karma (veri + model)	Veri varsa onu kullanır, yoksa genel bilgiyle açıklar.
4	Two pointers tekniği nedir?	Model (Gemini)	Genel programlama açıklaması yapar.
5	Bu cevabı oluştururken hangi kaynak belgeler kullanıldı?	RAG (retriever)	“Kaynaklar:” kısmında meta verileri gösterir.

💡 Test İpuçları
✅ İyi sonuç: Yanıt sonunda “Kaynaklar:” kısmı görünüyorsa RAG pipeline doğru çalışıyor.

🧠 Genel bilgi yanıtı: Kaynak kısmı yoksa model kendi bilgisinden açıklama üretmiştir.

🔍 Debug seçeneği: “🔍 İlk 3 kaynağı göster (debug)” kutucuğunu işaretleyerek kullanılan belgeleri görebilirsiniz.

💬 Türkçe yanıt: Prompt sistemi Türkçe olarak ayarlandığından yanıtlar otomatik Türkçedir.

🤝 Katkı Notu
Bu proje kişisel bir çalışmadır.
Dış katkıya kapalıdır, ancak incelemeniz ve ilham almanızdan memnuniyet duyarım 🌟

🧾 Lisans
Bu proje MIT Lisansı altında yayınlanmıştır.
Detaylar için LICENSE dosyasına göz atabilirsiniz.

<div align="center">
💻 Developed with ❤️ by @aleynaSezer
⭐ Eğer proje hoşunuza gittiyse yıldız vermeyi unutmayın!

</div> ```