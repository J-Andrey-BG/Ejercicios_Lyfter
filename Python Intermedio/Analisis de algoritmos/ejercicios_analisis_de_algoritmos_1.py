# Worst case = O(n^2)
def bubble_sort(number_list): 
    n = len(number_list) # O(1)
    for i in range(n):  # O(n)
        for j in range(0, n-i-1): # O(n^2)
            if number_list[j] > number_list[j+1]: # O(1)
                number_list[j], number_list[j+1] = number_list[j+1], number_list[j] # O(1)
    return number_list # O(1)