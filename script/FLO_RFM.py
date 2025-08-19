
##############################################################################################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
##############################################################################################################################


##############################################################################################################################
# İş Problemi (Business Problem)
##############################################################################################################################

# Bu proje kapsamında, FLO’nun 20.000 müşteriden oluşan veri seti üzerinde RFM (Recency, Frequency, Monetary) analizi uygulanmıştır. 
# Çalışmanın amacı, müşterilerin alışveriş davranışlarını analiz ederek sadakat seviyelerini ölçmek, hedef pazarlama stratejileri oluşturmak ve müşteri segmentasyonu yapmaktır. 
# FLO müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri belirlemek istiyor. Buna yönelik olarak müşterilerin davranışları tanımlanacak ve bu davranış öbeklenmelerine göre gruplar oluşturulacak.


##############################################################################################################################
# Veri Seti Bilgisi
##############################################################################################################################

# Veri seti son alışverişlerini 2020 - 2021 yıllarında OmniChannel(hem online hem offline alışveriş yapan) olarak yapan müşterilerin geçmiş alışveriş davranışlarından
# elde edilen bilgilerden oluşmaktadır.

# master_id: Eşsiz müşteri numarası
# order_channel : Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, ios, Desktop, Mobile, Offline)
# last_order_channel : En son alışverişin yapıldığı kanal
# first_order_date : Müşterinin yaptığı ilk alışveriş tarihi
# last_order_date : Müşterinin yaptığı son alışveriş tarihi
# last_order_date_online : Muşterinin online platformda yaptığı son alışveriş tarihi
# last_order_date_offline : Muşterinin offline platformda yaptığı son alışveriş tarihi
# order_num_total_ever_online : Müşterinin online platformda yaptığı toplam alışveriş sayısı
# order_num_total_ever_offline : Müşterinin offline'da yaptığı toplam alışveriş sayısı
# customer_value_total_ever_offline : Müşterinin offline alışverişlerinde ödediği toplam ücret
# customer_value_total_ever_online : Müşterinin online alışverişlerinde ödediği toplam ücret
# interested_in_categories_12 : Müşterinin son 12 ayda alışveriş yaptığı kategorilerin listesi


##############################################################################################################################
# Kütüphanelerin İçe Aktarılması ve Görüntü Ayarları
##############################################################################################################################

import pandas as pd
import datetime as dt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.set_option('display.width',1000)


##############################################################################################################################
# GÖREV 1: VERİYİ TANIMA VE HAZIRLAMA
##############################################################################################################################

###############################################################
# 1. Veri setini içe aktar
###############################################################

# CSV dosyasını pandas DataFrame'ine oku.
df_ = pd.read_csv("CRM_Analitigi/Dataset/flo_data_20K.csv")
# Orijinal DataFrame'in bir kopyasını oluştur.
df = df_.copy()

###############################################################
# 2. Veri keşfi
###############################################################

# Veri setinin ilk 10 satırını yazdır.
print("\nFirst 10 rows:")
print(df.head(10), "\n")

# Sütun isimlerini yazdır.
print("\nColumn names:")
print(df.columns, "\n")

# Veri setinin boyutlarını (satır ve sütun sayısı) yazdır.
print("\nShape of dataset (rows, columns):", df.shape, "\n")

# Betimsel istatistikleri (sayısal sütunlar için) yazdır.
print("\nDescriptive statistics:")
print(df.describe().T, "\n")

# Her sütundaki eksik (NaN) değerlerin sayısını yazdır.
print("\nMissing values by column:")
print(df.isnull().sum(), "\n")

# Veri setinin sütunları, eksik olmayan değer sayısı ve veri tipleri hakkında bilgi yazdır.
print("\nData types:")
print(df.info(), "\n")

###############################################################
# 3. Özellik Mühendisliği: Müşteri bazında toplam sipariş sayısı ve toplam harcama
###############################################################

