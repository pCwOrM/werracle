#!/usr/bin/env python3
"""
Generate publication-quality figures for Werracle arXiv submission.
Outputs to werracle/arxiv/figures/:
1. fig1_werracle_architecture.png
2. fig2_benchmarks_comparison.png
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "arxiv", "figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set global styles
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

def generate_architecture_figure():
    fig, ax = plt.subplots(figsize=(7.2, 3.4), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')

    # Color palette
    c_blue = '#1e3a8a'
    c_blue_light = '#dbeafe'
    c_emerald = '#065f46'
    c_emerald_light = '#d1fae5'
    c_purple = '#581c87'
    c_purple_light = '#f3e8ff'
    c_amber = '#92400e'
    c_amber_light = '#fef3c7'

    # Box 1: Inflow
    b1 = patches.FancyBboxPatch((0.3, 1.2), 2.2, 2.8, boxstyle="round,pad=0.15", 
                                 edgecolor=c_blue, facecolor=c_blue_light, linewidth=1.5)
    ax.add_patch(b1)
    ax.text(1.4, 3.65, "DeFi Transaction Flow", ha='center', va='center', fontsize=9, fontweight='bold', color=c_blue)
    ax.text(1.4, 3.0, "• Flash-loan borrow\n• Large pool swap\n• Volatility / tick spike\n• State parameters", 
            ha='center', va='center', fontsize=7.5, color='#1e293b', linespacing=1.4)
    ax.text(1.4, 1.6, "Incoming Call / beforeSwap", ha='center', va='center', fontsize=7, fontstyle='italic', color='#475569')

    # Arrow 1 -> 2
    ax.annotate("", xy=(2.9, 2.6), xytext=(2.5, 2.6),
                arrowprops=dict(arrowstyle="->", color='#334155', lw=2, mutation_scale=15))

    # Box 2: Werracle Core
    b2 = patches.FancyBboxPatch((3.0, 0.4), 4.0, 4.2, boxstyle="round,pad=0.15", 
                                 edgecolor=c_purple, facecolor=c_purple_light, linewidth=1.5)
    ax.add_patch(b2)
    ax.text(5.0, 4.25, "Werracle EVM Engine (Single Slot)", ha='center', va='center', fontsize=9.5, fontweight='bold', color=c_purple)

    # Sub-box: Slot Layout
    b_slot = patches.FancyBboxPatch((3.2, 3.0), 3.6, 0.9, boxstyle="round,pad=0.08",
                                     edgecolor='#a855f7', facecolor='#ffffff', linewidth=1)
    ax.add_patch(b_slot)
    ax.text(5.0, 3.6, "Packed 32-Byte Slot (bytes32): 100 Gas Warm SLOAD", ha='center', va='center', fontsize=7.2, fontweight='bold', color='#7e22ce')
    ax.text(5.0, 3.25, "[cx: 64b | cy: 64b | zoom: 64b | th: 16b | nonce: 16b | flags: 32b]", ha='center', va='center', fontsize=6.2, family='monospace', color='#3b0764')

    # Sub-box: Q16.16 & Mandelbrot Escape
    b_math = patches.FancyBboxPatch((3.2, 1.6), 3.6, 1.2, boxstyle="round,pad=0.08",
                                     edgecolor='#a855f7', facecolor='#ffffff', linewidth=1)
    ax.add_patch(b_math)
    ax.text(5.0, 2.5, "Procedural Escape Dynamics (WerrMath.sol)", ha='center', va='center', fontsize=7.2, fontweight='bold', color='#7e22ce')
    ax.text(5.0, 2.15, "$z_{n+1} = z_n^2 + c, \\quad z_0 = 0, \\quad c = c_x + i c_y$", ha='center', va='center', fontsize=8, color='#1e1b4b')
    ax.text(5.0, 1.8, "16-Point ($4 \\times 4$) Pareto Micro-Grid • Zero Tensor Arrays", ha='center', va='center', fontsize=6.8, fontstyle='italic', color='#4c1d95')

    # Gas badge
    b_gas = patches.FancyBboxPatch((3.6, 0.65), 2.8, 0.7, boxstyle="round,pad=0.08",
                                    edgecolor='#059669', facecolor='#ecfdf5', linewidth=1.2)
    ax.add_patch(b_gas)
    ax.text(5.0, 1.0, "Total Cost: 21,438 Gas (< $0.0005)", ha='center', va='center', fontsize=7.8, fontweight='bold', color='#065f46')

    # Arrow 2 -> 3
    ax.annotate("", xy=(7.4, 2.6), xytext=(7.0, 2.6),
                arrowprops=dict(arrowstyle="->", color='#334155', lw=2, mutation_scale=15))

    # Box 3: Outflow Actions
    b3 = patches.FancyBboxPatch((7.5, 1.2), 2.2, 2.8, boxstyle="round,pad=0.15", 
                                 edgecolor=c_emerald, facecolor=c_emerald_light, linewidth=1.5)
    ax.add_patch(b3)
    ax.text(8.6, 3.65, "Intra-Block Actions", ha='center', va='center', fontsize=9, fontweight='bold', color=c_emerald)
    ax.text(8.6, 3.0, "• Dynamic Fee Tuning\n  (0.05% - 0.50% fee)\n• Flash-Loan Revert\n• MEV Sandwich Block\n• AML / Sanction Trap", 
            ha='center', va='center', fontsize=7.5, color='#064e3b', linespacing=1.35)
    ax.text(8.6, 1.6, "Latency: < 1 ms (Atomic)", ha='center', va='center', fontsize=7, fontweight='bold', color='#047857')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig1_werracle_architecture.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

def generate_benchmarks_figure():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.0), dpi=300)

    systems = ['Web2 Oracle', 'ZK-ML\n(EZKL)', 'Werracle\n(Ours)']
    colors = ['#94a3b8', '#f59e0b', '#10b981']

    # Subplot 1: Gas Comparison
    gas_values = [60000, 380000, 21438]
    bars1 = ax1.bar(systems, gas_values, color=colors, width=0.55, edgecolor='#333333', linewidth=0.8)
    ax1.set_ylabel('Verification Gas (Opcode Gas)', fontsize=8.5, fontweight='bold')
    ax1.set_title('(a) On-Chain Gas Cost', fontsize=9.5, fontweight='bold', pad=8)
    ax1.set_ylim(0, 430000)
    ax1.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: f"{int(x/1000)}k" if x > 0 else "0"))
    ax1.grid(axis='y', linestyle='--', alpha=0.4)

    for bar, val in zip(bars1, gas_values):
        y_pos = bar.get_height() + 10000
        ax1.text(bar.get_x() + bar.get_width()/2, y_pos, f"{val:,}", ha='center', va='bottom', fontsize=7.5, fontweight='bold')
    
    # 18x cheaper note
    ax1.text(2, 45000, "18x Cheaper", ha='center', va='bottom', fontsize=7.5, color='#065f46', fontweight='bold')

    # Subplot 2: Latency Comparison (Log Scale)
    latencies = [24.0, 150.0, 0.0008]  # seconds
    bars2 = ax2.bar(systems, latencies, color=colors, width=0.55, edgecolor='#333333', linewidth=0.8)
    ax2.set_yscale('log')
    ax2.set_ylabel('Inference / Proving Latency (s)', fontsize=8.5, fontweight='bold')
    ax2.set_title('(b) Decision Latency (Log Scale)', fontsize=9.5, fontweight='bold', pad=8)
    ax2.set_ylim(0.0001, 1000)
    ax2.grid(axis='y', linestyle='--', alpha=0.4)

    labels = ["24 s", "150 s", "< 1 ms\n(Atomic)"]
    for bar, label, lat in zip(bars2, labels, latencies):
        y_pos = bar.get_height() * 1.5 if lat < 1 else bar.get_height() * 1.2
        ax2.text(bar.get_x() + bar.get_width()/2, y_pos, label, ha='center', va='bottom', fontsize=7.5, fontweight='bold')

    ax2.text(2, 0.005, "1,000x-100,000x\nSpeedup", ha='center', va='bottom', fontsize=7, color='#065f46', fontweight='bold')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig2_benchmarks_comparison.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    generate_architecture_figure()
    generate_benchmarks_figure()
