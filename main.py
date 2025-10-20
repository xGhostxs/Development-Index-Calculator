"""
Development Index Calculator
============================

Bu araç, Z-skorlu veri seti ile göstergeleri eşleştirerek
ilçe bazlı gelişmişlik skorlarını otomatik hesaplar.

İşlevler:
---------
1. Göstergeleri Z-skorlu verideki kolonlarla eşleştirir.
2. Negatif yönlü göstergeleri ters çevirir.
3. Boyut bazlı ve genel gelişmişlik skorlarını hesaplar.
4. Sonuçları Excel dosyası olarak kaydeder.

Kullanım:
---------
python main.py

Gerekli dosyalar:
- z_scores.xlsx      → Z-skorlu veri (örnek: ilçeler ve göstergeler)
- index_structure.xlsx → Göstergelerin ve boyutların yer aldığı yapı
"""

import pandas as pd

# ---------------------------
# DOSYA YOLLARI (anonimleştirilmiş)
# ---------------------------
z_skorlu_path = "data/z_scores.xlsx"
index_path = "data/index_structure.xlsx"
output_path = "output/development_scores.xlsx"

# ---------------------------
# 1) ENDEKS YAPISI OKUMA
# ---------------------------
index_df = pd.read_excel(index_path, sheet_name=0, header=None)
index_df.columns = ["Boyut", "Gösterge", "Ölçüm Yöntemi", "Ağırlık", "Açıklama"]

# Sadece gerekli kolonlar
index_clean = index_df[["Boyut", "Gösterge", "Ölçüm Yöntemi"]].dropna(subset=["Gösterge"])

# "Negatif" ifadesine göre yön belirleme
index_clean["Yön"] = index_clean["Ölçüm Yöntemi"].str.contains("negatif", case=False, na=False)
index_clean = index_clean[["Gösterge", "Boyut", "Yön"]]

# ---------------------------
# 2) Z SKORLU VERİ OKUMA
# ---------------------------
z_df = pd.read_excel(z_skorlu_path, sheet_name=0)
region_col = z_df.columns[0]  # örn: "İlçe" veya "Bölge"
regions = z_df[region_col]
z_columns = [c.strip() for c in z_df.columns if c != region_col]

# ---------------------------
# 3) GÖSTERGE EŞLEŞTİRME
# ---------------------------
mapping = {}
unmatched = []

for g in index_clean["Gösterge"].dropna().unique():
    matches = [c for c in z_columns if g.lower() in c.lower()]
    if matches:
        mapping[g] = matches[0]
    else:
        unmatched.append(g)

# ---------------------------
# 4) Z SKORLARI TABLOSU
# ---------------------------
z_scores = pd.DataFrame({region_col: regions})

for _, row in index_clean.iterrows():
    g = row["Gösterge"]
    is_negative = row["Yön"]
    if g in mapping:
        colname = mapping[g]
        coldata = z_df[colname]
        if is_negative:  # negatif yönlü göstergeyi ters çevir
            coldata = -1 * coldata
        z_scores[g] = coldata

# ---------------------------
# 5) GELİŞMİŞLİK SKORLARI TABLOSU
# ---------------------------
results = pd.DataFrame({region_col: regions})

# Boyut bazında skor hesaplama
for boyut in index_clean["Boyut"].dropna().unique():
    indicators = index_clean[index_clean["Boyut"] == boyut]
    cols = [z_scores[g] for g in indicators["Gösterge"] if g in z_scores.columns]
    if cols:
        results[f"{boyut} Skoru"] = pd.concat(cols, axis=1).mean(axis=1)

# Genel skor
all_cols = [z_scores[g] for g in index_clean["Gösterge"] if g in z_scores.columns]
if all_cols:
    results["Genel Gelişmişlik Skoru"] = pd.concat(all_cols, axis=1).mean(axis=1)

# ---------------------------
# 6) EXCEL ÇIKTISI
# ---------------------------
with pd.ExcelWriter(output_path) as writer:
    z_scores.to_excel(writer, sheet_name="Z Scores", index=False)
    results.to_excel(writer, sheet_name="Scores", index=False)

print("✅ İşlem tamamlandı. Sonuçlar 'output/development_scores.xlsx' dosyasına kaydedildi.")
print("\nEşleşmeyen göstergeler:")
for g in unmatched:
    print("-", g)
