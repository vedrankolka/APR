import numpy as np
import pandas
import matplotlib.pyplot as plt

bf_3_bit_schaffers = np.load('zad3_data/3_variables_bitvector_schaffers.npy')
bf_6_bit_schaffers = np.load('zad3_data/6_variables_bitvector_schaffers.npy')
bf_3_double_schaffers = np.load('zad3_data/3_variables_doubles_schaffers.npy')
bf_6_double_schaffers = np.load('zad3_data/6_variables_doubles_schaffers.npy')
bf_3_bit_almost_schaffers = np.load('zad3_data/3_variables_bitvector_almost_schaffers.npy')
bf_6_bit_almost_schaffers = np.load('zad3_data/6_variables_bitvector_almost_schaffers.npy')
bf_3_double_almost_schaffers = np.load('zad3_data/3_variables_doubles_almost_schaffers.npy')
bf_6_double_almost_schaffers = np.load('zad3_data/6_variables_doubles_almost_schaffers.npy')

bitvector_fitnesses = np.array([bf_3_bit_schaffers, bf_3_bit_almost_schaffers, bf_6_bit_schaffers, bf_6_bit_almost_schaffers]).reshape(1, 40)
doubles_fitnesses = np.array([bf_3_double_schaffers, bf_3_double_almost_schaffers, bf_6_double_schaffers, bf_6_double_almost_schaffers]).reshape(1, 40)


def compare(arr1, label1, arr2, label2, function):
    arr1_success_count = np.sum(arr1 >= -1e-6)
    arr2_success_count = np.sum(arr2 >= -1e-6)
    if arr1_success_count == arr2_success_count:
        arr1_median = np.median(arr1)
        arr2_median = np.median(arr2)
        if arr1_median > arr2_median:
            print(label1, 'is better than', label2, 'on', function)
        else:
            print(label2, 'is better than', label1, 'on', function)
    elif arr1_success_count > arr2_success_count:
        print(label1, 'is better than', label2, 'on', function)
    else:
        print(label2, 'is better than', label1, 'on', function)


compare(bf_3_bit_schaffers, '3 variables bitvector', bf_3_double_schaffers, '3 variables doubles', 'Schaffers function')
compare(bf_6_bit_schaffers, '6 variables bitvector', bf_6_double_schaffers, '6 variables doubles', 'Schaffers function')
compare(bf_3_bit_almost_schaffers, '3 variables bitvector', bf_3_double_almost_schaffers, '3 variables doubles', 'almost Schaffers')
compare(bf_6_bit_almost_schaffers, '6 variables bitvector', bf_6_double_almost_schaffers, '6 variables doubles', 'almost Schaffers')

data = np.array([bf_3_bit_schaffers, bf_6_bit_schaffers])

df = pandas.DataFrame(np.transpose(data), columns=['schaffers 3 variables', 'schaffers 6 variables'])
df.boxplot()
plt.show()
