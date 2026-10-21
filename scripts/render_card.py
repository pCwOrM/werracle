import base64
import asyncio
from playwright.async_api import async_playwright
import os

with open('werracle/assets/werracle_logo_oracle_trans.png', 'rb') as f:
    logo_b64 = base64.b64encode(f.read()).decode('utf-8')

html_content = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
    width: 2400px;
    height: 1350px;
    background: radial-gradient(circle at 25% 45%, #0c1a32 0%, #060913 55%, #020409 100%);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    color: #f8fafc;
    padding: 70px 90px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    position: relative;
}}
/* Ambient background grid */
body::before {{
    content: '';
    position: absolute;
    inset: 0;
    background-image: 
        linear-gradient(rgba(56, 189, 248, 0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56, 189, 248, 0.04) 1px, transparent 1px);
    background-size: 80px 80px;
    pointer-events: none;
}}
.main-container {{
    display: flex;
    flex: 1;
    align-items: center;
    gap: 80px;
    position: relative;
    z-index: 2;
}}
.logo-container {{
    flex: 0 0 680px;
    height: 680px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}}
.logo-halo {{
    position: absolute;
    width: 580px;
    height: 580px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(14, 165, 233, 0.25) 0%, rgba(0, 236, 151, 0.15) 45%, transparent 70%);
    filter: blur(40px);
}}
.orbit-ring {{
    position: absolute;
    width: 640px;
    height: 640px;
    border-radius: 50%;
    border: 1.5px dashed rgba(56, 189, 248, 0.35);
}}
.logo-img {{
    width: 540px;
    height: 540px;
    object-fit: contain;
    position: relative;
    z-index: 3;
    filter: drop-shadow(0 0 45px rgba(56, 189, 248, 0.5));
}}
.content-container {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}
.badge-row {{
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 24px;
}}
.pill {{
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 10px 24px;
    border-radius: 9999px;
    background: rgba(14, 165, 233, 0.12);
    border: 1.5px solid rgba(56, 189, 248, 0.5);
    color: #38bdf8;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}}
.pill-green {{
    background: rgba(0, 236, 151, 0.12);
    border-color: rgba(0, 236, 151, 0.5);
    color: #00EC97;
}}
.title {{
    font-size: 88px;
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #ffffff 30%, #bae6fd 70%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}}
.version-tag {{
    color: #fbbf24;
    -webkit-text-fill-color: #fbbf24;
    font-size: 64px;
    margin-left: 20px;
}}
.tagline {{
    font-size: 30px;
    font-weight: 500;
    color: #94a3b8;
    line-height: 1.4;
    margin-bottom: 40px;
}}
.tagline strong {{
    color: #f1f5f9;
}}
.tagline code {{
    color: #a78bfa;
    background: rgba(167, 139, 250, 0.12);
    padding: 2px 10px;
    border-radius: 8px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}}
.grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 22px;
}}
.card {{
    background: rgba(15, 23, 42, 0.7);
    border: 1.5px solid rgba(51, 65, 85, 0.8);
    border-radius: 20px;
    padding: 26px 30px;
    backdrop-filter: blur(16px);
    display: flex;
    flex-direction: column;
    gap: 8px;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
}}
.card-header {{
    font-size: 25px;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 12px;
}}
.card-desc {{
    font-size: 19px;
    color: #94a3b8;
    line-height: 1.35;
}}
.c-cyan {{ border-color: rgba(56, 189, 248, 0.4); }}
.c-cyan .card-header {{ color: #38bdf8; }}
.c-green {{ border-color: rgba(0, 236, 151, 0.4); }}
.c-green .card-header {{ color: #00EC97; }}
.c-pink {{ border-color: rgba(236, 72, 153, 0.4); }}
.c-pink .card-header {{ color: #f472b6; }}
.c-purple {{ border-color: rgba(168, 85, 247, 0.4); }}
.c-purple .card-header {{ color: #c084fc; }}

.footer-bar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(15, 23, 42, 0.75);
    border: 1.5px solid rgba(51, 65, 85, 0.8);
    border-radius: 20px;
    padding: 22px 36px;
    backdrop-filter: blur(16px);
    position: relative;
    z-index: 2;
}}
.footer-item {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 20px;
    color: #cbd5e1;
    font-weight: 600;
}}
.footer-item strong {{
    color: #f8fafc;
}}
.domain-highlight {{
    color: #38bdf8;
    font-size: 24px;
    font-weight: 800;
    letter-spacing: 0.5px;
}}
</style>
</head>
<body>

<div class="main-container">
    <div class="logo-container">
        <div class="logo-halo"></div>
        <div class="orbit-ring"></div>
        <img class="logo-img" src="data:image/png;base64,{logo_b64}" alt="Werracle Oracle Logo" />
    </div>

    <div class="content-container">
        <div class="badge-row">
            <div class="pill">Zero-Storage On-Chain AI</div>
            <div class="pill pill-green">Aurora EVM & NEAR Live</div>
        </div>

        <h1 class="title">WERRACLE<span class="version-tag">v2.0</span></h1>

        <p class="tagline">
            The whole AI model fits in a <strong>single 32-byte storage slot</strong> (<code>bytes32</code>).
        </p>

        <div class="grid">
            <div class="card c-cyan">
                <div class="card-header">⚡ ~20.7k Gas / Decision</div>
                <div class="card-desc">Sub-millisecond intra-block AI decisions (< $0.0001) in pure EVM bytecode.</div>
            </div>
            <div class="card c-green">
                <div class="card-header">🛡️ NEAR Intent Guard</div>
                <div class="card-desc">Pre-signing MEV & flash-loan circuit breaker for NEAR Chain Signatures.</div>
            </div>
            <div class="card c-pink">
                <div class="card-header">🦄 Uniswap v4 Hook</div>
                <div class="card-desc">Dynamic LP swap fee governor (0.05% - 0.50%) based on real-time pool turbulence.</div>
            </div>
            <div class="card c-purple">
                <div class="card-header">📜 40 Lean 4 Proofs</div>
                <div class="card-desc">Formal math & escape dynamics certified with 0 sorry and 1,000 sealed test vectors.</div>
            </div>
        </div>
    </div>
</div>

<div class="footer-bar">
    <div class="footer-item domain-highlight">🌐 werracle.io</div>
    <div class="footer-item">🏛️ <strong>Zenodo:</strong> 10.5281/zenodo.22942598</div>
    <div class="footer-item">📄 <strong>SSRN:</strong> 7626279</div>
    <div class="footer-item">🔴 <strong>Patent:</strong> TR 2026/016285</div>
    <div class="footer-item" style="color:#00EC97;">🟢 <strong>Aurora Testnet:</strong> Live & Verified</div>
</div>

</body>
</html>
'''

async def render():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 2400, 'height': 1350})
        await page.set_content(html_content)
        await page.wait_for_timeout(600)
        out_path = 'werracle/assets/werracle_twitter_social_card.png'
        await page.screenshot(path=out_path, full_page=True)
        artifact_path = r'C:\Users\maat\.gemini\antigravity\brain\dda702fe-3efa-4434-83d5-3111cadb22cf\werracle_twitter_social_card.png'
        await page.screenshot(path=artifact_path, full_page=True)
        print(f'Rendered card successfully to {out_path} and {artifact_path}!')
        await browser.close()

if __name__ == '__main__':
    asyncio.run(render())
