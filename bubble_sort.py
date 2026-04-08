# 冒泡排序演示（简化版）

def bubble_sort(arr):
    """冒泡排序算法"""
    n = len(arr)
    arr = arr.copy()
    
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # 如果没有交换，说明已经有序
        if not swapped:
            break
    
    return arr


# 测试
if __name__ == "__main__":
    test_data = [64, 34, 25, 12, 22, 11, 90]
    print(f"原始数组: {test_data}")
    print(f"排序后:   {bubble_sort(test_data)}")
