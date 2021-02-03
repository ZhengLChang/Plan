from io import StringIO
import math

class heap_topK(object):
    def __init__(self, compare_func=None, init_arr=list(), K = 100):
        #self.arr = list(set(init_arr))
        self.K = K
        
        if compare_func is not None:
            self.compare_func = compare_func
        else:
            self.compare_func = heap_topK.default_compare_func
        self.arr = list()
        for num in init_arr:
            self.add(num)
    @staticmethod
    def default_compare_func(argv1, argv2):
        if argv1 >= argv2:
            return True
        if argv1 < argv2:
            return False
    def heap_adjust(self, arr, arr_len, index):
        leftIdx = 2 * index + 1
        rightIdx = 2 * index + 2

        maxIdx = index

        if leftIdx < arr_len and self.compare_func(arr[maxIdx], arr[leftIdx]) is True:
            maxIdx = leftIdx

        if rightIdx < arr_len and self.compare_func(arr[maxIdx], arr[rightIdx]) is True:
            maxIdx = rightIdx

        if maxIdx != index:
            tmp = arr[index]
            arr[index] = arr[maxIdx]
            arr[maxIdx] = tmp
            self.heap_adjust(arr, arr_len, maxIdx)
    @property
    def result(self):
        tmp_arr = list(self.arr)
        for i in range(len(tmp_arr) - 1, -1, -1):
            tmp = tmp_arr[0]
            tmp_arr[0] = tmp_arr[i]
            tmp_arr[i] = tmp
            self.heap_adjust(tmp_arr, i, 0)
        return tmp_arr

    def heap_sort(self):
        arr_len = len(self.arr)
        last_non_leaf_node = int(arr_len / 2) - 1
        for i in range(last_non_leaf_node, -1, -1):
            self.heap_adjust(self.arr, arr_len, i)
        return self.arr

    def add(self, new_num):
        print(len(self.arr))
        if type(new_num) == int or type(new_num) == dict:
            #if new_num in self.arr:
            # return
            if len(self.arr) == 0:
                self.arr.append(new_num) 
                return 

            if len(self.arr) < self.K:
                self.arr.append(new_num)
                self.heap_sort()
                return

            if self.compare_func(new_num, self.arr[0]):
                self.arr[0] = new_num
                self.heap_adjust(self.arr, len(self.arr), 0)
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
    obj = heap_topK(init_arr = [8, 5])
    a = [2, 22, 1, 5, 19, 9, 4, 10, 11]
    #obj.add(a)
    for i in a:
       obj.add(i)
    obj.show_tree()
    print(obj.result)