df["order_num_total"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["customer_value_total"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

###############################################################
# 4. Tarih değişkenlerini datetime tipine çevir
###############################################################

# Sütun isimleri içinde "date" geçenleri seç.
date_columns = df.columns[df.columns.str.contains("date")]
# Seçilen sütunları datetime tipine çevir.
df[date_columns] = df[date_columns].apply(pd.to_datetime)

###############################################################
# 5. Kanal bazında dağılım
###############################################################

# order_channel sütununa göre gruplama yap.
print("\nDistribution by order channel:")
# Her kanal için müşteri sayısı, toplam sipariş sayısı),toplam harcama hesapla.
print(df.groupby("order_channel").agg({"master_id": "count",
                                       "order_num_total": "sum",
                                       "customer_value_total": "sum"}), "\n")

###############################################################
# 6. En çok gelir getiren ilk 10 müşteri
###############################################################

# "customer_value_total" sütununa göre DataFrame'i azalan sırada sırala.
# İlk 10 satırı seç.
print("\nTop 10 customers by total revenue:")
print(df.sort_values("customer_value_total", ascending=False).head(10), "\n")

###############################################################
# 7. En çok sipariş veren ilk 10 müşteri
###############################################################

# "order_num_total" sütununa göre DataFrame'i azalan sırada sırala.
# İlk 10 satırı seç.
print("\nTop 10 customers by total number of orders:")
print(df.sort_values("order_num_total", ascending=False).head(10), "\n")f



##############################################################################################################################
# GÖREV 2: RFM METRİKLERİNİN HESAPLANMASI
##############################################################################################################################

###############################################################
# 1. Analiz tarihi: Son alışveriş tarihinden 2 gün sonrası
###############################################################

# Veri setindeki son sipariş tarihini bul.
print("\nLast order date in dataset:")
print(df["last_order_date"].max())  # Veri setindeki son tarih 2021-05-30

# Analiz tarihini belirle (son sipariş tarihinden 2 gün sonrası).
analysis_date = dt.datetime(2021, 6, 1)

###############################################################
# 2. RFM dataframe oluşturma
###############################################################

# RFM metriklerini saklamak için boş bir DataFrame oluştur.
rfm = pd.DataFrame()
# Müşteri ID'lerini RFM DataFrame'ine kopyala.
rfm["customer_id"] = df["master_id"]

# Recency (Yenilik): Analiz tarihi ile son sipariş tarihi arasındaki gün farkını hesapla.
rfm["recency"] = (analysis_date - df["last_order_date"]).dt.days

# Frequency (Sıklık): Toplam sipariş sayısını kullan.
rfm["frequency"] = df["order_num_total"]

# Monetary (Parasal Değer): Toplam harcama değerini kullan.
rfm["monetary"] = df["customer_value_total"]

# Oluşturulan RFM DataFrame'inin ilk 5 satırını yazdır.
print("\nFirst 5 rows of RFM dataframe:")
print(rfm.head(), "\n")



##############################################################################################################################
# GÖREV 3: RF VE RFM SKORLARININ HESAPLANMASI
##############################################################################################################################

###############################################################
# 1. Recency, Frequency, Monetary skorlarının hesaplanması
###############################################################

# Recency skorunu hesapla: Değerleri 5 gruba ayır ve 5 en iyi (en düşük recency) olacak şekilde etiketle.
rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])
# Frequency skorunu hesapla: Değerlerin rank'ını al, 5 gruba ayır ve 5 en iyi (en yüksek frequency) olacak şekilde etiketle.
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
# Monetary skorunu hesapla: Değerleri 5 gruba ayır ve 5 en iyi (en yüksek monetary) olacak şekilde etiketle.
rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])

###############################################################
# 2. RF_SCORE oluşturma
###############################################################

# Recency ve Frequency skorlarını birleştirerek RF_SCORE oluştur.
rfm["RF_SCORE"] = (rfm["recency_score"].astype(str) +
                   rfm["frequency_score"].astype(str))

###############################################################
# 3. RFM_SCORE oluşturma
###############################################################

# Recency, Frequency ve Monetary skorlarını birleştirerek RFM_SCORE oluştur.
rfm["RFM_SCORE"] = (rfm["recency_score"].astype(str) +
                    rfm["frequency_score"].astype(str) +
                    rfm["monetary_score"].astype(str))

# RFM skorları eklenmiş DataFrame'in ilk 5 satırını yazdır.
print("\nFirst 5 rows of RFM with scores:\n")
print(rfm.head())



##############################################################################################################################
# GÖREV 4: SEGMENTLERİN OLUŞTURULMASI
##############################################################################################################################

###############################################################
# 1. Segment tanımlamaları
###############################################################

