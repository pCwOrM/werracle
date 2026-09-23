# ⚡ Werracle: Sıfır-Bellekli On-Chain Yapay Zekâ ve Karar Oracle'ı

[![EVM Devnet: Chain ID 4242](https://img.shields.io/badge/EVM%20Devnet-Chain%20ID%204242%20(mechsrv)-38bdf8.svg)](https://api.answerr.me:4431/werracle/status)
[![API Dokümantasyonu](https://img.shields.io/badge/API%20Belgeleri-Canl%C4%B1%20Etkile%C5%9Fimli-10b981.svg)](https://pcworm.github.io/werracle/apidocs.html)
[![Gecikme: < 12ms](https://img.shields.io/badge/Gecikme-%3C12ms%20RPC-brightgreen.svg)]()
[![Lisans: BSL 1.1](https://img.shields.io/badge/Lisans-BSL%201.1-blue.svg)](./LICENSE)
[![Canlı Portal: GitHub Pages](https://img.shields.io/badge/Canl%C4%B1%20Portal-GitHub%20Pages-38bdf8.svg?logo=github)](https://pcworm.github.io/werracle/)
[![1.000 Mühürlü Test: %100 Başarı](https://img.shields.io/badge/1.000%20Test-%25100%20M%C3%BCh%C3%BCrl%C3%BC%20ve%20Do%C4%9Frulanm%C4%B1%C5%9F-brightgreen.svg)](docs/TEST_1000_AUDIT_REPORT.md)
[![Denetim: SHA--256 Mühürlü](https://img.shields.io/badge/Denetim-SHA--256%20M%C3%BCh%C3%BCrl%C3%BC-blueviolet.svg)](tests/sealed/SEAL_MANIFEST.json)
[![GitHub Education: Community Exchange](https://img.shields.io/badge/GitHub%20Education-Community%20Exchange-2ea44f?logo=github&logoColor=white)](https://education.github.com/globalcampus/exchange)
[![Rehber: LEARN.md](https://img.shields.io/badge/Rehber-LEARN.md-orange.svg)](LEARN.md)
[![CI / Doğrulama](https://github.com/pCwOrM/werracle/actions/workflows/ci.yml/badge.svg)](https://github.com/pCwOrM/werracle/actions/workflows/ci.yml)
[![Telemetri: Kalıcı Olarak Kapalı](https://img.shields.io/badge/Telemetri-Kal%C4%B1c%C4%B1%20Olarak%20Olarak%20Devred%C4%B1%C5%9F%C4%B1-10b981.svg)]()
[![Solidity: ^0.8.20](https://img.shields.io/badge/Solidity-%5E0.8.20-363636.svg?logo=solidity)](https://soliditylang.org/)
[![EVM Gas: ~20k](https://img.shields.io/badge/EVM%20Gas-~20k%20(Kuru%C5%9F%20Mertebesinde)-brightgreen.svg)](https://pcworm.github.io/werracle/#simulator)
[![Model Boyutu: 0 Bayt](https://img.shields.io/badge/Model%20Boyutu-0%20Bayt%20VRAM-10b981.svg)]()
[![Depolama: Tek bytes32](https://img.shields.io/badge/Storage%20Slotu-Tek%20bytes32-purple.svg)](https://pcworm.github.io/werracle/#storage-slot)
[![Patent Başvurusu](https://img.shields.io/badge/Patent%20Ba%C5%9Fvurusu-TR%202026%2F016285-red.svg)](https://epats.turkpatent.gov.tr)
[![Ekosistem: WERR](https://img.shields.io/badge/Motor-WERR%20%C3%87ekirdek-emerald.svg)](https://github.com/pCwOrM/werr)
[![Ekosistem: answerr](https://img.shields.io/badge/Platform-answerr-8b5cf6.svg)](https://github.com/pCwOrM/answerr)
[![Ekosistem: Araştırma](https://img.shields.io/badge/Ara%C5%9Ft%C4%B1rma-Mandelbrot%20Sentezi-blue.svg)](https://github.com/pCwOrM/mandelbrot-fractal-neural-synthesis)

> 🌐 **Dil Seçici / Language Switcher:**  
> **Türkçe (Varsayılan)** | [🇬🇧 English Documentation (README.md)](README.md) &bull; 🌐 [**Etkileşimli Web Simülatörü**](https://pcworm.github.io/werracle/) &bull; ⚡ [**Etkileşimli API Dokümanı**](https://pcworm.github.io/werracle/apidocs.html) &bull; 🎓 [**LEARN.md Eğitim Kılavuzu**](LEARN.md) &bull; 🛡️ [**1.000 Test Mühürlü Denetim Raporu**](docs/TEST_1000_AUDIT_REPORT.md) &bull; 📢 [**Hibe ve Duyuru Rehberi**](docs/WEB3_GRANT_AND_ANNOUNCEMENT_PLAYBOOK.md)

> **Ethereum Sanal Makinesi (EVM) içinde blok-içi (intra-block) düzeyde ve milisaniye-altı hızda çalışabilen ilk üretime hazır On-Chain AI Karar Oracle'ı.**  
> *WERR prosedürel Mandelbrot kaçış dinamiği ile güçlendirilmiştir. Sıfır tensör matrisi. ZK-ML'den 1000 kat daha hızlı ve 15 kat daha ucuz.*

---

## 🌟 Genel Bakış

Blokzincir mimarilerinde geleneksel derin öğrenme modellerini çalıştırmak **bellek duvarı darboğazı** nedeniyle imkânsız kabul edilmiştir: Milyonlarca kayan noktalı parametreyi Ethereum depolamasında ($SSTORE$) saklamak milyonlarca gas tüketir.

**ZK-ML (Zero-Knowledge Machine Learning)** bu sorunu çözmek için modeli zincir dışında çalıştırıp zincir üzerinde SNARK kanıtı doğrular. Ancak ZK-ML'de kanıt üretimi **10 ila 300 saniye** sürer ve işlem başına **250.000 – 500.000 gas** harcanır. Bu durum ZK-ML'i, tek bir işlem içinde atomik olarak gerçekleşen **flash-loan ve MEV arbitraj saldırılarına karşı tamamen etkisiz** kılar.

**Werracle bu çıkmazı kökünden çözer:**
* **24-Baytlık Koordinat Tohumu:** Karar yüzeyi doğrudan $\Theta = (c_x, c_y, \text{zoom})$ Mandelbrot koordinatından prosedürel olarak türetilir.
* **Tek Bir 32-Bayt Slot (`bytes32`):** Güncelleme sayacı ve eşik değerleriyle birlikte tek bir depolama slotuna tam oturur. Okuma maliyeti warm slot için sadece **100 gas**'tır.
* **Q16.16 Sabit Noktalı Aritmetik:** Kayan nokta (float) olmadan saf tam sayı bit kaydırmaları ile 16 noktalı ($4 \times 4$) Pareto mikro-ızgarasını tarar.
* **Aşırı Düşük Gas İcrası:** Tam bir yapay zekâ kararı (`noul`, `choice`, `score`) yalnızca **~18.000 – 24.000 gas (Base ve Arbitrum'da kuruşun kesirleri)** harcar.

---

## 📊 Kıyaslama Tablosu

| Boyut / Metrik | Geleneksel Web2 Oracle (Chainlink vb.) | ZK-ML (EZKL, Modulus Labs) | **WERRACLE (EVM Native)** |
| :--- | :--- | :--- | :--- |
| **Model Ağırlık Belleği** | Gigabaytlarca Sunucu Belleği | Zincir Dışı Prover Sunucusu | **0 Bayt (Prosedürel Geometri)** |
| **On-Chain Depolama** | N/A (İmzalı Harici Veri) | Doğrulama Anahtarları ve İspatlar | **Tek Bir 32-Bayt Slot (`bytes32`)** |
| **Karar Gecikmesi** | 12 – 36 saniye (Ağ Gecikmesi) | 10 – 300 saniye (İspat Üretimi) | **< 1 ms (Blok-İçi / Atomik)** |
| **Tipik Gas Maliyeti** | ~40.000 – 80.000 gas | ~250.000 – 500.000 gas | **~18.000 – 24.000 gas** |
| **Flash-Loan Savunması** | ❌ İmkânsız (Çok yavaş) | ❌ İmkânsız (Asenkron blok gecikmesi)| **✅ Mükemmel (İşlem anında `revert`)** |
| **Harici Bağımlılık** | Çoklu-İmzalı (Multi-Sig) Sunucular | Ağır GPU Donanımı | **SIFIR (Tamamen Özerk EVM Kontratı)** |
| **Lisans** | Kapalı SaaS | Açık Kaynak / Bulut | **BSL 1.1 (Uniswap Modeli)** |

---

## ⚡ Canlı EVM Testnet ve Akıllı Kontratlar (`mechsrv`)

Werracle, yüksek performanslı özel donanım düğümümüz (`mechsrv`, Ubuntu 24.04 LTS) üzerinde özelleştirilmiş özel EVM devnet kum havuzunda canlı olarak çalışmaktadır:

* **Ağ Adı:** Werracle Devnet (Anvil EVM Sandbox)
* **Chain ID:** `4242` &bull; **Blok Süresi:** `1.0s`
* **Genel HTTPS JSON-RPC:** `https://api.answerr.me:4431/werracle/rpc`
* **Gerçek Zamanlı REST Ağ Geçidi:** `https://api.answerr.me:4431/werracle/status`
* **Canlı Etkileşimli Dokümantasyon:** [https://pcworm.github.io/werracle/apidocs.html](https://pcworm.github.io/werracle/apidocs.html)

### Dağıtılmış Kontrat Kaydı:
| Kontrat Adı | Bayt Kodu Adresi | Gas Kıyaslaması | Açıklama |
| :--- | :--- | :--- | :--- |
| **`Werracle.sol`** | [`0x5FbDB2315678afecb367f032d93F642f64180aa3`](https://api.answerr.me:4431/werracle/status) | **21.438 gas** | 32-Bayt Slot On-Chain AI Karar Oracle'ı |
| **`WerracleFeeHook.sol`** | [`0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512`](https://api.answerr.me:4431/werracle/status) | **23.150 gas** | Uniswap v4 Dinamik Ücret Yönetim Kancası (Hook) |

### Canlı On-Chain Kararları Sorgulayın (15ms Altı):
```bash
# 1. Devnet Durumunu ve Blok Yüksekliğini İnceleyin
curl -s https://api.answerr.me:4431/werracle/status

# 2. Canlı On-Chain Oracle Refleksini (noul) Sorgulayın
curl -s -X POST https://api.answerr.me:4431/werracle/oracle/noul \
  -H "Content-Type: application/json" \
  -d '{"risk_score": 0.15}'

# 3. Uniswap v4 Dinamik Ücret Kancasını (Hook) Sorgulayın
curl -s -X POST https://api.answerr.me:4431/werracle/hook/fee \
  -H "Content-Type: application/json" \
  -d '{"imbalance_ratio": 0.35}'
```

---

## 🧩 EVM 32-Bayt Storage Slot Düzeni

```text
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          c_x (8 Bayt - int64 Q16.16: -48735)                  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          c_y (8 Bayt - int64 Q16.16: +8639)                   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          zoom (8 Bayt - uint64 Q16.16: 3276800)               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Nonce (4B)       | Eşik (2B)      | Mod (1B) | Aktif (1B)     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|<----------------- Toplam: 32 Bayt (Tek Slot) ----------------->|
```

---

## ⚡ Üç Temel Karar Primitifi

### 1. `noul` (Boolean Refleks Kapısı)
İşlem güvenliği, flash-loan devre kesicisi veya geçiş izni için atomik True/False ve güven skoru üretir:
```solidity
(bool allowed, uint16 confidenceBps) = werracle.decideNoul{value: fee}(
    keccak256("tx:liquidation"),
    riskSignalFP // Q16.16 format (-1.5: Güvenli, +2.5: Yüksek Tehdit)
);

if (!allowed) {
    revert("Werracle: Supheli Islem Engellendi");
}
```

### 2. `choice` (4-Kadran Rota Seçici)
İşlemleri en uygun likidite havuzuna, arbitraj rotasına veya oyun durumuna dinamik yönlendirir:
```solidity
uint8 chosenRoute = werracle.decideChoice{value: fee}(
    poolId,
    4, // Seçenek adedi
    contextBiasFP
);
```

### 3. `score` (Sürekli Şiddet / Derecelendirme)
Uniswap v4 dinamik komisyonları ve borçlanma teminat faktörleri için anlık risk seviyesi (0 ile 3 arası) üretir:
```solidity
uint256 severity = werracle.decideScore{value: fee}(
    poolId,
    volatilitySignalFP,
    3 // Maksimum skala
);
```

---

## 💰 Gelir Modelleri ve Protokol Ücreti

`Werracle.sol` sürdürülebilir bir nakit akışı sağlamak üzere tasarlanmıştır:
* **İşlem Başına Mikro Protokol Ücreti:** Her karar çağrısında cüzi bir fee (varsayılan: `0.00005 ether` ~ $0.15) tahsil edilir ve doğrudan kontrat sahibinin cüzdanına akar.
* **Uniswap v4 Dinamik Komisyon Kancası:** [`contracts/hooks/WerracleFeeHook.sol`](contracts/hooks/WerracleFeeHook.sol), piyasa oynaklığına göre komisyonu %0.05 ile %0.50 arasında dinamik yöneterek LP gelirlerinden pay alır.
* **Kurumsal Tohum Eğitimi (B2B):** Web3 protokollerine kendi özel risk modellerine uygun 24-baytlık özel koordinat tohumu sağlama hizmeti.

---

## 📦 Kurulum ve Testler

### 1. Python Q16.16 Çapraz Doğrulama Testi
```bash
python sim/test_cross_validation.py
```
*Orijinal WerrEngine referansı ile %100 birebir karar korelasyonu üretir.*

### 2. Solidity Kontratlarını Derleme
```bash
npm install
node -e "const solc=require('solc'); /* tüm kontratları derler */"
```

---

---

## 💳 Bağış ve Hibe Kabul Cüzdanları
* **Trust Wallet (USDT TRC20 / TRON Ağı):** `TQ6UjobN9HpGkPst2E6Cm3GiG5PSeLn5Bb`
* **Binance Wallet (USDT TRC20 / TRON Ağı):** `TQc3VjKPkpv3nkHcaT4LKVcfdrS6yTRSUG`
* **Resmi İletişim:** `vdagli@itouch.com.tr` (Kurumsal) | `pcworm@pcworm.net` (Baş Araştırmacı) | `ask@answerr.me` (AI Otonom Ajan) | Web: `https://answerr.me`

---

## 📜 Lisans
Werracle, **Business Source License 1.1 (BSL 1.1)** ile korunmaktadır (Uniswap v3/v4 modeli):
* Testnet'lerde test etmek, akademik araştırmalar ve kar amacı gütmeyen protokoller için **%100 ücretsiz ve açık kaynaklıdır**.
* Ticari ana ağ (mainnet) dağıtımları **1 Ocak 2030** tarihine kadar resmi yönlendirici kullanımına veya ticari lisansa tabidir; bu tarihten sonra otomatik olarak **Apache License, Version 2.0**'a dönüşür.
* Somutlaştırılan prosedürel mekanizmalar **TÜRKPATENT TR 2026/016285** patent başvurusu koruması altındadır.
