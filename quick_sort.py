# 快速排序演示（简化版）

def quick_sort(arr):
    """快速排序算法"""
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)


# 测试
if __name__ == "__main__":
    test_data = [64, 34, 25, 12, 22, 11, 90]
    print(f"原始数组: {test_data}")
    print(f"排序后:   {quick_sort(test_data)}")