# RF skorlarına karşılık gelen segment isimlerini tanımlayan bir sözlük oluştur.
# Anahtarlar regex desenleri, değerler ise segment isimleridir.
seg_map = {
    r"[1-2][1-2]": "hibernating", # Düşük Recency ve Düşük Frequency
    r"[1-2][3-4]": "at_Risk",     # Düşük Recency, Orta-Yüksek Frequency
    r"[1-2]5": "cant_loose",      # Düşük Recency, Yüksek Frequency
    r"3[1-2]": "about_to_sleep",  # Orta Recency, Düşük Frequency
    r"33": "need_attention",      # Orta Recency, Orta Frequency
    r"[3-4][4-5]": "loyal_customers", # Orta-Yüksek Recency, Yüksek Frequency
    r"41": "promising",           # Yüksek Recency, Düşük Frequency (Yeni olabilirler veya tek seferlik)
    r"51": "new_customers",       # En Yüksek Recency, Düşük Frequency (Yeni müşteriler)
    r"[4-5][2-3]": "potential_loyalists", # Yüksek Recency, Orta Frequency
    r"5[4-5]": "champions"        # En Yüksek Recency, En Yüksek Frequency
}

# rfm DataFrame'ine "segment" adında yeni bir sütun ekle.
# RF_SCORE sütunundaki değerleri seg_map sözlüğünü kullanarak segment isimleriyle değiştir.
# regex=True parametresi, anahtarların regex desenleri olarak kullanılmasını sağlar.
rfm["segment"] = rfm["RF_SCORE"].replace(seg_map, regex=True)

# Segment bilgisi eklenmiş DataFrame'in ilk 5 satırını yazdır.
print("\nFirst 5 rows of RFM with segments:\n")
print(rfm.head())

# First 5 rows of RFM with segments:
#                            customer_id  recency  frequency  monetary recency_score frequency_score monetary_score RF_SCORE RFM_SCORE          segment
# 0  cc294636-19f0-11eb-8d74-000d3a38a36f       95       5.00    939.37             3               4              4       34       344  loyal_customers
# 1  f431bd5a-ab7b-11e9-a2fc-000d3a38a36f      105      21.00   2013.55             3               5              5       35       355  loyal_customers
# 2  69b69676-1a40-11ea-941b-000d3a38a36f      186       5.00    585.32             2               4              3       24       243          at_Risk
# 3  1854e56c-491f-11eb-806e-000d3a38a36f      135       2.00    121.97             3               1              1       31       311   about_to_sleep
# 4  d6ea1074-f1f5-11e9-9346-000d3a38a36f       86       2.00    209.98             3               1              1       31       311   about_to_sleep



##############################################################################################################################
# GÖREV 5: EYLEME DÖNÜŞTÜRÜLEBİLİR İÇGÖRÜLER
##############################################################################################################################

###############################################################
# 1. Segmentlerin recency, frequency, monetary ortalamaları
###############################################################

print("\nSegment statistics (mean values and counts):\n")
# RFM DataFrame'inden segment, recency, frequency ve monetary sütunlarını seç.
# "segment" sütununa göre gruplama yap.
# Her grup için recency, frequency ve monetary sütunlarının ortalamasını (mean) ve sayısını (count) hesapla.
print(rfm[["segment", "recency", "frequency", "monetary"]]
      .groupby("segment").agg(["mean", "count"]), "\n")


#   Segment statistics (mean values and counts):

#                     recency       frequency       monetary      
#                        mean count      mean count     mean count
# segment                                                         
# about_to_sleep       113.79  1629      2.40  1629   359.01  1629
# at_Risk              241.61  3131      4.47  3131   646.61  3131
# cant_loose           235.44  1200     10.70  1200  1474.47  1200
# champions             17.11  1932      8.93  1932  1406.63  1932
# hibernating          247.95  3604      2.39  3604   366.27  3604
# loyal_customers       82.59  3361      8.37  3361  1216.82  3361
# need_attention       113.83   823      3.73   823   562.14   823
# new_customers         17.92   680      2.00   680   339.96   680
# potential_loyalists   37.16  2938      3.30  2938   533.18  2938
# promising             58.92   647      2.00   647   335.67   647 


###############################################################
# 2.a Yeni kadın ayakkabı markası için hedef müşteri seçimi
###############################################################
# a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri tercihlerinin üstünde. Bu nedenle markanın
# tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçeilmek isteniliyor. Bu müşterilerin sadık  ve
# kadın kategorisinden alışveriş yapan kişiler olması planlandı. Müşterilerin id numaralarını csv dosyasına yeni_marka_hedef_müşteri_id.cvs
# olarak kaydediniz

