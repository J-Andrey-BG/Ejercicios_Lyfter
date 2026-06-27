def bubble_sort(number_list):
    n = len(number_list)
    for i in range(n):
        for j in range(0, n-i-1):
            if number_list[j] > number_list[j+1]:
                number_list[j], number_list[j+1] = number_list[j+1], number_list[j]
    return number_list