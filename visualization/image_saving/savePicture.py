import numpy as np
import matplotlib.pyplot as plt
from math import cos,sin
import os

def PRCurve(recall,precision,path):
    if(isinstance(recall,np.ndarray)):
        assert(recall.shape[0] == precision.shape[0])

    if(isinstance(recall,list)):
        assert(len(recall) == len(precision))

    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.plot(recall,precision)
    plt.savefig(path)
    plt.show()

# save multiple feature
def featureSaving(array,path):
    if not os.path.exist(path):
        os.makedirs(path)
    if(len(array.shape) == 2):
        plt.imsave(array,os.path.join(path,'0.png'))
    elif(len(array.shape) == 3):
        for i in range(array.shape[0]):
            plt.imsave(array[i],os.path.join(path,str(i)+'png'))


# if you just want to save a numpy array, without bbox
# plt.imsave('name',array)

# if you want also to save bbox use fig

def randomColor():
    ret = '#'
    for i in range(6):
        rand = np.random.randint(0,16)
        rand = hex(rand)[-1].upper()
        ret += rand[-1]
    return ret


def displayBboxes(bboxes,random_color=True,linewidth=1):
    '''
    bboxes: N * M   M: w h x y theta x y x y ...
            theta is counterclockwise , ni shi zhen
    '''
    cc = randomColor()
    display_step = int((bboxes.shape[1] - 5) / 2 + 1) 
    for i in range(bboxes.shape[0]):
        w = bboxes[i,0] / 2
        l = bboxes[i,1] / 2
        if(random_color):
            cc = randomColor()
        for j in range(display_step):
            if not j:
                center_x = bboxes[i,2]
                center_y = bboxes[i,3]
                theta = bboxes[i,4]
                costheta = cos(-theta)
                sintheta = sin(-theta)
                template1 = w * np.array([1, -1, 1, -1])
                template2 = l * np.array([1, 1, -1, -1])

                x = template1 * costheta - template2 * sintheta + center_x
                y = template1 * sintheta + template2 * costheta + center_y

                x[x < 0] = 0
                y[y < 0] = 0
                x = np.ceil(x)
                y = np.ceil(y)

                plt.plot([x[0], x[1]], [y[0], y[1]], color=cc, linewidth=linewidth)
                plt.plot([x[1], x[3]], [y[1], y[3]], color=cc, linewidth=linewidth)
                plt.plot([x[3], x[2]], [y[3], y[2]], color=cc, linewidth=linewidth)
                plt.plot([x[2], x[0]], [y[2], y[0]], color=cc, linewidth=linewidth)

            else:
                plt.plot(center_x,center_y,marker='o',markersize=2, color=cc)


def saveFigWithBBox(array,bboxes,path):
    '''
    array: pictures
    bboxes: N * M   M: w h x y theta x y theta x y theta ...
    '''
    plt.clf()
    fig = plt.figure('picWithBboxes')
    plt.imshow(array)
    displayBboxes(bboxes)
    plt.savefig(path)


if __name__ == "__main__":
    a = [1,2,3]
    b = [1,2,3]
    #PRCurve(a,b,'test.png')
    a = np.array([100,50,200,200,np.pi/3]).reshape(1,5)
    pics = np.zeros((500,500))
    saveFigWithBBox(pics,a,'bbox.png')