# "champions" ve "loyal_customers" segmentlerindeki müşteri ID'lerini seç.
target_segments_customer_ids = rfm[rfm["segment"].isin(["champions", "loyal_customers"])]["customer_id"]
# Seçilen segmentlerdeki ve "KADIN" kategorisiyle ilgilenen müşteri ID'lerini filtrele.
cust_ids = df[(df["master_id"].isin(target_segments_customer_ids)) &
              (df["interested_in_categories_12"].str.contains("KADIN"))]["master_id"]

# Hedef müşteri ID'lerini CSV dosyasına kaydet.
cust_ids.to_csv("yeni_marka_hedef_müşteri_id.csv", index=False)
print("\nNew brand target customer IDs saved to yeni_marka_hedef_müşteri_id.csv")
print("Number of customers:", cust_ids.shape[0])


###############################################################
# 2.b Erkek ve Çocuk ürünlerinde indirim için hedef müşteri seçimi
###############################################################
# b. Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi müşterilerden olan ama uzun süredir
# alışveriş yapmayan ve yeni gelen müşteriler özel olarak hedef alınmak isteniliyor. Uygun profildeki müşterilerin id'lerini csv dosyasına indirim_hedef_müşteri_ids.csv
# olarak kaydediniz.

# "cant_loose", "hibernating", "new_customers" segmentlerindeki müşteri ID'lerini seç.
target_segments_customer_ids = rfm[rfm["segment"].isin(["cant_loose", "hibernating", "new_customers"])]["customer_id"]
# Seçilen segmentlerdeki ve "ERKEK" veya "COCUK" kategorileriyle ilgilenen müşteri ID'lerini filtrele.
cust_ids = df[(df["master_id"].isin(target_segments_customer_ids)) &
              ((df["interested_in_categories_12"].str.contains("ERKEK")) |
               (df["interested_in_categories_12"].str.contains("COCUK")))]["master_id"]

# Hedef müşteri ID'lerini CSV dosyasına kaydet.
cust_ids.to_csv("indirim_hedef_müşteri_ids.csv", index=False)
print("\nDiscount campaign target customer IDs saved to indirim_hedef_müşteri_ids.csv")
print("Number of customers:", cust_ids.shape[0])



##############################################################################################################################
# BONUS: TÜM SÜRECİ FONKSİYONLAŞTIRMA
##############################################################################################################################

def create_rfm(dataframe):
    """RFM segmentasyon veri çerçevesi oluşturur"""

    # Veri hazırlama: Toplam sipariş sayısı ve toplam harcama hesapla
    dataframe["order_num_total"] = (dataframe["order_num_total_ever_online"] +
                                    dataframe["order_num_total_ever_offline"])
    dataframe["customer_value_total"] = (dataframe["customer_value_total_ever_offline"] +
                                         dataframe["customer_value_total_ever_online"])
    
    # Tarih değişkenlerini datetime tipine çevir
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)

    # Analiz tarihi: Son alışveriş tarihinden 2 gün sonrası
    analysis_date = dt.datetime(2021, 6, 1)

    # RFM metrikleri: Recency, Frequency ve Monetary değerlerini hesapla
    rfm = pd.DataFrame()
    rfm["customer_id"] = dataframe["master_id"]
    rfm["recency"] = (analysis_date - dataframe["last_order_date"]).dt.days # Gün farkını hesapla
    rfm["frequency"] = dataframe["order_num_total"] # Toplam sipariş sayısı
    rfm["monetary"] = dataframe["customer_value_total"] # Toplam harcama

    # Skorlar: Recency, Frequency, Monetary skorlarını hesapla ve birleştir
    rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1]) # Recency skoru (ters)
    rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]) # Frequency skoru (rank ile)
    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5]) # Monetary skoru
    rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str)) # RF skoru
    rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str) + rfm['monetary_score'].astype(str)) # RFM skoru

    # Segmentler: RF_SCORE'a göre müşteri segmentlerini ata
    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_Risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }
    rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True) # Segment isimlerini ata

    # İstenen sütunları içeren RFM DataFrame'ini döndür
    return rfm[["customer_id", "recency", "frequency", "monetary", "RF_SCORE", "RFM_SCORE", "segment"]]

# Fonksiyonu çalıştır ve sonucu yeni bir DataFrame'e ata
rfm_df = create_rfm(df)
print("\nFinal RFM dataframe created with segments:\n")
print(rfm_df.head(),"\n")
