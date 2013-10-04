import numpy as np
import scipy
import scipy.ndimage as ndimage
import scipy.ndimage.filters as filters
import matplotlib.pyplot as plt
import os

def main():
    # Need to controle everything from this spot in the directory tree
    # Define some variables that tell the program where the file of images we want analized is.
    # vid is a string just containing the name of the dated file we want to work with. 
    # labeled as folows:
    # Vid<date in month day year>
    vid = 'Vids080413'
    # There may be differet movies with different zoom setings and different particles. The next
    # directory we need to specify is which movie.
    # named as follows:
    # Particle_<integer starting at 0 going up>
    vid_num = 'Particle_0'
    # Next we specify the folder for videos that share the same calibration (zoom value or whatnot).
    calibration = 'Calibration_0'
    # Next we specify the folder with the images laid out in it. These are named as folows:
    # ("Pnt" if required")<number of killavolts>KVpp_<driving frequency>Hz
    im_file = '10000KVpp_10000Hz'

    # pretty self explanitory. If you do the images made are just the ones with the arrow (no dot)
    do_you_want_images = False

    # this is going to be the array that stors all the particle positiongs over the corse of teh
    # video
    particle_pos = np.array([])

    # get to the right directory and extract the numbers from the file names (convinient later on)
    os.chdir(vid+'/'+vid_num+'/'+im_file)
    kil_v_pp = im_file[:im_file.find('K')]
    hz = im_file[(im_file.find('_')+1):im_file.find('H')]
    print('current directory is: '+os.getcwd()+'\n'+'KVpp is: '+kil_v_pp+'\n'+'Hz is: '+hz)

    if do_you_want_images:
        os.mkdir('./Labeled')

    all_files = os.listdir('.')
    all_images = []
    for i,j in enumerate(all_files):
        if 'png' in j:
            all_images.append(j)

    for i,j in enumerate(all_images): 
        neighborhood_size = 5
        threshold = 100
        
        data = scipy.misc.imread(j)
        
        data_max = filters.maximum_filter(data, neighborhood_size)
        #print('data_max = filters.maximum_filter(data, neighborhood_size) is: ' +str(data_max))
        maxima = (data == data_max)
        #print('maxima = (data == data_max) is :' + str(maxima )) 
        data_min = filters.minimum_filter(data, neighborhood_size)
        #print('data_min = filters.minimum_filter(data, neighborhood_size) is: ' +str(data_min))
        diff = ((data_max - data_min) > threshold)
        #print(' diff = ((data_max - data_min) > threshold) is: ' + str(diff))
        maxima[diff==0] = 0
        #print(' maxima[diff==0] (set to zero) is: ' + str(maxima[diff==0]))
        
        labeled, num_objects = ndimage.label(maxima)
        #print('labeled is: ' + str(labeled))
        #print('num_objects is: ' + str(num_objects))
        
        slices = ndimage.find_objects(labeled)
        #print('slices = ndimage.find_objects(labeled) is: ' + str(slices))

        # slices is strange. it is a tuple. in this case the tuple is (#,#,None) wich is why
        # 'notmuch' is just a place holder.
        x, y = [], []
        for dy, dx, notmuch in slices:
            print('in dy,dx loop number -> '+str(i))
            x_center = (dx.start + dx.stop - 1)/2
            x.append(x_center)
            y_center = (dy.start + dy.stop - 1)/2
            y.append(y_center)

        
        particle_pos = np.append(particle_pos,x[0])
        particle_pos = np.append(particle_pos,y[0])
        
        print('len(x) is: '+str(len(x)))
        print('x is: ' + str(x))

        if do_you_want_images:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.imshow(data)
            #plt.savefig('/tmp/data.png',bbox_inches = 'tight')
            # this is just for the ploting
            if i == 0:
                first_x = x
                first_y = y
            ax.autoscale(False)
            #ax.plot(x,y, 'ro')
            ax.annotate('', xy=(x,y),color='white',
                    xytext=(first_x+120.0,first_y+120.0),arrowprops=dict(facecolor='white',shrink=0.05))
            fig.savefig('Labeled/'+str(i)+'result.png', bbox_inches = 'tight')
    
    print('particle_pos is: ' + str(particle_pos))
    print('len(particle_pos) is: ' + str(len(particle_pos)))
    particle_pos = particle_pos.reshape(-1,2)
    x_vals = particle_pos[:,0]
    vx_vals = x_vals[1:]-x_vals[:-1]
    x_vals = x_vals[1:]

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.set_xlabel(r'$x$'      , fontsize=20.0)
    ax1.set_ylabel(r'$\dot{x}$', fontsize=20.0)
    ax1.plot(x_vals,vx_vals)
    fig1.savefig('x_vx_'+kil_v_pp+'KVpp_'+hz+'Hz'+'.png')
        
    
if __name__ == '__main__':
    main()
