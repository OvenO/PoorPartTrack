import numpy as np
import scipy
import scipy.ndimage as ndimage
import scipy.ndimage.filters as filters
import matplotlib.pyplot as plt

def main():

    file_name = '1KVpp_2Hz 006.png'
    neighborhood_size = 5
    threshold = 100
    
    data = scipy.misc.imread(file_name)
    
    data_max = filters.maximum_filter(data, neighborhood_size)
    print('data_max = filters.maximum_filter(data, neighborhood_size) is: ' +str(data_max))
    maxima = (data == data_max)
    print('maxima = (data == data_max) is :' + str(maxima )) 
    data_min = filters.minimum_filter(data, neighborhood_size)
    print('data_min = filters.minimum_filter(data, neighborhood_size) is: ' +str(data_min))
    diff = ((data_max - data_min) > threshold)
    print(' diff = ((data_max - data_min) > threshold) is: ' + str(diff))
    maxima[diff==0] = 0
    print(' maxima[diff==0] (set to zero) is: ' + str(maxima[diff==0]))
    
    labeled, num_objects = ndimage.label(maxima)
    print('labeled is: ' + str(labeled))
    print('num_objects is: ' + str(num_objects))
    
    slices = ndimage.find_objects(labeled)
    print('slices = ndimage.find_objects(labeled) is: ' + str(slices))
    x, y = [],[]
    for dy, dx, notmuch in slices:
        x_center = (dx.start + dx.stop - 1)/2
        x.append(x_center)
        y_center = (dy.start + dy.stop - 1)/2
        y.append(y_center)
    
    print('after loop vars')
    print('x_center = (dx.start + dx.stop - 1)/2 is: ' +str(x_center))
    print('y_center = (dy.start + dy.stop - 1)/2 is: ' + str(y_center))
    
    
    plt.imshow(data)
    plt.savefig('/tmp/data.png',bbox_inches = 'tight')
    
    plt.autoscale(False)
    plt.plot(x,y, 'ro')
    plt.savefig('/tmp/result.png', bbox_inches = 'tight')
        
    
if __name__ == '__main__':
    main()
