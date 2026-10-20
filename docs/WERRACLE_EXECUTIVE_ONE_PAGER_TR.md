# WERRACLE — YÖNETİCİ ÖZETİ VE TEK SAYFALIK PITCH (ONE-PAGER)
## Sıfır Bellekli Zincir Üstü Yapay Zekâ Karar Kâhini | EVM 32-Bayt Slot & NEAR Niyet Koruyucu
**Patent Başvuruları: TR 2026/016285 & TR 2026/016633 | Lean 4 ile Biçimsel Olarak İspatlı (40 Teorem, 0 Sorry)**  
*Baş Geliştirici: pcworm.near | ITOUCH Bilişim Sistemleri Ltd. Şti.*  
*Hedef Kategoriler: Unstoppable DeFi, AI Security & Defense, Privacy & Private AI, Autonomous Business, AI Swarms*

---

### 1. Yönetici Özeti
Günümüz DeFi protokolleri ve otonom yapay zekâ ajanları çözümsüz bir ikilemle karşı karşıyadır:
- **EVM Üzerinde Klasik Yapay Zekâ:** Zincir üstünde çalışamaz. Milyonlarca kayan noktalı ağırlık, blok gaz limitlerini 1.000 kat aşar (>15M gaz).
- **ZK-ML (Sıfır Bilgi Kanıtlı ML):** Zincir dışında kanıt üretmek 10 ila 300 saniye sürer ve zincirde doğrulaması ~350.000 gaza mal olur. Kanıt zincire ulaştığında flash-loan saldırganı havuzu çoktan boşaltmıştır.
- **Zincir Dışı Kâhinler (Chainlink/API):** Merkezi hata noktalarıdır; gecikme arbitrajına ve önden koşmaya (front-running) açıktır.

**Çözüm:** **Werracle**, tescilli ve patentli **WERR™ Çekirdeği** ile tüm bir karar modelini **tek bir 32 baytlık EVM depolama hücresine** sıkıştırır. Milisaniyenin altında, soruyu soran aynı işlem içinde **~19.400 gaz** ile (ZK-ML'den %99,8 daha ucuz, basit bir token transferinden daha tasarruflu) karar üretir. **Harici sunucu yok, dış anahtar yok, veri sızıntısı yok.**

---

### 2. 32 Baytlık "Gizli Formül" (Neden Biz Kazanıyoruz?)
Tıpkı Coca-Cola'nın gizli formülü veya bir Intel işlemci gibi, Werracle protokol kurucularının karmaşık dinamik sistemleri anlamasını gerektirmez. Değer teklifi net, değişmez ve ispatlıdır:

| Parametre | Zincir Dışı AI Kâhinleri | ZK-ML Doğrulama | Werracle (WERR™ Çekirdeği) |
| :--- | :--- | :--- | :--- |
| **Gecikme (Latency)** | 1–2 Blok (~12–24 sn) | 10–300 Saniye | **< 1 ms (Aynı İşlem İçinde)** |
| **Gaz Maliyeti** | Yok (Zincir dışı) | ~350.000 Gaz | **~19.400 Gaz** |
| **Flash-Loan Savunması** | ❌ İmkânsız (Geç gelir) | ❌ İspat çok geç gelir | **✅ İşlem İçinde Atomik Revert** |
| **Zincir Üstü Ayak İzi** | Harici RPC Düğümleri | Kilobaytlarca ispat anahtarı | **Tek 32 Baytlık Slot** |
| **Biçimsel Doğrulama** | Yok | Yalnızca devre | **40 Lean 4 Teoremi (0 Sorry)** |
| **Gizlilik / Telemetri** | Yüksek sızıntı (API logları) | Ara durumlar sızar | **%100 Yalıtılmış Sıfır Sızıntı** |

---

### 3. Kullanıma Hazır Savunma Senaryoları

#### 🛡️ A. İşlem İçi Flash Loan & MEV Kalkanı
- **Sorun:** Saldırgan tek bir Ethereum bloğunda 50M$ borç alır, DEX fiyatını oynatır, pozisyonları likide eder ve borcu kapatır.
- **Werracle Refleksi:** Kredi sözleşmesi `IWerracle.decideNoul(state, riskQ16)` çağırır. Fiyat etkisi veya borçlanma tehdit sınırını aşarsa Werracle `false` döner ve `require(allowed)` işlemi **atomik olarak geri alır (revert)**. Saldırgan hiçbir şey çalamaz ve tüm gaz parasını cebinden öder.

#### 📈 B. Uniswap v4 Dinamik Oynaklık ve Sürpriz Ücret Kancası
- `WerracleFeeHook.sol` ile likidite havuzları takas ücretlerini sakin piyasada **%0,05**'ten MEV türbülansında **%0,50**'ye kadar otomatik ayarlar. Zararlı emir akışları cezalandırılarak protokol rezervlerine aktarılır.

#### 🟢 C. NEAR Intent İmza Öncesi Koruyucusu (`pcworm.near`)
- NEAR Zincir İmzalarının önünde bir refleks olarak çalışır. Temiz niyetler (çapraz zincir takaslar, ajan mikro ödemeleri) **12,6 µs** içinde onaylanır; sandviç saldırıları ve manipülatif paketler henüz kriptografik imza üretilmeden veto edilir.

---

### 4. Teknik Kale ve Doğrulama
1. **Lean 4 Makine Denetimli İspat:**
   - 40 teorem, Lean 4 çekirdeği tarafından **standart 3 aksiyom dışında hiçbir ek aksiyom olmadan ve 0 sorry** ile denetlenmiştir.
   - Sabit gaz tavanı, döngünün sonlanması ($\le 12$ adım) ve Q16.16 karelerinde `int64` taşma olamayacağı ispatlıdır.
2. **Mühürlü Test Paketi:** 1.000 / 1.000 deterministik test geçti.
3. **Patent Rüçhanları:** Türk Patent ve Marka Kurumu başvuruları **TR 2026/016285** ve **TR 2026/016633**.
4. **Canlı Sözleşmeler (Aurora Testnet - Chain 1313161555):**
   - `Werracle.sol`: `0x4085673F1e45bf26682CA704b2d09C03d1212cd4`
   - `WerracleTripodZMod9.sol`: `0x1d7Ae9E1dDDA805539d9e225425804Ef8B9caBaF`
   - Gezgin: [explorer.testnet.aurora.dev](https://explorer.testnet.aurora.dev)

---

### 5. Solidity'de 3 Satırda Entegrasyon
```solidity
import "werracle/contracts/IWerracle.sol";

// Herhangi bir DeFi havuz, takas veya likidasyon fonksiyonunda:
(bool allowed, ) = werracle.decideNoul(txStateHash, riskScoreQ16);
require(allowed, "Werracle: Dusmanca islem deseni engellendi");
```

---

### 6. İletişim ve Araştırma Kayıtları
- **Baş Geliştirici:** pcworm.near / Volkan Dağlı (`pcworm@pcworm.net`, `vdagli@itouch.com.tr`)
- **Kurum:** ITOUCH Bilişim Sistemleri Ltd. Şti. (Çukurova Teknokent, Adana, Türkiye)
- **Resmi Web Sitesi:** [https://pcworm.github.io/werracle/](https://pcworm.github.io/werracle/)
- **Akademik Kayıtlar:** arXiv:2609.30719 | SSRN:7626279 | Zenodo DOI: 10.5281/zenodo.22942598 | Hugging Face: papers/2609.30719
