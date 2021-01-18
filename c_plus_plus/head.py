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

def max_head(arr, arr_len, index):
    leftIdx = 2 * index + 1
    rightIdx = 2 * index + 2

    maxIdx = index

    if leftIdx < arr_len and arr[leftIdx] > arr[maxIdx]:
        maxIdx = leftIdx

    if rightIdx < arr_len and arr[rightIdx] > arr_len:
        maxIdx = rightIdx

    if maxIdx != index:
        tmp = arr[index]
        arr[index] = arr[maxIdx]
        arr[maxIdx] = tmp
        max_head(arr, len(arr), maxIdx)

a = [19, 9, 4, 10, 11]
for i in range(int(len(a) / 2) - 1, 0, -1):
    max_head(a, len(a), i)
show_tree(a)
print(a)
