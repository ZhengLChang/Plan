from io import StringIO
import math

def show_tree(tree, total_width=36, fill=' '):
    """漂亮的打印一棵树。"""
    output = StringIO()
    last_row = -1
    for i, n in enumerate(tree):
        if i:
            row = int(math.floor(math.log(i + 1, 2)))
        else:
            row = 0
        if row != last_row:
            output.write('\n')
        columns = 2 ** row
        col_width = int(math.floor(total_width / columns))
        output.write(str(n).center(col_width, fill))
        last_row = row
    print(output.getvalue())
    print('-' * total_width)
    print()


def head_adjust(arr, arr_len, index):
    print(f"index: {index}")
    leftIdx = 2 * index + 1
    rightIdx = 2 * index + 2

    maxIdx = index

    if leftIdx < arr_len and arr[leftIdx] < arr[maxIdx]:
        maxIdx = leftIdx

    if rightIdx < arr_len and arr[rightIdx] < arr[maxIdx]:
        maxIdx = rightIdx

    if maxIdx != index:
        tmp = arr[index]
        arr[index] = arr[maxIdx]
        arr[maxIdx] = tmp
        head_adjust(arr, arr_len, maxIdx)

def max_head(arr):
    tmp_arr = list(arr)
    len_arr = len(tmp_arr)
    last_non_leaf_node = int(len_arr / 2) - 1
    print(f"{tmp_arr} => {len_arr} {last_non_leaf_node}")
    for i in range(last_non_leaf_node, -1, -1):
        head_adjust(tmp_arr, len_arr, i)
    return tmp_arr


a = [22, 1, 19, 9, 4, 10, 11]
import time
new_a = max_head(a)
#begin = time.time()
#a = sorted(a)
print(a)
print(new_a)
show_tree(new_a)
#print(f"{time.time() - begin}")
