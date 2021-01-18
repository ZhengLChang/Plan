from io import StringIO
import math

class head_topK(object):
    K = 3
    def __init__(self, init_arr=list()):
        self.arr = init_arr
        for num in self.arr:
            self.add(num)

    def head_adjust(self, arr, arr_len, index):
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
            self.head_adjust(arr, arr_len, maxIdx)

    def min_head(self):
        arr_len = len(self.arr)
        last_non_leaf_node = int(arr_len / 2) - 1
        for i in range(last_non_leaf_node, -1, -1):
            self.head_adjust(self.arr, arr_len, i)
        return self.arr

    def add(self, new_num):
        if type(new_num) == int:
            if len(self.arr) == 0:
                self.arr.append(new_num) 
                return 

            if len(self.arr) < head_topK.K:
                self.arr.append(new_num)
                self.min_head()
                return
            if new_num > self.arr[0]:
                self.arr[0] = new_num
                self.head_adjust(self.arr, len(self.arr), 0)
                return
        elif type(new_num) == list:
            for num in new_num:
                self.add(num)

    def show_tree(self, total_width=36, fill=' '):
        """漂亮的打印一棵树。"""
        print(self.arr)
        output = StringIO()
        last_row = -1
        for i, n in enumerate(self.arr):
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



if __name__ == "__main__":
    obj = head_topK([8, 5])
    a = [22, 1, 19, 9, 4, 10, 11]
    obj.add(a)
    #for i in a:
    #    obj.add(i)
    obj.show_tree()



