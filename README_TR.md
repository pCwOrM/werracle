<p align="center">
  <img src="assets/werracle_logo_oracle.svg" alt="Werracle Logo Amblemi" width="160" height="160" />
</p>

# ⚡ Werracle: Sıfır-Bellekli On-Chain Yapay Zekâ ve Karar Oracle'ı

[![EVM Devnet: Chain ID 4242](https://img.shields.io/badge/EVM%20Devnet-Chain%20ID%204242%20(api.answerr.me)-38bdf8.svg)](https://api.answerr.me/werracle/status)
[![API Dokümantasyonu](https://img.shields.io/badge/API%20Belgeleri-Canl%C4%B1%20Etkile%C5%9Fimli-10b981.svg)](https://werracle.io/apidocs.html)
[![Gecikme: < 12ms](https://img.shields.io/badge/Gecikme-%3C12ms%20RPC-brightgreen.svg)]()
[![Lisans: BSL 1.1](https://img.shields.io/badge/Lisans-BSL%201.1-blue.svg)](./LICENSE)
[![Web3 Protokol: werracle.io](https://img.shields.io/badge/Web3%20Protokol-werracle.io-f59e0b.svg?logo=cloudflare&logoColor=white)](https://werracle.io/)
[![Kurumsal Portal: werracle.com](https://img.shields.io/badge/Kurumsal%20Portal-werracle.com-2b3bd1.svg?logo=cloudflare&logoColor=white)](https://werracle.com/)
[![Akademik Portal: werr.io](https://img.shields.io/badge/Akademik%20Portal-werr.io-0284c7.svg?logo=cloudflare&logoColor=white)](https://werr.io/)
[![Aurora Sözleşmesi: 0x1d7Ae9E1](https://img.shields.io/badge/Aurora%20S%C3%B6zle%C5%9Fmesi-0x1d7Ae9E1...caBaF-78D64B.svg)](https://explorer.testnet.aurora.dev/address/0x1d7Ae9E1dDDA805539d9e225425804Ef8B9caBaF)
[![Bulut Kasası: R2 Aktif](https://img.shields.io/badge/Bulut%20Kasas%C4%B1-Cloudflare%20R2%20Aktif-f38020.svg?logo=cloudflare&logoColor=white)](https://werracle.com/)
[![NSF ICARM Rekoru](https://img.shields.io/badge/NSF%20ICARM-230%20Do%C4%9Frulanm%C4%B1%C5%9F%20E%C4%9Fri-blue)](https://elliptic-rank.icarm.cloud/user/114)
[![1.000 Mühürlü Test: %100 Başarı](https://img.shields.io/badge/1.000%20Test-%25100%20M%C3%BCh%C3%BCrl%C3%BC%20ve%20Do%C4%9Frulanm%C4%B1%C5%9F-brightgreen.svg)](docs/TEST_1000_AUDIT_REPORT.md)
[![Denetim: SHA--256 Mühürlü](https://img.shields.io/badge/Denetim-SHA--256%20M%C3%BCh%C3%BCrl%C3%BC-blueviolet.svg)](tests/sealed/SEAL_MANIFEST.json)
[![GitHub Education: Community Exchange](https://img.shields.io/badge/GitHub%20Education-Community%20Exchange-2ea44f?logo=github&logoColor=white)](https://education.github.com/globalcampus/exchange)
[![Rehber: LEARN.md](https://img.shields.io/badge/Rehber-LEARN.md-orange.svg)](LEARN.md)
[![CI / Doğrulama](https://github.com/pCwOrM/werracle/actions/workflows/ci.yml/badge.svg)](https://github.com/pCwOrM/werracle/actions/workflows/ci.yml)
[![Telemetri: Kalıcı Olarak Kapalı](https://img.shields.io/badge/Telemetri-Kal%C4%B1c%C4%B1%20Olarak%20Olarak%20Devred%C4%B1%C5%9F%C4%B1-10b981.svg)]()
[![Solidity: ^0.8.20](https://img.shields.io/badge/Solidity-%5E0.8.20-363636.svg?logo=solidity)](https://soliditylang.org/)
[![Cairo: 2.8+ (Sierra)](https://img.shields.io/badge/Starknet-Cairo%202.8%2B%20(Sierra)-ec796b.svg)](cairo/)
[![Starknet Adım: ~1.420](https://img.shields.io/badge/CairoVM-~1.420%20Ad%C4%B1m%20(STARK--Native)-ec796b.svg)](docs/STARKNET_ARCHITECTURE_AND_SEED_GRANT_ROADMAP.md)
[![Starknet DeFi: Ekubo Eklentisi](https://img.shields.io/badge/Starknet%20DeFi-Ekubo%20LVR%20Extension-blueviolet.svg)](cairo/src/ekubo_werracle_extension.cairo)
[![EVM Gas: ~20k](https://img.shields.io/badge/EVM%20Gas-~20k%20(Kuru%C5%9F%20Mertebesinde)-brightgreen.svg)](https://werracle.io/#simulator)
[![Model Boyutu: 0 Bayt](https://img.shields.io/badge/Model%20Boyutu-0%20Bayt%20VRAM-10b981.svg)]()
[![Depolama: Tek bytes32 / felt252](https://img.shields.io/badge/Storage%20Slotu-Tek%20bytes32%20%7C%20felt252-purple.svg)](https://werracle.io/#storage-slot)
[![Patent Başvurusu](https://img.shields.io/badge/Patent%20Ba%C5%9Fvurusu-TR%202026%2F016285-red.svg)](https://epats.turkpatent.gov.tr)
[![Ekosistem: WERR](https://img.shields.io/badge/Motor-WERR%20%C3%87ekirdek-emerald.svg)](https://github.com/pCwOrM/werr)
[![Ekosistem: answerr](https://img.shields.io/badge/Platform-answerr-8b5cf6.svg)](https://github.com/pCwOrM/answerr)
[![Ekosistem: Araştırma](https://img.shields.io/badge/Ara%C5%9Ft%C4%B1rma-Mandelbrot%20Sentezi-blue.svg)](https://github.com/pCwOrM/mandelbrot-fractal-neural-synthesis)
[![Ekosistem: WerrSoma Konnektom](https://img.shields.io/badge/Konnektom-WerrSoma%20158K%20N%C3%B6ron-00f0ff.svg)](https://github.com/Lexovian/WerrSoma)
[![Konnektom DOI](https://img.shields.io/badge/WerrSoma%20DOI-10.5281%2Fzenodo.22996625-024dad.svg)](https://doi.org/10.5281/zenodo.22996625)
[![WerrSoma Portalı](https://img.shields.io/badge/WerrSoma%20Portal-werrsoma.answerr.me-00f0ff.svg)](https://werrsoma.answerr.me/)
[![Ekosistem: WERRobotics](https://img.shields.io/badge/WERRobotics-Arduino%20%26%20Edge%20AI-ff9100.svg?logo=arduino&logoColor=white)](https://github.com/pCwOrM/WERRobotics)
[![NEAR Protocol](https://img.shields.io/badge/NEAR%20Protocol-Intents%20%26%20Aurora%20EVM-00EC97.svg?logo=near&logoColor=black)](near/README.md)
[![Aurora EVM](https://img.shields.io/badge/Aurora%20EVM-Chain%20ID%201313161555-78D64B.svg)](near/README.md)
[![arXiv: 2609.30719 (Werracle)](https://img.shields.io/badge/arXiv-2609.30719%20%5Bcs.CR%5D-b31b1b.svg)](https://arxiv.org/abs/2609.30719)
[![SSRN: 7626279](https://img.shields.io/badge/SSRN-7626279-002f6c.svg?logo=elsevier)](https://ssrn.com/abstract=7626279)
[![arXiv DOI: 10.48550/arXiv.2609.30719](https://img.shields.io/badge/arXiv%20DOI-10.48550%2FarXiv.2609.30719-b31b1b.svg)](https://doi.org/10.48550/arXiv.2609.30719)
[![arXiv: 2609.25498 (WERR)](https://img.shields.io/badge/arXiv-2609.25498%20%5Bcs.AI%5D-b31b1b.svg)](https://arxiv.org/abs/2609.25498)
[![Lean 4 Formel İspat: Zenodo 22974544](https://img.shields.io/badge/Paper%205%20DOI-10.5281%2Fzenodo.22974544-024dad.svg)](https://doi.org/10.5281/zenodo.22974544)
[![Lean 4 Formel Makale: arXiv 2609.33066](https://img.shields.io/badge/Formel%20Makale-arXiv%3A2609.33066%20(Lean4)-b31b1b.svg)](https://arxiv.org/abs/2609.33066)
[![Formel Doğrulama: Lean 4 (0 Sorry)](https://img.shields.io/badge/Formel%20Doğrulama-Lean%204%20(0%20Sorry)-9333ea.svg)](formal_proofs/WerracleProof.lean)
[![Zenodo DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.22942598-024dad.svg)](https://doi.org/10.5281/zenodo.22942598)
[![Makale: Kamera-Hazır PDF](https://img.shields.io/badge/Makale%20v2.0-Kamera--Haz%C4%B1r-emerald.svg)](https://arxiv.org/pdf/2609.30719)

> 🌐 **Dil Seçici / Language Switcher:**  
> **Türkçe (Varsayılan)** | [🇬🇧 English Documentation (README.md)](README.md) &bull; 🐺 [**Starknet (Cairo 2 / Sierra) Mimarisi ve Yol Haritası**](docs/STARKNET_ARCHITECTURE_AND_SEED_GRANT_ROADMAP.md) &bull; 🟢 [**NEAR Intents ve Aurora Mimarisi**](near/README.md) &bull; 📄 [**Resmi arXiv Makalesi (2609.30719)**](https://arxiv.org/abs/2609.30719) &bull; 🌐 [**Etkileşimli Web Simülatörü**](https://werracle.io/) &bull; ⚡ [**Etkileşimli API Dokümanı**](https://werracle.io/apidocs.html) &bull; 🎓 [**LEARN.md Eğitim Kılavuzu**](LEARN.md) &bull; 🛡️ [**1.000 Test Mühürlü Denetim Raporu**](docs/TEST_1000_AUDIT_REPORT.md) &bull; 📢 [**Hibe ve Duyuru Rehberi**](docs/WEB3_GRANT_AND_ANNOUNCEMENT_PLAYBOOK.md)

> **Hem Ethereum Sanal Makinesi (`EVM / Solidity`) hem de Starknet (`Cairo 2.x / Sierra`) içinde blok-içi (intra-block) düzeyde ve milisaniye-altı hızda çalışabilen ilk üretime hazır On-Chain AI Karar Oracle'ı.**  
> *WERR prosedürel Mandelbrot kaçış dinamiği ile güçlendirilmiştir. Sıfır tensör matrisi. ZK-ML'den 1000 kat daha hızlı ve 15 kat daha ucuz — Starknet üzerinde %100 doğal STARK kanıt geçerliliği ile.*  
> 📄 **Resmi Yayın:** *"Werracle: Sub-Cent Intra-Block AI Reflex Oracles and Flash-Loan Circuit Breakers for EVM Smart Contracts"* — [**arXiv:2609.30719 [cs.CR, cs.AI, cs.DC]**](https://arxiv.org/abs/2609.30719) │ [**SSRN: 7626279 (Elsevier)**](https://ssrn.com/abstract=7626279) | DOI: [`10.48550/arXiv.2609.30719`](https://doi.org/10.48550/arXiv.2609.30719) | Zenodo: [`10.5281/zenodo.22942598`](https://doi.org/10.5281/zenodo.22942598)  
> 📡 **Werracle Radar (Canlı DaaS & Tasfiye Gözlemevi):** [radar.werracle.com](https://radar.werracle.com) │ [Hugging Face Veri Seti (v1.2)](https://huggingface.co/datasets/pCwOrM/werracle-oev-liquidation-dataset-2026) │ [Zenodo Veri Seti DOI: 10.5281/zenodo.23623588](https://doi.org/10.5281/zenodo.23623588) │ [SSRN: 7668638](https://papers.ssrn.com/abstract=7668638)  
> 💼 **Yatırımcı Sunumları (PDF):** [Radar DaaS (EN)](docs/Werracle_Radar_Investor_Pitch_Deck.pdf) │ [Radar DaaS (TR)](docs/Werracle_Radar_Yatirimci_Sunumu_TR.pdf) │ [Tüm Ekosistem (EN)](docs/Werracle_Product_Investor_Pitch_Deck_EN.pdf) │ [Tüm Ekosistem (TR)](docs/Werracle_Product_Investor_Pitch_Deck_TR.pdf)

<p align="center">
  <img src="assets/twitter_lean4_tesla_gauntlet.png" alt="Werracle Lean 4 Formel Doğrulama & Tesla 3-6-9 Harmonikleri" width="100%">
</p>

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

## ⚡ Canlı EVM Testnet ve Akıllı Kontratlar (`api.answerr.me`)

Werracle, yüksek performanslı özel donanım düğümümüz (`api.answerr.me`, Ubuntu 24.04 LTS) üzerinde özelleştirilmiş özel EVM devnet kum havuzunda canlı olarak çalışmaktadır:

* **Ağ Adı:** Werracle Devnet (Anvil EVM Sandbox)
* **Chain ID:** `4242` &bull; **Blok Süresi:** `1.0s`
* **Genel HTTPS JSON-RPC:** `https://api.answerr.me/werracle/rpc`
* **Gerçek Zamanlı REST Ağ Geçidi:** `https://api.answerr.me/werracle/status`
* **Canlı Etkileşimli Dokümantasyon:** [https://werracle.io/apidocs.html](https://werracle.io/apidocs.html)

### Dağıtılmış Kontrat Kaydı (v2.0 ve v1.0 Tabanı):
| Kontrat Adı | Bayt Kodu Adresi | Gas Kıyaslaması | Açıklama |
| :--- | :--- | :--- | :--- |
| **`WerracleTripodZMod9.sol`** | [`0x0a95887dBa2783E1E445bB4D3A9a1f7cB3152d04`](https://api.answerr.me/werracle/status) | **22.557 gas** | **v2.0 Amiral Gemisi Çekirdeği**: Seyreltilmiş Çok Ölçekli Tripod ve $\mathbb{Z} \pmod 9$ Erken Kaçış |
| **`BlockchainResonanceMatrix.sol`** | Gömülü Baytkodu Kütüphanesi | **3.821 gas** | **v2.0 Anlamsal Matris**: 5 Sütunda 40 On-Chain Belirteç (0 SLOAD) |
| **`Werracle.sol`** | [`0x5FbDB2315678afecb367f032d93F642f64180aa3`](https://api.answerr.me/werracle/status) | **21.438 gas** | **v1.0 Kanonik Tabanı**: 16-noktalı Pareto mikro-ızgarası (arXiv / Zenodo referansı) |
| **`WerracleFeeHook.sol`** | [`0xdef5Ad647Af159D27cd111007e4CCD1fDE9d4006`](https://api.answerr.me/werracle/status) | **36.739 gas** | Uniswap v4 Dinamik Volatilite Ücret Kancası (Hook) |

### Canlı On-Chain Kararları Sorgulayın (15ms Altı):
```bash
# 1. Devnet Durumunu ve Blok Yüksekliğini İnceleyin
curl -s https://api.answerr.me/werracle/status

# 2. Canlı On-Chain Oracle Refleksini (noul) Sorgulayın
curl -s -X POST https://api.answerr.me/werracle/oracle/noul \
  -H "Content-Type: application/json" \
  -d '{"risk_score": 0.15}'

# 3. Uniswap v4 Dinamik Ücret Kancasını (Hook) Sorgulayın
curl -s -X POST https://api.answerr.me/werracle/hook/fee \
  -H "Content-Type: application/json" \
  -d '{"imbalance_ratio": 0.35}'
```

---

## 🚀 Werracle v2.0: Çok Ölçekli Seyreltilmiş Tripod ve $\mathbb{Z} \pmod 9$ Rezonansı

Werracle v2.0, canlı EVM üzerinde test edilmiş ve kanıtlanmış iki büyük algoritmik yenilik sunar:

### 1. Çok Ölçekli Harmonik Tripod (Seyreltilmiş 12-Noktalı Izgara)
Tek bir odak düzlemi yerine, v2.0 üç harmonik yakınlaştırma düzlemi üzerinden örnekleme yapar:
* **Geniş Ufuk ($0.60\times$):** Makro gürültüyü filtreler ve sınır dalgalanmalarını stabilize eder (Ağırlık: $0.25$).
* **Doğal Odak ($1.00\times$):** Kanonik karar düzlemi (Ağırlık: $0.50$).
* **Derin Kırılma ($1.60\times$):** Çatallanma sınırındaki ince fraktal iplikçikleri ayrıştırır (Ağırlık: $0.25$).  
Her düzlemde 4 ortogonal kardinal nokta ($3 \times 4 = 12$ nokta) taranarak, v1.0'ın 16 noktalı düz ızgarasından daha az işlemle 3 ölçekli harmonik derinlik elde edilir.

### 2. $\mathbb{Z} \pmod 9$ Modüler Rezonans Erken Kaçış Dinamiği
Lean 4 formel cebirsel halka yapısına (`ZMod 9`) dayalı modüler kilometre taşlarında ($n \in \{3, 6, 9\}$) kaçış kontrolü yapılır. Flaş saldırılar ve ani şoklar 3. adımda hızla kaçarak ortalama döngü derinliğini 12 adımdan ~3.9 adıma düşürür.

### 3. Ampirik EVM Gaz Kıyaslaması (v1.0 Taban vs v2.0 Tripod $\mathbb{Z} \pmod 9$)
EIP-150 / EIP-2929 / EIP-3860 kuralları altında `solc 0.8.20 (runs: 200)` derlemesiyle [`scripts/ideal_evm_gas_benchmark.js`](scripts/ideal_evm_gas_benchmark.js) aracıyla canlı ölçülmüştür:

| Katman / Senaryo | v1.0 Taban | v2.0 Tripod $\mathbb{Z} \pmod 9$ | Net Tasarruf | Düşüş Oranı | Tavan Kriteri |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Saf Çıkarım Motoru Gazı** | **226.363 gaz** | **22.557 gaz** | **-203.806 gaz** | **-%90,0** | **BAŞARILI** ($\le 24.000$) |
| **En Kötü Durum Motor Tavanı** | 226.416 gaz | **22.568 gaz** | -203.848 gaz | -%90,0 | **BAŞARILI** (+1.432 gaz payı) |
| **Warm `decideNoul` (Normal)** | 264.970 gaz | **61.186 gaz** | -203.784 gaz | -%76,9 | Operasyonel |
| **Warm `decideNoul` (Şok / Hızlı Kaçış)** | 247.972 gaz | **44.102 gaz** | -203.870 gaz | -%82,2 | Operasyonel |
| **2 Seçenekli Rota Seçimi** | 247.786 gaz | **43.726 gaz** | -204.060 gaz | -%82,4 | Operasyonel |
| **8 Seçenekli Rota Seçimi** | 251.752 gaz | **44.680 gaz** | -207.072 gaz | -%82,3 | Operasyonel |
| **1-Belirteç Rezonans Sorgusu** | N/A | **3.821 gaz** | Salt Bytecode | 0 SLOAD | Anlık |
| **4-Belirteç Kompozit Füzyon** | N/A | **7.443 gaz** | Salt Bytecode | 0 SLOAD | Anlık |
| **Uniswap v4 Dinamik Kanca** | N/A | **36.739 gaz** | Uçtan Uca | Volatiliteye Bağlı | Sub-blok |

> 🛡️ **Formel İnvaryant Doğrulaması**: Ayrıntılı ampirik denetim raporu [`docs/EVM_GAS_IDEAL_BENCHMARK_REPORT.md`](docs/EVM_GAS_IDEAL_BENCHMARK_REPORT.md) ve ham JSON verileri [`tests/results/evm_gas_ideal_benchmark.json`](tests/results/evm_gas_ideal_benchmark.json) dosyasında mevcuttur.

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

## 💳 Bağış ve Hibe Kabul Cüzdanı
* **Resmi Cüzdan (Binance - USDT TRC20 / TRON Ağı):** `TLMhaDJTVYBHBSGJ9nCQGLvqnYFPsBgLJu`
* **Resmi İletişim:** `vdagli@itouch.com.tr` (Kurumsal) | `pcworm@pcworm.net` (Baş Araştırmacı) | `ask@answerr.me` (AI Otonom Ajan) | Web: `https://answerr.me`

---

## 📖 Akademik Alıntı (Citation)

Werracle'ı veya temelindeki WERR fraktal Sistem-1 karar motorunu Web3 araştırmalarınızda, dApp'lerinizde veya akademik yayınlarınızda kullanıyorsanız lütfen şu şekilde atıfta bulununuz:

```bibtex
@article{dagli2026werracle_arxiv,
  author        = {Volkan Da{\u{g}}l{\i} and Zerrin Da{\u{g}}l{\i} and Da{\u{g}}han Da{\u{g}}l{\i}},
  title         = {Werracle: Sub-Cent Intra-Block AI Reflex Oracles and Flash-Loan Circuit Breakers for EVM Smart Contracts},
  journal       = {arXiv preprint arXiv:2609.30719 [cs.CR, cs.AI, cs.DC]},
  year          = {2026},
  eprint        = {2609.30719},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CR},
  url           = {https://arxiv.org/abs/2609.30719},
  doi           = {10.48550/arXiv.2609.30719},
  note          = {Zenodo Archive: 10.5281/zenodo.22942598. TÜRKPATENT Priority: TR 2026/016285}
}


@article{dagli2026werracle_ssrn,
  title         = {Werracle: Sub-Cent Intra-Block AI Reflex Oracles and Flash-Loan Circuit Breakers for EVM Smart Contracts},
  author        = {Da{\u{g}}l{\i}, Volkan and Da{\u{g}}l{\i}, Zerrin and Da{\u{g}}l{\i}, Da{\u{g}}han},
  journal       = {Elsevier SSRN Electronic Journal},
  year          = {2026},
  month         = {October},
  note          = {SSRN Abstract ID: 7626279},
  url           = {https://ssrn.com/abstract=7626279}
}
@article{dagli2026fractalmap,
  author        = {Volkan Dağlı and Zerrin Dağlı and Dağhan Dağlı},
  title         = {Universal Fractal Natural Language Decision Map: Real-Time Edge Triage Across Heterogeneous Domains},
  journal       = {arXiv preprint arXiv:2609.25498 [cs.NE]},
  year          = {2026},
  url           = {https://arxiv.org/abs/2609.25498},
  doi           = {10.5281/zenodo.22939253}
}

@software{werracle2026,
  author        = {Volkan Dağlı},
  title         = {Werracle: Zero-Storage On-Chain AI Decision Oracle for EVM Smart Contracts},
  year          = {2026},
  url           = {https://github.com/pCwOrM/werracle},
  doi           = {10.5281/zenodo.22939253}
}

@article{dagli2026lean4_oed,
  title        = {Zero-Storage Procedural Neural Synthesis via Boundary Dynamics: Formal Verification in Lean 4 and Bare-Metal Gauntlet Validation},
  author       = {Da{\u{g}}l{\i}, Volkan and Da{\u{g}}l{\i}, Zerrin and Da{\u{g}}l{\i}, Da{\u{g}}han},
  journal      = {Zenodo Open Science Archive},
  year         = {2026},
  month        = {September},
  doi          = {10.5281/zenodo.22974544},
  url          = {https://doi.org/10.5281/zenodo.22974544},
  note         = {Formally verified in Lean 4 (Mathlib4, 0 sorry). 40-core bare-metal gauntlet benchmark verified. TÜRKPATENT Priority: TR 2026/016285.}
}

@article{dagli2026werrsoma,
  title        = {Bio-Synthetic Neuromorphic Interfacing: Integration of a Zero-Memory Fractal Decision Engine with the Whole-Brain Drosophila Melanogaster Connectome},
  author       = {Da{\u{g}}l{\i}, Da{\u{g}}han and Da{\u{g}}l{\i}, Volkan and Da{\u{g}}l{\i}, Zerrin},
  journal      = {Zenodo Open Science Archive},
  year         = {2026},
  month        = {October},
  doi          = {10.5281/zenodo.23072929},
  url          = {https://doi.org/10.5281/zenodo.23072929},
  note         = {158.262 nöron, 3.99M sinaps. Sub-4ms refleks gecikmesi, 0 VRAM. TÜRKPATENT Başvuru: TR 2026/016633. Çatı DOI: 10.5281/zenodo.22996625. Canlı 3D Portal: https://werrsoma.answerr.me/}
}
```

---

### 🏛️ Kurumsal İşletim Yapısı ve Akademik Araştırma Yönetişimi

Werr / Werracle / Answerr ekosistemi, **bağımsız akademik araştırma ve patent yazarlığı katmanı** ile **ticari kurumsal faaliyet katmanı** arasındaki kesin kurumsal ayrım ilkesiyle yürütülmektedir:

#### 1. 🏢 Ticari İşletim ve Fikrî Mülkiyet Lisanslama Katmanı (`ITouch Systems`)
* **Resmi Ticari Unvan:** **ITouch Bilişim Sistemleri Mühendislik Danışmanlık Sanayi ve Ticaret Limited Şirketi** (*ITouch Systems*)
* **Merkez ve Resmi Kayıtlar:** Çukurova Teknokent, Balcalı Mah. Güney Kampüs/5 Sk. No: 4/1 İç Kapı No: 26, 01330 Sarıçam / Adana, Türkiye • Vergi Dairesi ve VKN: **Yüreğir V.D. 4690944558** • MERSİS: `0469094455800001` • Sanayi Sicil: `827254` • KEP: `itouchbilisim@hs01.kep.tr`
* **Yönetim, Mühendislik ve Operasyon Ekibi (8 Kişilik ITouch Ekibi):**
  * **Yönetim ve Ortaklar:**
    1. **Volkan Dağlı** — *Kurucu & CTO* (Fizikçi, Yönetim Bilişim Sistemleri Uzmanı & Bilişim Teknolojileri YL)
    2. **Bekirhan Dağlı** — *Ortak & CEO* (Çevre Mühendisi)
  * **Mühendislik, Finans ve Operasyon:**
    3. **Burak Salar** — *Mekatronik Mühendisi, MBA*
    4. **Fatih İlkin Sercan** — *Ekonomist, Sermaye Piyasası ve Borsa YL*
    5. **Mustafa Kalender** — *Bilgisayar Mühendisi ([Tetra Ar-Ge](https://tetraarge.com.tr/))*
    6. **Mustafa Ünal** — *Yazılım Geliştirme Uzmanı & Usta Öğretici ([Tetra Ar-Ge](https://tetraarge.com.tr/))*
    7. **Prenses Metin** — *Bilgisayar Programcısı ([Gifted Coder Technology](https://giftedcodertechnology.com.tr/))*
    8. **Semih Salar** — *İşletme Uzmanı ([Tureken Ajans](https://tureken.com/))*
* **Münhasır Ticari Haklar ve Markalar:** Patentlerin tam vekâlet sahibi ve yazılımların hak sahibi olan **Volkan Dağlı**'nın (Kurucu & CTO) resmi yetkilendirmesiyle; tüm yazılım, patent ve yayınların ticari kullanım, satış ve kurumsal lisanslama hakları ile **`Werr®`**, **`Werracle®`** ve **`Answerr®`** markaları (TÜRKPATENT başvuruları ITouch Systems adına) münhasıran **ITouch Bilişim Sistemleri Ltd. Şti.**'ye aittir.

#### 2. 🎓 Akademik Araştırma ve Patent Yazarlığı Katmanı
* **Volkan Dağlı** — *Baş Araştırmacı ve Baş Mimar* (Akademik Bağlılık: **Anadolu Üniversitesi**; Ticari Rol: **Kurucu & CTO, ITouch Systems**).
* **Dr. Zerrin Dağlı** — *Akademik Danışman ve Ortak Yazar* (Akademik Bağlılık: **Mersin Üniversitesi**; yalnızca bağımsız **Akademik Danışman** ve bilimsel ortak yazar olarak yer almakta olup **hiçbir ticari rolü veya şirket bağı yoktur**).
* **Dağhan Dağlı** — *Stajyer / Gönüllü Genç Araştırmacı* (Bağlılık: **Toros Üniversitesi — Toros Fen Lisesi**; bilimsel yayınlarda yalnızca ticari olmayan stajyer/gönüllü araştırmacı olarak yer almaktadır).
* **Patentler (`TÜRKPATENT TR 2026/016285` ve `TR 2026/016633`):** **Volkan Dağlı**, **Dr. Zerrin Dağlı** ve **Dağhan Dağlı** adına şahsi ortak buluş olarak kayıtlıdır; **tüm temsil, vekâlet ve ticari lisanslama yetkisi Volkan Dağlı'ya verilmiş** olup ticari hakları münhasıran **ITouch Bilişim Sistemleri Ltd. Şti.** tarafından yürütülmektedir.

### 💳 Resmi Hazine Cüzdanları ve Anında 1-Tık B2B API Ödeme Sistemi
| Kanal / Ödeme Yöntemi | Ağ / Altyapı | Doğrulanmış Adres / Ödeme Bağlantısı |
| :--- | :--- | :--- |
| **1-Tık Web3 & Çoklu Ödeme** | Base USDC / TRC20 USDT / **iyzico 3D Kredi Kartı** | [**`radar.werracle.com/v1/radar/dashboard#subscribe-section`**](https://radar.werracle.com/v1/radar/dashboard#subscribe-section) |
| **Anında Ticari Fatura (PDF)** | Resmi ITouch Systems Ticari Faturası | [**`radar.werracle.com/v1/radar/invoice/sample.pdf`**](https://radar.werracle.com/v1/radar/invoice/sample.pdf) |
| **Resmi EVM Cüzdanı (Binance)** | Base / Ethereum (ERC20) / Arbitrum / BSC (`USDC` & `USDT`) | `0x4945ef6e124eea2176ddf050b33db42b0ae8c7f7` |
| **Resmi TRON Cüzdanı (Binance)** | TRC20 (TRON Ağı — `USDT`) | `TLMhaDJTVYBHBSGJ9nCQGLvqnYFPsBgLJu` |
| **Resmi Tüzel Kişilik** | Çukurova Teknokent (VKN: `4690944558`) | ITouch Bilişim Sistemleri Mühendislik Danışmanlık Sanayi ve Ticaret Ltd. Şti. |

* **Resmi İletişim Kanalları:** `contact@werracle.com` (Kurumsal & Protokol) | `ask@answerr.me` (Destek & Genel İletişim) | `labs@werr.io` (Werr Labs Araştırma) | `billing@werr.io` (Faturalama)

---

## 📜 Lisans
Werracle, **Business Source License 1.1 (BSL 1.1)** ile korunmaktadır (Uniswap v3/v4 modeli):
* Testnet'lerde test etmek, akademik araştırmalar ve kar amacı gütmeyen protokoller için **%100 ücretsiz ve açık kaynaklıdır**.
* Ticari ana ağ (mainnet) dağıtımları **1 Ocak 2030** tarihine kadar resmi yönlendirici kullanımına veya ticari lisansa tabidir; bu tarihten sonra otomatik olarak **Apache License, Version 2.0**'a dönüşür.
* Somutlaştırılan prosedürel mekanizmalar **TÜRKPATENT TR 2026/016285** patent başvurusu koruması altındadır.

## 🏛️ Tarihsel Arşivler ve Sürüm Mirası

Tüm önceki tasarım ve protokol sürümleri şeffaflık ve denetlenebilirlik amacıyla kaynakta arşiv olarak korunmaktadır:

- **Klasik v1.0 Arşivi (`werracle.io` İlk Temel Sürüm):** [`https://werracle.io/v1_classic.html`](https://werracle.io/v1_classic.html)
- **Mimari v2.0 Deneme Alanı Arşivi:** [`https://werracle.io/v2_initial_archive.html`](https://werracle.io/v2_initial_archive.html)
- **Kurumsal Portal v1.0 (Koyu Tema Arşivi):** [`https://werracle.com/archive_dark_v1.html`](https://werracle.com/archive_dark_v1.html)
