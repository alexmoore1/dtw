from numpy import array, zeros, argmin, inf
import wfdb

DEBUG = False

def dtw(x, y):
    
    len_x, len_y = len(x), len(y)
    ary0 = zeros((len_x + 1, len_y + 1))
    ary0[0, 1:] = inf
    ary0[1:, 0] = inf
    ary1 = ary0[1:, 1:]
    for i in range(len_x):
        for j in range(len_y):
            ary1[i, j] = abs(x[i] - y[j])
 
    for i in range(len_x):
        for j in range(len_y):
            ary1[i, j] += min(ary0[i, j], ary0[i, j+1], ary0[i+1, j])
            
    if DEBUG:
        print('--- ary0 ---')
        print(ary0)
        print('--- ary1 ---')
        print(ary1)
        
    path = backpoint(ary0)
    distance = ary1[-1, -1] / sum(ary1.shape)

    return path, distance
    
def backpoint(ary0):
    x, y = ary0.shape
    i = x - 2
    j = y - 2
    a = [i]
    b = [j]
    while ((i > 0) or (j > 0)):
        traceback = argmin( (ary0[i, j], ary0[i, j+1], ary0[i+1, j]) )
        if traceback == 0:
            i -= 1
            j -= 1
        elif traceback == 1:
            i -= 1
        else: # traceback == 2:
            j -= 1
            
        a.insert(0, i)
        b.insert(0, j)
        
        path = ( array(a), array(b) )
    return path

def calc_distances(x,y):
    distances = zeros((len(y), len(x)))
    for i in range(len(y)):
        for j in range(len(x)):
            distances[i,j] = (x[j]-y[i])**2
    return distances

def calc_costs(x, y):
    distances = calc_distances(x,y)
    costs = zeros((len(y), len(x)))
    costs[0,0] = distances[0,0]
    for i in range(1, len(x)):
        costs[0,i] = distances[0,i] + costs[0, i-1]
    for i in range(1, len(y)):
        costs[i,0] = distances[i, 0] + costs[i-1, 0]
    for i in range(1, len(y)):
        for j in range(1, len(x)):
            costs[i, j] = min(costs[i-1, j-1], costs[i-1, j], costs[i, j-1]) + distances[i, j]
    return costs, distances

def path_cost(x, y, costs, distances):
    path = [[len(x)-1, len(y)-1]]
    cost = 0
    i = len(y)-1
    j = len(x)-1
    while i>0 and j>0:
        if i==0:
            j = j - 1
        elif j==0:
            i = i - 1
        else:
            if costs[i-1, j] == min(costs[i-1, j-1], costs[i-1, j], costs[i, j-1]):
                i = i - 1
            elif costs[i, j-1] == min(costs[i-1, j-1], costs[i-1, j], costs[i, j-1]):
                j = j-1
            else:
                i = i - 1
                j= j- 1
        path.append([j, i])
    path.append([0,0])
    #for [y, x] in path:
        #cost = cost +distances[x, y]
    return path

if __name__ == '__main__':

    x = array([0, 1, 1, 2, 4, 4, 3, 1, 2, 0])
    y = array([0, 0, 2, 3, 3, 2, 2, 3, 2, 0])

    #data = wfdb.rdsamp('100',sampfrom=0, sampto=2000)[0]
    #two_ch_list = list(data)
    #x = [t[0] for t in two_ch_list]
    #y = [t[1] for t in two_ch_list]
    
    print('-- x --')
    print(x)
    print()
    print('-- y --')
    print(y)
    print()

    # calc path and distance    
    path, distance = dtw(x, y)
    
    if DEBUG:
        print('--- path ---')
        x_s, y_s = path
        for x_val, y_val in zip(x_s, y_s):
            print(x_val, y_val)
        print()

    # path plot
    from matplotlib import pyplot as plt
    # plt.imshow(cost.T, origin='lower', cmap=plt.cm.Reds, interpolation='nearest')
    plt.plot(path[0], path[1])
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axis('tight')
    plt.xticks(range(len(x)), x)
    plt.yticks(range(len(y)), y)
    plt.title('DTW Distance: {}'.format(distance))
    #plt.grid(True)
    plt.show()

    # plot x
    plt.clf()
    x_values = range(len(x))
    plt.plot(x_values, x)   
    plt.show()

    # plot y
    plt.clf()
    x_values = range(len(y))
    plt.plot(x_values, y)    
    plt.show()

    # plot both
    x_values = range(len(x))
    plt.plot(x_values, x)    

    x_values = range(len(y))
    plt.plot(x_values, y)    

    plt.show()

    # plot both with lines between points
    costs, distances = calc_costs(x, y)

    plt.clf()
    plt.plot(x, 'bo-' ,label='x')
    plt.plot(y, 'o-', label = 'y')
    plt.legend();
    paths = path_cost(x, y, costs, distances)
    for [map_x, map_y] in paths:
        #print (map_x, map_y)
        plt.plot([map_x, map_y], [x[map_x], y[map_y]], 'r')
    plt.show()