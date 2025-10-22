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

Proje dizininde:
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

🔸 Örnek Sorular:
Kategori	Örnek Soru
Problem Analizi	“Problem Statement'ında ‘type error’ geçen bir örnekte hangi kodlama ipucu verilmiştir?”
Kod Düzeltme	“Django reposundaki tarih formatlama hatasını düzelten patch’te hangi değişiklikler yapılmış?”
Test Kodu Sorgulama	“Bir test_patch içeriğinde ‘assert len(’ kontrolü geçen örnek var mı?”
Genel Kavram	“Bir döngüde liste elemanlarını değiştirirken IndexError almamak için ne yapılmalı?”

🔍 Debugging (Hata Ayıklama)
Arayüzdeki “🔍 İlk 3 kaynağı göster (debug)” seçeneğini işaretleyerek, modelin yanıt oluştururken kullandığı problem açıklamalarını, yamaları ve test kodlarını görüntüleyebilirsiniz.

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