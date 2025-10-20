# 📊 Development Index Calculator

Bu araç, Z-skorlu veri setini ve endeks yapısını kullanarak
**bölgesel gelişmişlik skorlarını** otomatik hesaplar.

## 🚀 Özellikler
- Göstergeleri otomatik eşleştirir  
- Negatif yönlü göstergeleri ters çevirir  
- Boyut bazlı ve genel gelişmişlik skorlarını üretir  
- Sonuçları Excel dosyası olarak dışa aktarır

## 📁 Klasör Yapısı
data/
├─ z_scores.xlsx
└─ index_structure.xlsx
output/
└─ development_scores.xlsx

## 💻 Kullanım
```bash
pip install -r requirements.txt
python main.py
