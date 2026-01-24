import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Set style for academic paper
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['figure.dpi'] = 150

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Generate x values for distribution curves
x = np.linspace(-6, 10, 1000)

# Colors
ref_color = '#2E86AB'  # Blue for reference
cur_color = '#E94F37'  # Red for current

# ===== LEFT PANEL: NO DRIFT =====
ax1 = axes[0]

# Reference distribution (mean=2, std=1)
ref_dist = stats.norm.pdf(x, 2, 1)
# Current distribution (similar - mean=2.1, std=1)
cur_dist = stats.norm.pdf(x, 2.1, 1)

ax1.fill_between(x, ref_dist, alpha=0.4, color=ref_color, label='Reference Data $P_{ref}(X)$')
ax1.fill_between(x, cur_dist, alpha=0.4, color=cur_color, label='Current Data $P_{cur}(X)$')
ax1.plot(x, ref_dist, color=ref_color, linewidth=2)
ax1.plot(x, cur_dist, color=cur_color, linewidth=2)

ax1.set_xlabel('Feature Value (X)', fontweight='bold')
ax1.set_ylabel('Probability Density', fontweight='bold')
ax1.set_title('No Drift: Distributions Overlap', fontweight='bold', pad=10)
ax1.legend(loc='upper right', framealpha=0.9)
ax1.set_xlim(-4, 8)
ax1.set_ylim(0, 0.5)

# Add annotation
ax1.annotate('Classifier cannot\ndistinguish sources\n(AUC ≈ 0.5)', 
             xy=(2, 0.35), fontsize=10, ha='center',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.7))

ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# ===== RIGHT PANEL: DRIFT DETECTED =====
ax2 = axes[1]

# Reference distribution (mean=2, std=1)
ref_dist = stats.norm.pdf(x, 2, 1)
# Current distribution (shifted - mean=5.5, std=1.2)
cur_dist = stats.norm.pdf(x, 5.5, 1.2)

ax2.fill_between(x, ref_dist, alpha=0.4, color=ref_color, label='Reference Data $P_{ref}(X)$')
ax2.fill_between(x, cur_dist, alpha=0.4, color=cur_color, label='Current Data $P_{cur}(X)$')
ax2.plot(x, ref_dist, color=ref_color, linewidth=2)
ax2.plot(x, cur_dist, color=cur_color, linewidth=2)

ax2.set_xlabel('Feature Value (X)', fontweight='bold')
ax2.set_ylabel('Probability Density', fontweight='bold')
ax2.set_title('Drift Detected: Distributions Shifted', fontweight='bold', pad=10)
ax2.legend(loc='upper right', framealpha=0.9)
ax2.set_xlim(-4, 10)
ax2.set_ylim(0, 0.5)

# Add arrow showing shift
ax2.annotate('', xy=(5.5, 0.25), xytext=(2, 0.25),
             arrowprops=dict(arrowstyle='->', color='black', lw=2))
ax2.text(3.75, 0.27, 'Distribution\nShift', ha='center', fontsize=10, fontweight='bold')

# Add annotation
ax2.annotate('Classifier can\ndistinguish sources\n(AUC >> 0.5)', 
             xy=(5.5, 0.42), fontsize=10, ha='center',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.7))

ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('figures/figure-1-new.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('figures/figure-1-new.pdf', dpi=300, bbox_inches='tight', facecolor='white')
print("Figure saved successfully to figures/figure-1-new.png and figures/figure-1-new.pdf")
