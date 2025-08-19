# Python | RFM Müşteri Segmentasyonu - FLO

## Projeye Genel Bakış

**Komut Dosyaları:** [`FLO_RFM_analysis`](https://github.com/gulizsamgar/PYTHON-Customer-Segmentation-with-RFM/blob/b13da35dcf13c4fac476119a0e5590d87592b464/script/FLO_RFM_analysis.py)

**Hedef:** Bu projenin temel hedefi, FLO'nun müşteri veri seti üzerinde RFM (Recency, Frequency, Monetary) analizi yaparak müşterileri anlamlı segmentlere ayırmak ve bu segmentlere yönelik hedefli pazarlama stratejileri geliştirmek için eyleme dönüştürülebilir içgörüler elde etmektir.

**Açıklama:** Proje, 2020-2021 yılları arasındaki OmniChannel müşteri verilerini kullanarak RFM metriklerini hesaplama, skorlama yapma ve önceden tanımlanmış segmentlere (Champions, Loyal Customers, Hibernating vb.) atama adımlarını içermektedir. Ayrıca, belirli pazarlama senaryoları için hedef müşteri kitlelerinin nasıl belirleneceği gösterilmiştir. Tüm RFM segmentasyon süreci, tekrar kullanılabilir bir Python fonksiyonu olarak da sunulmuştur.

Kodlar, projenin her adımını anlaşılır bir şekilde takip etmek amacıyla açıklamalı olarak hazırlanmıştır.

---

## İçerik

Proje aşağıdaki ana görevlerden oluşmaktadır:

*   **GÖREV 1: Veriyi Tanıma ve Hazırlama:** Veri setinin yüklenmesi, genel bilgilerin incelenmesi, eksik değer kontrolü ve yeni değişkenlerin (toplam sipariş sayısı, toplam harcama) oluşturulması.
*   **GÖREV 2: RFM Metriklerinin Hesaplanması:** Recency, Frequency ve Monetary değerlerinin hesaplanması.
*   **GÖREV 3: RF ve RFM Skorlarının Hesaplanması:** RFM metriklerinin skorlanması ve RF/RFM skorlarının oluşturulması.
*   **GÖREV 4: Segmentlerin Oluşturulması:** RF skorlarına göre müşteri segmentlerinin tanımlanması ve atanması.
*   **GÖREV 5: Eyleme Dönüştürülebilir İçgörüler:** Segment özelliklerinin incelenmesi ve belirli pazarlama kampanyaları için hedef kitlelerin belirlenmesi (örneğin, yeni marka tanıtımı ve indirim kampanyası).
*   **BONUS: Tüm Süreci Fonksiyonlaştırma:** RFM segmentasyon adımlarının tekrar kullanılabilir bir Python fonksiyonu içine alınması.

---

## Beceriler

*   Müşteri Segmentasyonu (RFM Analizi) yapma
*   Python ile veri işleme, temizleme ve manipülasyonu (Pandas kütüphanesi)
*   Özellik Mühendisliği
*   Kantilleme (Quantile Analysis) ve Skorlama
*   Düzenli İfadeler (Regex) kullanma
*   Veri Filtreleme ve Seçimi
*   Temel İstatistiksel Analiz (Gruplama ve Özetleme)
*   Fonksiyon Yazma
*   Dosya İşlemleri (CSV kaydetme)

---

## Teknoloji

*   Python (3.x)
*   Python IDE'si PyCharm
*   Google Colab (veya Jupyter Not Defteri)

---

## Araçlar ve Kitaplıklar

*   **Python Programlama:** Temel sözdizimi, fonksiyonlar, koşullu ifadeler, döngüler.
*   **Pandas:** Veri yükleme, işleme, manipülasyonu ve analizi için (DataFrame kullanımı, gruplama, filtreleme, yeni sütun oluşturma).
*   **Numpy:** Sayısal işlemler ve veri manipülasyonu için (Pandas ile entegre kullanımı).
*   **Datetime:** Tarih ve saat verileriyle çalışmak için.

---

## Kullanım

Kodları çalıştırmak için Python 3.x yüklü bir ortamda `.py` dosyasını kullanabilirsiniz.

- Gerekli kütüphaneleri içe aktarın.
- Veri setini **[`flo_data_20k.csv`](https://github.com/gulizsamgar/PYTHON-Customer-Segmentation-with-RFM/blob/0541aa6d4adfb0224e6d1f5b4470ef061f1bddae/dataset/flo_data_20k.csv)** doğru dosya yolunu belirterek yükleyin.
- Her bir veri seti bölümündeki kod hücrelerini sırasıyla çalıştırarak veri hazırlığı, RFM metrikleri hesaplama, skorlama, segmentasyon ve içgörüler adımlarını takip edin.
- Kod çıktılarındaki analizleri ve sonuçları inceleyin.
- Markdown hücrelerindeki açıklamaları okuyarak yapılan işlemlerin amacını ve sonuçlarını anlayın.
- Farklı segmentasyon senaryoları için kodları uyarlayarak kendi analizlerinizi yapın.

---

## Detaylı Açıklamalar

Her görevin detaylı açıklamaları ve kod çıktıları için proje klasöründeki **[`Jupyter Not Defteri dosyasına (.ipynb)`](FLO_RFM_analysis.ipynb)** göz atabilirsiniz.

---

**Not:** Bu projeye temel oluşturan ve FLO veri seti üzerinde SQL ile yapılan müşteri kategorizasyonu ve temel analizlerin yapıldığı önceki çalışmama [buradan](https://github.com/gulizsamgar/SQL-FLO-Customer-Segmentation/blob/6b7eec3938ab83c02226f5e1612118a06e57a6ce/README.md) göz atabilirsiniz.
