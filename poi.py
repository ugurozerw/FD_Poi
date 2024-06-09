import matplotlib
matplotlib.use('Agg')  # GUI backend olmadan çizim yapmak için
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import poisson

# İşlem türlerine göre günlük ortalama sahtecilik sayıları (lambda)
average_frauds = {
    'credit_card': 2,   # Kredi kartı işlemlerinde günlük ortalama 2 sahtecilik
    'bank_transfer': 1, # Banka transferlerinde günlük ortalama 1 sahtecilik
    'atm': 0.5          # ATM işlemlerinde günlük ortalama 0.5 sahtecilik
}

# Anomali olarak kabul edilecek olasılık eşiği
anomaly_threshold = 0.01

# Grafik çizdirme
def plot_poisson_distribution(transaction_type, lambda_):
    # 0'dan 15'e kadar sahtecilik sayıları (genellikle Poisson dağılımı için yeterli bir aralık)
    k_values = np.arange(0, 16)
    # Poisson PMF değerlerini hesapla
    probabilities = poisson.pmf(k_values, lambda_)
    
    plt.figure(figsize=(8, 4))
    plt.bar(k_values, probabilities, color='skyblue', alpha=0.7, label=f'λ = {lambda_}')
    plt.axhline(y=anomaly_threshold, color='red', linestyle='--', label=f'Anomaly Threshold (P = {anomaly_threshold})')
    
    # Anomalileri işaretle
    for k, prob in zip(k_values, probabilities):
        if prob < anomaly_threshold:
            plt.scatter(k, prob, color='red', edgecolor='black', zorder=5)
            plt.text(k, prob, f'{prob:.4f}', fontsize=8, ha='center', va='bottom', color='darkred')
    
    plt.title(f'Poisson Distribution - {transaction_type.capitalize()} Transactions')
    plt.xlabel('Number of Frauds in a Day')
    plt.ylabel('Probability')
    plt.xticks(k_values)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Grafik dosyası olarak kaydet
    plt.savefig(f"{transaction_type}_poisson_distribution.png")
    plt.close()

# Her işlem türü için olasılıkları hesaplayıp grafik çizdir
for transaction_type, lambda_ in average_frauds.items():
    plot_poisson_distribution(transaction_type, lambda_)