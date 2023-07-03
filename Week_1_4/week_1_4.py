def implemention_function_data(data, function_list):

    new_data = [[function(data[counter]) for counter in range(len(data))]
                 for function in function_list]

    return new_data

multiply_two = lambda x : 2 * x
multiply_four = lambda x : 4 * x
multiply_eight = lambda x : 8 * x

functions = [multiply_two, multiply_four, multiply_eight]
data_list = [1,2,3,4,5]

new_list = implemention_function_data(data_list, functions)
print(new_list)

