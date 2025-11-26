import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def generate_normal_distribution():
    """
    生成正态分布数据并进行分析
    """
    print("=" * 60)
    print("正态分布数据可视化分析")
    print("=" * 60)

    # 设置随机种子以保证结果可重现
    np.random.seed(42)

    # 生成1000个服从标准正态分布N(0,1)的数值
    data = np.random.randn(1000)

    # 计算基本统计量
    mean = np.mean(data)
    std = np.std(data)
    median = np.median(data)
    data_range = [np.min(data), np.max(data)]

    print(f"生成数据统计信息:")
    print(f"  样本数量: {len(data)}")
    print(f"  均值 (μ): {mean:.6f} (理论值: 0.000000)")
    print(f"  标准差 (σ): {std:.6f} (理论值: 1.000000)")
    print(f"  中位数: {median:.6f}")
    print(f"  数据范围: [{data_range[0]:.4f}, {data_range[1]:.4f}]")

    return data, mean, std, data_range


def plot_normal_distribution(data, mean, std, data_range):
    """
    绘制正态分布数据的各种图形
    """
    # 创建图形和子图布局
    fig = plt.figure(figsize=(15, 10))
    fig.suptitle('Normal Distribution N(0,1) Visualization', fontsize=16, fontweight='bold')

    # 子图1：折线图 - 显示数据序列
    ax1 = plt.subplot(2, 2, 1)
    plt.plot(data, alpha=0.7, color='blue', linewidth=0.8)
    plt.axhline(y=mean, color='red', linestyle='--', alpha=0.8, label=f'Mean: {mean:.3f}')
    plt.axhline(y=mean + std, color='orange', linestyle=':', alpha=0.6, label=f'μ+σ: {mean + std:.3f}')
    plt.axhline(y=mean - std, color='orange', linestyle=':', alpha=0.6, label=f'μ-σ: {mean - std:.3f}')
    plt.title('Data Sequence Line Chart (1000 samples)', fontsize=12)
    plt.xlabel('Sample Index')
    plt.ylabel('Value')
    plt.legend(fontsize=9)
    plt.grid(True, alpha=0.3)

    # 子图2：直方图 - 默认bin数
    ax2 = plt.subplot(2, 2, 2)
    n_default, bins_default, patches_default = plt.hist(data, bins='auto',
                                                        alpha=0.7, color='green',
                                                        edgecolor='black', linewidth=0.5)
    plt.axvline(mean, color='red', linestyle='--', alpha=0.8, label=f'Mean: {mean:.3f}')
    plt.title(f'Histogram (Default bins: {len(bins_default) - 1})', fontsize=12)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # 子图3：直方图 - 指定bin=100
    ax3 = plt.subplot(2, 2, 3)
    n_100, bins_100, patches_100 = plt.hist(data, bins=100,
                                            alpha=0.7, color='purple',
                                            edgecolor='black', linewidth=0.3)
    plt.axvline(mean, color='red', linestyle='--', alpha=0.8, label=f'Mean: {mean:.3f}')
    plt.title('Histogram (bins=100)', fontsize=12)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # 子图4：概率密度函数对比
    ax4 = plt.subplot(2, 2, 4)
    # 绘制数据的直方图（归一化）
    n, bins, patches = plt.hist(data, bins=30, density=True,
                                alpha=0.6, color='lightblue',
                                edgecolor='black', label='Data Distribution')

    # 绘制理论正态分布曲线
    x = np.linspace(data_range[0], data_range[1], 100)
    theoretical_pdf = stats.norm.pdf(x, 0, 1)  # 理论N(0,1)的PDF
    plt.plot(x, theoretical_pdf, 'r-', linewidth=2, label='Theoretical N(0,1)')

    plt.title('Probability Density Function Comparison', fontsize=12)
    plt.xlabel('Value')
    plt.ylabel('Probability Density')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    return len(bins_default) - 1


def analyze_distribution_properties(data, mean, std):
    """
    分析分布特性
    """
    print("\n" + "=" * 50)
    print("Distribution Properties Analysis")
    print("=" * 50)

    # 计算落在不同标准差范围内的数据比例
    within_1_std = np.sum((data >= mean - std) & (data <= mean + std)) / len(data)
    within_2_std = np.sum((data >= mean - 2 * std) & (data <= mean + 2 * std)) / len(data)
    within_3_std = np.sum((data >= mean - 3 * std) & (data <= mean + 3 * std)) / len(data)

    print("Data Distribution Range Analysis:")
    print(f"  Within μ±σ range: {within_1_std:.4f} (theoretical: 0.6827)")
    print(f"  Within μ±2σ range: {within_2_std:.4f} (theoretical: 0.9545)")
    print(f"  Within μ±3σ range: {within_3_std:.4f} (theoretical: 0.9973)")

    # 正态性检验
    print("\nNormality Tests:")
    try:
        shapiro_stat, shapiro_p = stats.shapiro(data)
        print(f"  Shapiro-Wilk test p-value: {shapiro_p:.6f}")
        if shapiro_p > 0.05:
            print("  → Data follows normal distribution (p > 0.05)")
        else:
            print("  → Data does not follow normal distribution (p ≤ 0.05)")
    except Exception as e:
        print(f"  Shapiro-Wilk test failed: {e}")

    # KS检验
    try:
        ks_stat, ks_p = stats.kstest(data, 'norm', args=(0, 1))
        print(f"  Kolmogorov-Smirnov test p-value: {ks_p:.6f}")
        if ks_p > 0.05:
            print("  → Data follows standard normal distribution N(0,1) (p > 0.05)")
        else:
            print("  → Data does not follow standard normal distribution N(0,1) (p ≤ 0.05)")
    except Exception as e:
        print(f"  KS test failed: {e}")


def main():
    """
    主函数
    """
    print("Normal Distribution Data Visualization Program")
    print("Using NumPy.random.randn() to generate standard normal distribution N(0,1) data")

    # 生成和分析数据
    data, mean, std, data_range = generate_normal_distribution()

    # 绘制图形
    default_bins = plot_normal_distribution(data, mean, std, data_range)
    print(f"\nDefault number of bins in histogram: {default_bins}")

    # 分析分布特性
    analyze_distribution_properties(data, mean, std)

    # 显示一些数据样本
    print(f"\nData samples (first 10 values):")
    print([f"{x:.4f}" for x in data[:10]])


if __name__ == "__main__":
    main()