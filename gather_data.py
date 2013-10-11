import pylab as pl
import os

def get_ratio(cal_file):
    line = cal_file.readline()
    print('line is: ' +str(line))
    print('line[:line.find(\'p\')] is: '+str(line[:line.find('p')]))
    num_px = float(line[:line.find('p')])
    num_mm = float(line[line.find('=')+1:line.find('m')])
    ratio = num_mm/num_px
    print('rato is: ' +str(ratio))
    
    return ratio

# data is the data from data.txt. 
def get_pos_vel(data,ratio):
    data = data*ratio

    # get in one dimension
    r = pl.sqrt(data[:,0]**2 + data[:,1]**2)
    # print('r is: ' + str(r))
    # put min value at the origin
    r = r - r.min()
    vr = r[1:]-r[:-1]
    r = r[1:]
    # with min val at origin it is easy to cetre
    # centre about origin
    r = r - r.max()/2.0

    return r,vr

# get_label(f_name) takes the file name string and turns it into the string we want to have in the
# legend of the plot.
#Needs to be smart in choosing weather to displya KV or Hz... Thats why we pass it look at
def get_label(f_name,look_at):
    if 'Hz' in look_at:
        # we go to 'V' and add 1 just incase we used a lowercase 'p' in the file name
        f_name = f_name[:(f_name.find('V')+1)]
        new = ''
        i = 0
        while i < len(f_name):
            if f_name[i] =='P':
                new = new + '.'
                i += 3
            new = new + f_name[i]
            i += 1

        return new
    if 'KV' in look_at:
        # we go to 'V' and add 1 just incase we used a lowercase 'p' in the file name
        f_name = f_name[(f_name.find('_')+1):]
        new = ''
        i = 0
        while i < len(f_name):
            if f_name[i] =='P':
                new = new + '.'
                i += 3
            new = new + f_name[i]
            i += 1
        return new
           

def main():
    # We are going to need to goup the data apropriately. For now this will mean only working with one
    # particle at a time and only looking at variation in frequency OR driving amplitude. The only
    # tricky part is going to be colecting and putting together the data of different calibrations.

    vid = 'Vids080413'
    # There may be differet movies with different zoom s
    # directory we need to specify is which movie.
    # named as follows:
    # Particle_<integer starting at 0 going up>
    vid_num = 'Particle_0'
    
    # 'look_at' is the choice of Hz or KVpp variations
    # This will pull all voltages for 3Hz of this particle
    #look_at = '3Hz'
    look_at = '1Pnt2KVpp'

    # list stores the names of the clibration files
    os.chdir(vid+'/'+vid_num)

    # calibration files
    calibs = os.listdir('.')

    fig = pl.figure()
    ax = fig.add_subplot(111)
    ax.set_ylim([-.5,.5])
    ax.set_ylabel(r'$x$'      ,fontsize = 35)
    ax.set_xlabel(r'$\dot{x}$',fontsize = 35)

    some_colors = ['b','c','g','k','r','y']
    # Flip options:
    # Whats this mean? depending on which 'way' the particle is boincing we might want to filp the
    # scatter plott across the velocity axis. Method: make first image. define which colors need to
    # be fliped.
    # fo 3Hz particle 0 vids flip = ['b']
    flip = ['b']

    # omit which colors
    #for 3Hz particle 0 vids omit = ['k']
    omit = ['g']
        
    
    number = 0
    for i,j in enumerate(calibs):
        if 'Calibration_' in j:
            cal_file = open(j+'/calibration.txt','r')
            ratio = get_ratio(cal_file)
            cal_file.close()
            print('j is: ' + str(j))
            for a,b in enumerate(os.listdir(j)):
                if look_at in b:
                    if some_colors[number] in omit:
                        number+=1
                        continue
                    print('b is: ' + str(b))

                    data = pl.genfromtxt(j+'/'+b+'/data.txt',comments='x')
                    # need to give get_pos_vel data and ratio so everything ends up in the same
                    # units
                    pos,vel = get_pos_vel(data,ratio)
                    # flip chosen colors. 
                    if some_colors[number] in flip:
                        pos = -pos
                    #print('pos is: ' + str(pos))
                    #print('vel is: ' + str(vel))
                    ax.scatter(pos,vel,color = some_colors[number],label=get_label(b,look_at))
                    print('number is: '+ str(number))
                    number += 1


    os.chdir('/Users/OwewO/Desktop')

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    fig.tight_layout()
    fig.savefig('agrogated_data.png')
    os.system('open agrogated_data.png')

if __name__ == '__main__':
    main()
