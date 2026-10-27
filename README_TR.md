<div align="center">

# WERRACLE
### Sıfır-Bellekli Blokzincir Üzeri Yapay Zekâ Karar Kâhini ve DeFi Risk Radarı

[![Lisans: BSL 1.1](https://img.shields.io/badge/Lisans-BSL_1.1-0ea5e9.svg)](LICENSE)
[![Solidity: ^0.8.24](https://img.shields.io/badge/Solidity-^0.8.24%20(Q16.16)-6366f1.svg)](contracts/)
[![EVM Devnet: Chain ID 4242](https://img.shields.io/badge/EVM_Devnet-Zincir_4242-10b981.svg)](https://api.answerr.me/rpc)
[![Zenodo DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.22942598-f59e0b.svg)](https://doi.org/10.5281/zenodo.22942598)
[![arXiv Ön Baskı](https://img.shields.io/badge/arXiv-2609.30719-b91c1c.svg)](https://arxiv.org/abs/2609.30719)
[![Canlı Radar](https://img.shields.io/badge/Canl%C4%B1_Telemetri-radar.werracle.com-38bdf8.svg)](https://radar.werracle.com)

<p align="center">
  <b>Zincir dışı güven varsayımlarına ihtiyaç duymaksızın; dinamik Uniswap v4 takas kancaları (hooks), blok altı MEV savunması ve gerçek zamanlı borç verme kasası risk telemetrisini Ethereum Sanal Makinesi (EVM) içinde doğrudan çalıştıran sıfır depolamalı, sabit noktalı prosedürel karar kâhini.</b>
</p>

[Hızlı Başlangıç](#-hızlı-başlangıç-ve-dağıtım) •
[Mimari](#-blokzincir-üzeri-fraktal-mimari) •
[Akıllı Sözleşmeler](#-akıllı-sözleşme-paketi) •
[Ampirik Sonuçlar](#-ampirik-kıyaslamalar-ve-svr-telemetrisi) •
[Canlı Risk Radarı](#-werracle-risk-radarı) •
[Ekosistem](#-werr-ekosistemi) •
[Araştırma Kronolojisi](RESEARCH_CHRONOLOGY.md) •
[English Documentation](README.md)

</div>

---

## 🏛️ Yeni Bir Paradigma

Merkeziyetsiz finans (DeFi) protokolleri **kâhin gecikmesi**, **gas maliyeti** ve **güven minimizasyonu** arasında temel bir açmazla karşı karşıyadır:
1. **Geleneksel İtme/Çekme Kâhinleri (Oracles):** Zincir dışı çoklu imzalara, üçüncü taraf düğüm ağlarına veya gecikmeli fiyat güncellemelerine bağımlıdır. Bu durum Otomatik Piyasa Yapıcıları (AMM) Dengeleme-Kayıp (LVR) ve toksik MEV arbitrajına açık hale getirir.
2. **Derin Sinir Ağı Çıkarımı:** Üretimsel LLM'ler ve çok katmanlı sinir ağları blokzincir üzerinde doğrudan çalıştırılamaz; gigabaytlarca kayan nokta ağırlığını EVM bayt kodunda hesaplamak blok gas limitlerini katbekat aşar.

**Werracle**, **WERR** prosedürel fraktal refleks motorunu yerel EVM bayt koduna taşıyarak bu engeli aşar:
* **Sıfır Depolama Alanı:** Ağırlıklar için sözleşme durumunda **0 bayt** depolama gerektirir. Karar sınırları anlık olarak hesaplanan geometrik değişmezlerdir.
* **Deterministik Q16.16 Sabit Nokta Matematiği:** Optimize edilmiş Solidity derleyicisi içinde sabit noktalı polinom sınır kaçış dinamiklerini ($z_{n+1} = z_n^2 + c$) yürütür.
* **Blok Altı Yürütme Hızı:** Tam refleks doğrulamasını Ethereum L1 üzerinde **$< 42.000$ gas** tüketimiyle, Base ve Arbitrum L2 ağlarında ise cent altı maliyetlerle gerçekleştirir.

```
          Gelen Takas / Tasfiye İşlemi
                       │
                       ▼
       ┌──────────────────────────────────────┐
       │     Uniswap v4 Havuzu / Morpho Kasa  │
       └──────────────────┬───────────────────┘
                          │ beforeSwap() / liquidate() çağrısı
                          ▼
       ┌──────────────────────────────────────┐
       │       WerracleCore (On-Chain)        │
       │  Q16.16 Sabit Noktalı Fraktal Motor  │  ◄── Sıfır Depolama Ağırlığı
       │           Gas: ~38.500 birim         │
       └──────────────────┬───────────────────┘
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
   [Dinamik Takas Ücreti]    [Refleks Koruma]
   LVR/MEV Geri Kazanımı     Kötü borç silsilesini durdurma
```

---

## ⚡ Hızlı Başlangıç ve Dağıtım

### Sözleşme Kurulumu (Foundry)

```bash
forge install pCwOrM/werracle
```

*Veya npm/yarn ile yükleyin:*

```bash
npm install @werracle/contracts
```

### Temel Sözleşme Entegrasyonu

```solidity
// SPDX-License-Identifier: BUSL-1.1
pragma solidity ^0.8.24;

import {IWerracleOracle} from "@werracle/contracts/interfaces/IWerracleOracle.sol";

contract SafeVault {
    IWerracleOracle public immutable oracle;

    constructor(address _oracle) {
        oracle = IWerracleOracle(_oracle);
    }

    function executeProtectedAction(bytes32 poolId, uint256 volatility) external {
        // Sıfır-depolamalı refleks kâhinini sorgula
        // Dönen değer: 0 = İzin Ver / Normal, 1 = Dikkat / Yüksek Ücret, 2 = Acil Durum Kapısı
        uint8 decision = oracle.evaluateRisk(poolId, volatility);
        
        require(decision != 2, "Werracle: Acil durum volatilite refleksi tetiklendi");
        
        // Durum geçişini yürüt...
    }
}
```

---

## 📐 Akıllı Sözleşme Paketi

Depo, EVM üzerinde çalışan denetlenmiş Solidity uygulamalarını içerir:

| Sözleşme | Amaç | Gas Profili | Hedef Ağlar |
|---|---|---|---|
| [`WerracleCore.sol`](contracts/WerracleCore.sol) | Q16.16 kaçış matematiğiyle kanonik blokzincir üzeri refleks kâhini | ~38.500 gas | Ethereum L1, Base, Arbitrum |
| [`WerracleUniswapV4Hook.sol`](contracts/hooks/WerracleUniswapV4Hook.sol) | Toksik LVR arbitrajını önleyen `beforeSwap` dinamik ücret kancası | ~41.200 gas | Base L2, Uniswap v4 Dağıtımları |
| [`WerracleMorphoSVR.sol`](contracts/adapters/WerracleMorphoSVR.sol) | MetaMorpho kasa sağlığı izleme & SVR değer geri kazanımı | ~32.000 gas | Ethereum L1 / Base L2 |
| [`FixedPointFractal.sol`](contracts/libraries/FixedPointFractal.sol) | Yörüngesel karmaşık kaçış hesaplayan matematik kütüphanesi | Saf kütüphane | EVM Bayt Kodu uyumlu |

---

## 📊 Ampirik Kıyaslamalar ve SVR Telemetrisi

Werracle'ın Akıllı Değer Geri Kazanımı (Smart Value Recapture - SVR) ve dinamik ücret kancaları kapsamlı stres simülasyonları ve testnet testlerinden geçirilmiştir:

* **Akıllı Değer Geri Kazanımı (SVR):** Volatil arbitraj olaylarında standart 30 bps Uniswap havuzlarına kıyasla **%94,38** değer geri kazanım oranına ulaştı.
* **FastLane Atlas Solver Kıyaslamaları:** Karşıt ardışıl çalıştırma (backrunning) paketlerine karşı mikrosaniye düzeyinde refleks arbitrajı kanıtlandı.
* **MetaMorpho Borç Verme Dayanıklılığı:** Sentetik tasfiye şoklarında kötü borç kaskad tetikleyicilerini başarıyla bloke etti.

Detaylı simülasyon betikleri, Monte Carlo analizleri ve sözleşme gas profil kayıtları [RESEARCH_CHRONOLOGY.md](RESEARCH_CHRONOLOGY.md) dosyasında sunulmaktadır.

---

## 📡 Werracle Risk Radarı

Werracle, kurumsal düzeyde canlı risk istihbarat paneline güç vermektedir:

🔗 **[https://radar.werracle.com](https://radar.werracle.com)**

* **Canlı MetaMorpho Kasa Telemetrisi:** Gerçek zamanlı teminat izleme, arz/borç APY oynaklığı ve kötü borç riski metrikleri.
* **Base L2 Yürütme Akışları:** Blokzincir üzeri refleks işlemleri, dinamik takas ücreti ayarlamaları ve MEV koruma olaylarının canlı akışı.
* **Kurumsal DaaS API:** Kantitatif piyasa yapıcılar ve merkeziyetsiz protokoller için düşük gecikmeli REST & WebSocket akışları.

---

## 🌐 WERR Ekosistemi

Werracle, WERR temel mimarisinin merkeziyetsiz yürütme katmanını temsil eder:

```
                          ┌─────────────────────────────┐
                          │            WERR             │
                          │    Çekirdek Matematik Motor │
                          │  Sıfır-Bellekli Sistem-1    │
                          └──────────────┬──────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼                                               ▼
  ┌─────────────────────────────┐                 ┌─────────────────────────────┐
  │          Werracle           │                 │           answerr           │
  │ Blokzincir Karar Kâhini     │                 │   Çift Bilişli Çalışma Alanı│
  │  DeFi Risk Radarı & DaaS    │                 │   Doğal Dil Güvenlik API'si │
  │   https://radar.werracle.com│                 │     https://answerr.me      │
  └─────────────────────────────┘                 └─────────────────────────────┘
```

* **[`werr`](https://github.com/pCwOrM/werr):** Çekirdek sıfır-bellekli fraktal refleks motoru ve Lean 4 ile biçimsel olarak doğrulanmış matematiksel ispatlar.
* **`werracle`:** Blokzincir üzeri Solidity uygulamaları, Uniswap v4 kancaları ve merkeziyetsiz risk radarı.
* **[`answerr`](https://github.com/pCwOrM/answerr):** Sistem-2 muhakemesini deterministik refleks yürütmeyle birleştiren çift bilişli çalışma alanı.

---

## 📄 Akademik Atıf ve Arşiv Kaynakları

Bu araştırmayı bilimsel yayınlarınızda referans gösterirken lütfen aşağıdaki künyeyi kullanın:

```bibtex
@article{dagli2026werracle,
  author       = {Dağlı, Volkan and Dağlı, Zerrin and Dağlı, Dağhan},
  title        = {{Werracle: Zero-Storage On-Chain AI Decision Oracle via Procedural Fractal Dynamics}},
  journal      = {arXiv preprint arXiv:2609.30719},
  year         = {2026},
  doi          = {10.48550/arXiv.2609.30719},
  publisher    = {Zenodo},
  version      = {v1.0.0},
  note         = {Zenodo DOI: 10.5281/zenodo.22942598}
}
```

* **SSRN Araştırma Özeti:** SSRN: 7626279 ([https://ssrn.com/abstract=7626279](https://ssrn.com/abstract=7626279))
* **Tam Araştırma Kronolojisi:** [`RESEARCH_CHRONOLOGY.md`](RESEARCH_CHRONOLOGY.md)

---

## ⚖️ Lisans ve Fikri Mülkiyet

* **Açık Bilim, Eğitim ve Değerlendirme Kullanımı:** Lisanslı Eser; **Business Source License 1.1 (BSL 1.1)** kapsamında ticari olmayan tüm akademik araştırmalar, kişisel incelemeler, testler ve genel testnet dağıtımları için serbestçe çalıştırılabilir, kaynak kodu incelenebilir ve yinelenebilir.
* **Ticari Faaliyetler ve Üretim Lisanslaması:** Her türlü ticari ana ağ (mainnet) dağıtımı, gelir üreten DeFi protokollerine entegrasyon veya tescilli SaaS/DaaS işletimi, Lisans Veren'den yazılı Ticari Lisans alınmasını gerektirir:
  * **Lisans Veren:** `ITOUCH BİLİŞİM SİSTEMLERİ MÜHENDİSLİK DANIŞMANLIK SANAYİ VE TİCARET LİMİTED ŞİRKETİ` (`ITouch Sistemleri` · Çukurova Teknokent, Adana, Türkiye).
  * **Bilimsel Ortak Yazarlar ve Mucitler:** Volkan Dağlı (*Anadolu Üniversitesi*), Dr. Zerrin Dağlı (*Mersin Üniversitesi — Akademik Danışman, Ortak Yazar ve Ortak Mucit*), Dağhan Dağlı (*Toros Üniversitesi — Ortak Yazar ve Ortak Mucit*).
  * **Hak Devri ve Yetki Silsilesi:** Bilimsel ortak yazarlar ve mucitler, fikri mülkiyet yönetimi ve temsil yetkisini Volkan Dağlı'ya; Volkan Dağlı ise münhasır küresel ticari lisanslama, marka ve operasyon haklarını ITouch Bilişim Sistemleri Ltd. Şti.'ye devretmiştir.
  * **Ticari Markalar:** `WERR™`, `Werracle™`, `answerr™` ve `WerrSoma™` markalarının mülkiyeti münhasıran ITouch Bilişim Sistemleri Ltd. Şti.'ye aittir.
  * **Patent Başvuruları:** TÜRKPATENT **TR 2026/016285** ve **TR 2026/016633**.
  * **İletişim:** `contact@werracle.com` · `info@itouch.com.tr`

---

<div align="center">
  <sub>ITouch Bilişim Sistemleri tarafından geliştirilmiştir · Çukurova Teknokent, Adana, Türkiye</sub><br>
  <sub>Telif Hakkı &copy; 2026 ITouch Bilişim Sistemleri Ltd. Şti. Tüm hakları saklıdır.</sub>
</div>
