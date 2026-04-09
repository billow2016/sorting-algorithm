import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import copy


class SortingVisualizer:
    def __init__(self, data):
        self.data = data
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.bars = self.ax.bar(range(len(data)), data, color='skyblue')
        self.ax.set_title('Sorting Algorithm Visualization')
        self.ax.set_xlabel('Index')
        self.ax.set_ylabel('Value')
        self.ax.set_ylim(0, max(data) * 1.1)
        
    def update_bars(self, colors=None):
        """更新柱状图颜色和高度"""
        for i, (bar, val) in enumerate(zip(self.bars, self.data)):
            bar.set_height(val)
            if colors:
                bar.set_color(colors[i])
            else:
                bar.set_color('skyblue')
        return self.bars
    
    def quick_sort_generator(self, arr, low, high):
        """快速排序生成器，用于动画"""
        if low < high:
            pi = yield from self.partition(arr, low, high)
            yield from self.quick_sort_generator(arr, low, pi - 1)
            yield from self.quick_sort_generator(arr, pi + 1, high)
    
    def partition(self, arr, low, high):
        """快速排序的分区函数"""
        pivot = arr[high]
        i = low - 1
        
        colors = ['skyblue'] * len(arr)
        colors[high] = 'red'  # pivot
        
        for j in range(low, high):
            colors[j] = 'yellow'  # 正在比较
            yield colors.copy()
            
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                colors[i] = 'green'  # 交换后
                colors[j] = 'green'
                yield colors.copy()
            
            colors[j] = 'skyblue'
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        colors[i + 1] = 'purple'  # 已就位
        yield colors.copy()
        
        return i + 1
    
    def bubble_sort_generator(self, arr):
        """冒泡排序生成器，用于动画"""
        n = len(arr)
        sorted_indices = []  # 已排序的索引
        
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                colors = ['skyblue'] * len(arr)
                colors[j] = 'yellow'
                colors[j + 1] = 'yellow'
                
                # 标记已排序的部分
                for k in range(n - i, n):
                    colors[k] = 'purple'
                
                yield colors.copy()
                
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
                    colors[j] = 'green'
                    colors[j + 1] = 'green'
                    yield colors.copy()
            
            # 标记这一轮最后一位已排序
            sorted_indices.append(n - i - 1)
            if not swapped:
                # 剩余的都是已排序
                for k in range(n - i - 1):
                    if k not in sorted_indices:
                        sorted_indices.append(k)
                break
        
        # 全部排序完成
        yield ['purple'] * len(arr)
    
    def animate_quick_sort(self):
        """快速排序动画"""
        self.ax.set_title('Quick Sort Visualization')
        data_copy = copy.deepcopy(self.data)
        self.data = data_copy
        
        gen = self.quick_sort_generator(self.data, 0, len(self.data) - 1)
        
        def update(frame):
            try:
                colors = next(gen)
                self.update_bars(colors)
            except StopIteration:
                self.update_bars(['purple'] * len(self.data))
            return self.bars
        
        anim = animation.FuncAnimation(
            self.fig, update, frames=500, interval=50, blit=False, repeat=False
        )
        plt.show()
    
    def animate_bubble_sort(self):
        """冒泡排序动画"""
        self.ax.set_title('Bubble Sort Visualization')
        data_copy = copy.deepcopy(self.data)
        self.data = data_copy
        
        gen = self.bubble_sort_generator(self.data)
        frames = []
        
        try:
            while True:
                frames.append(next(gen))
        except StopIteration:
            pass
        
        def update(frame_idx):
            if frame_idx < len(frames):
                self.update_bars(frames[frame_idx])
            return self.bars
        
        anim = animation.FuncAnimation(
            self.fig, update, frames=len(frames), interval=100, blit=False, repeat=False
        )
        plt.show()
    
    def compare_algorithms(self):
        """对比两种排序算法 - 同步动画"""
        # 创建两个独立的数据副本
        data_quick = copy.deepcopy(self.data)
        data_bubble = copy.deepcopy(self.data)
        
        # 创建双子图
        self.fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # 设置柱子
        bars1 = ax1.bar(range(len(data_quick)), data_quick, color='skyblue')
        bars2 = ax2.bar(range(len(data_bubble)), data_bubble, color='skyblue')
        
        # 设置标题和标签
        ax1.set_title('Quick Sort', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Index')
        ax1.set_ylabel('Value')
        ax1.set_ylim(0, max(self.data) * 1.1)
        
        ax2.set_title('Bubble Sort', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Index')
        ax2.set_ylabel('Value')
        ax2.set_ylim(0, max(self.data) * 1.1)
        
        plt.tight_layout()
        
        # 获取两个排序算法的生成器
        gen_quick = self.quick_sort_generator(data_quick, 0, len(data_quick) - 1)
        gen_bubble = self.bubble_sort_generator(data_bubble)
        
        # 预计算所有帧
        frames_quick = []
        frames_bubble = []
        
        try:
            while True:
                frames_quick.append(next(gen_quick))
        except StopIteration:
            pass
        
        try:
            while True:
                frames_bubble.append(next(gen_bubble))
        except StopIteration:
            pass
        
        max_frames = max(len(frames_quick), len(frames_bubble))
        
        def update(frame_idx):
            # 更新快速排序
            if frame_idx < len(frames_quick):
                colors = frames_quick[frame_idx]
                for i, bar in enumerate(bars1):
                    bar.set_height(data_quick[i])
                    bar.set_color(colors[i])
            
            # 更新冒泡排序
            if frame_idx < len(frames_bubble):
                colors = frames_bubble[frame_idx]
                for i, bar in enumerate(bars2):
                    bar.set_height(data_bubble[i])
                    bar.set_color(colors[i])
            
            return list(bars1) + list(bars2)
        
        anim = animation.FuncAnimation(
            self.fig, update, frames=max_frames, interval=50, blit=False, repeat=False
        )
        plt.show()


def main():
    """主函数"""
    # 生成随机数据
    data_size = 30
    data = [random.randint(10, 100) for _ in range(data_size)]
    
    print("排序算法可视化")
    print("=" * 40)
    print("1. 快速排序可视化")
    print("2. 冒泡排序可视化")
    print("3. 算法对比（同步动画）")
    print("=" * 40)
    
    choice = input("请选择 (1/2/3): ").strip()
    
    visualizer = SortingVisualizer(data)
    
    if choice == '1':
        print("正在展示快速排序...")
        visualizer.animate_quick_sort()
    elif choice == '2':
        print("正在展示冒泡排序...")
        visualizer.animate_bubble_sort()
    elif choice == '3':
        print("正在展示算法对比...")
        visualizer.compare_algorithms()
    else:
        print("无效选择，默认展示快速排序")
        visualizer.animate_quick_sort()


if __name__ == "__main__":
    main()
