def pre_order_transversal(heap):
    def transverse(index):
        if index < len(heap) and heap[index] != "#":
            transverse_result.append(heap[index])

            transverse(2 * index + 1)
            transverse(2 * index + 2)
    
    transverse_result = []
    transverse(0)

    return transverse_result

binary_heap = ['1', '2', '3', '4', '#', '5', '#']
result = pre_order_transversal(binary_heap)
print(result)