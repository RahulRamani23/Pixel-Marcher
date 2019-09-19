#################################################################
#                                                               #
#    Define any helper functions you need in this file only.    #
#                                                               #
#    You *cannot* include any additional libraries. If you      #
#    need something that Python doesn't have natively,          #
#    implement it.                                              #
#                                                               #
#    Make sure you take a look at Map.py to get familiar        #
#    with how the image is loaded in and stored, you will       #
#    need this to implement your solution properly.             #
#                                                               #
#    A few test cases are provided in Test.py. You can test     #
#    your code by running                                       #
#               python3 Test.py                                 #
#    in the directory where the files are located.              #
#                                                               #
#################################################################


class Heap():
    ''' binary tree implementation of a min heap using list representation
    '''

    def __init__(self, weight, key):
        '''
        construct a heap using key with weight as the root
        '''
        # list representation of a heap
        self._heap = []
        self._heap.append((weight, key))
        # stores dictionary of keys to their location on the heap
        self.key = {}
        self.key[key] = 0

    def insert(self, weight, key):
        '''(Heap, obj, obj) -> NoneType
        insert the given key at right place in the heap'''
        self._heap.append((weight, key))
        self.key[key] = len(self._heap) - 1
        self.bubbleUp(len(self._heap) - 1)

    def decreaseWeight(self, key, weight):
        '''
        decrease the weight of key
        '''
        index = self.key[key]
        self._heap[index][0] = weight
        self.bubbleUp(index)

    def bubbleUp(self, index):
        '''
        Restores heap order starting from index
        '''
        # find the last node index
        # find the parent (always  (last_node - 1//2) because it rounded down)
        parent = int((index - 1) // 2)
        # continue swapping until last node in right place or you get to the root
        curr_key = self._heap[index][1]
        while (index > 0 and self._heap[parent][0] > self._heap[index][0]):
            parent_key = self._heap[parent][1]
            (self._heap[parent], self._heap[index]) = (
                self._heap[index], self._heap[parent])
            self.key[curr_key], self.key[parent_key] = parent, index
            # update index and parent
            index = parent
            parent = int((index - 1) // 2)

    def extract_min(self):
        '''
        removes the min weight key and returns it
        '''
        min_key = None
        # raise an exception if heap is empty
        if (len(self._heap) > 0):
            # get min key
            min_key = self._heap[0]
            # remove the last node
            last_node = self._heap.pop(len(self._heap) - 1)
            self.key.pop(last_node[1])
            # step2: replace the root with last node if at least there is one item in the heap
            if(len(self._heap) != 0):
                # replace root with the last node
                self._heap[0] = last_node
                #self._heap2[0] = l_node2
                self.key[last_node[1]] = 0
                # step 3, 4: last node will be updated automatically, so restore the heap_order
                self.bubbleDown()
            # return the highest priority item
        return (min_key)

    def bubbleDown(self):
        '''
        restore the heap order starting from the root
        '''
        # start from the root
        index = 0
        curr_key = self._heap[index][1]
        # continue going down while heap order is violated
        child_index = self.findViolation(index)
        while (child_index is not None):
            # get the childs key
            child_key = self._heap[child_index][1]
            # swap index and child
            (self._heap[index],
             self._heap[child_index]) = (self._heap[child_index],
                                         self._heap[index])
            (self.key[curr_key], self.key[child_key]) = (child_index, index)
            # update index to point to child_index
            index = child_index
            # find next violator
            child_index = self.findViolation(index)

    def getWeight(self, key):
        '''
        returns the weight of the key
        '''
        return self._heap[self.key[key]][0]

    def findViolation(self, index):
        '''
        returns the location of a violating child of key at index if there is
        a violation
        '''
        # left and right child of index
        left = index * 2 + 1
        right = index * 2 + 2
        returned_index = None
        if (left >= len(self._heap)):
            returned_index = None
        # if it has one child, left child may violate
        elif (right >= len(self._heap)):
            if (self._heap[left][0] < self._heap[index][0]):
                returned_index = left
        # otherwise, we find which child has the smallest weight and compare
        # it against the parent
        elif (self._heap[left][0] < self._heap[index][0]
              and self._heap[left][0] <= self._heap[right][0]):
            returned_index = left
        elif (self._heap[right][0] < self._heap[index][0] and
              self._heap[right][0] <= self._heap[left][0]):
            returned_index = right
        # return the found index
        return returned_index

    def getSize(self):
        return len(self._heap)


def withinPicture(mp, coord):
    if (0 <= coord[0] <= mp.sx - 1 and 0 <= coord[1] <= mp.sy - 1):
        return True
    else:
        return False


def findPath(mp, speed):
    """
        ---------- Input ---------
        (1) mp    : This is a Map object representing the image you are working on. Look at the Map
                    class to see details on how we are representing the data.

        (2) speed : This is the speed **function**. You are supposed to use this to find the speed on
                    each pixel walked on by the Pixel Marcher. 
                    
                    ** The speed is going to be in units/second, where each pixel is exactly one unit 
                    in size. We will keep this simple and assume that the Pixel Marcher cannot walk
                    in diagonals, and always covers exactly 1 unit when marching over a pixel. **

                    This function should be called like this:

                            speed(mp, (x,y))

                    to find the speed at which the Pixel Marcher can go over pixel (x,y). In general 
                    it returns a floating point value, and will always be greater than 0.

        ---------- Requirements ---------
        Your objective is to find the fastest path from pixel (0,0) to pixel (sx-1, sy-1), along
        with the the time required to traverse this path in seconds. Here, sx and sy are the x and y 
        dimensions of the image. (These are stored in 'mp')

        From each pixel, it is possible to step to at most 4 other pixels, namely the ones on it's top, 
        right, bottom and left. All of these pixels may have different speeds, and you have to use the 
        given speed function to compute these.

        Note: When going through your neighbours, always go through them in the following order for the 
            sake of this assignment: TOP, RIGHT, BOTTOM, LEFT (Start at the top and go clockwise).


                                                    (x, y-1)
                                                        ^
                                                        |
                                    (x-1, y) <------ (x, y) ------> (x+1, y)
                                                        |
                                                        v
                                                    (x, y+1)


        Always doing it in this order will ensure consistency if there are multiple fastest paths. (It's OK
        if your path is still different, as long as it is correct and still optimal)

        Once you find this path, you need to store all the nodes along it in mp.path[], ensuring that 
        the (0,0) is the first element in the array, (sx-1, sy-1) is the last, and all the remaining
        elements are in order.

        Your function additionally needs to return the time required to traverse the fastest path *in
        seconds*. You will be graded on this since this time for the path is unique and must match the 
        expected answer.

        You are NOT allowed to import any additional libraries. All code must be your own.      
        """

    # initialize heap
    heap = Heap(1 / speed(mp, (0, 0)), (0, 0))
    # set of the pixels that we have assigned a speed to
    pixel_set = {(0, 0)}
    precededBy = dict()  # will keep the fastest path back to (0,0)
    visited = {(0, 0)}  # set of pixels that we traversed to

    # used to visit around the pixel
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]

    while (heap.getSize() > 0):
        curr_speed, curr_coord = heap.extract_min()
        if(curr_coord == (mp.sx - 1, mp.sy - 1)):
            break  # already calculated speed, can just add it to mp.path
        visited.add(curr_coord)  # we are visiting this coordinate
        for i in range(4):  # loop around the current pixel
            # coordinates to a pixel adjacent to curr_coord
            coord = (curr_coord[0] + dx[i], curr_coord[1] + dy[i])
            # if we have not visited it and it is within the picture
            if (coord not in visited and withinPicture(mp, coord)):
                # calculate speed
                total_speed = 1 / speed(mp, coord) + curr_speed
                # coord wasn't assigned a speed, assign it and add to heap
                if(coord not in pixel_set):
                    heap.insert(total_speed, coord)
                    precededBy[coord] = (curr_coord, total_speed)
                    pixel_set.add(coord)
                # coord was once assigned a speed, decrease it if the new speed
                # is faster than the previous speed
                elif(total_speed < heap.getWeight(coord)):
                    heap.decreaseWeight(coord, total_speed)
                    precededBy[coord] = (curr_coord, total_speed)
    # last pixel has to be part of the path
    mp.path.append((mp.sx - 1, mp.sy - 1))
    # get the preceding pixel
    p = precededBy[(mp.sx - 1, mp.sy - 1)]
    totalSpeed = p[1]
    # insert all the pixels back up to (0,0)
    while (p[0] != (0, 0)):
        mp.path.insert(0, p[0])
        p = precededBy[p[0]]
    mp.path.insert(0, (0, 0))
    return totalSpeed


def all_colour_speed(mp, p):
    """
    ---------- Input ---------
    mp : A Map object that represents the image
    p  : A tuple containing the (x,y) coordinates for pixel you want to
            return the speed for.


    ---------- Requirements ---------
    Define your own speed function here so that when "25colours.ppm" is run with this function, 
    the fastest path in the image satisfies the following constraints:

        (1) The fastest path must visit every one of the 25 colours in the graph. The order 
            in which the path visits these colours does *not* matter, as long as it visits them all. 
            Be careful - missing even one colour will result in 0 for this function.

        (2) The path can stay on one colour for as many steps as necessary, however once the path 
            leaves a colour, it can NEVER go through another pixel of the same colour again.
            (Said in another way, it can only enter/exit each coloured box once)

        (3) The speed for every pixel *must* be greater than 0.

    There is no restriction on path length, it can be as long or as short as needed - as long as it 
    satisfies the conditions above. 

    Important Note: This speed function will NOT be tested with your solution to the first part of the
                    question. This will be passed into my code and should still produce the results as above,
                    so do not try to change your findPath() method to help with this.

                    This function will be tested ONLY on the specified image, so you do not have to worry
                    about generalizing it. Just make sure that it does not depend on anything else in your
                    code other than the arguments passed in.


    How to test:    Use the 'outputGradient' and 'outputPath' methods in Map to help you debug. Displaying
                    the path will be useful to start, as it will give you a general idea of what the fastest 
                    path looks like, but you will also want to display the gradient to make sure that 
                    there are no colours repeated! (This should be obvious visually if it is the case)

    """
    (x, y) = p
    speed = 0.2

    width = mp.sx // 5  # this gives us the width of the box
    box_center_x = width // 2  # this gives the middle x pixel of the first box

    height = mp.sy // 5  # this gives us the height of the box
    box_center_y = height // 2  # this gives the middle y line of the first box

    y_lines = set()
    # box_center_y provides a line down the middle of the first row of boxes
    # we can add the height of the boxes to define other mid lines
    for i in range(0, 5):
        y_lines.add((i * height) + box_center_y)

    # this will bring us to the middle of the first box
    if((y in range(0, box_center_y) and x == 0)  # move down
       or (x in range(0, box_center_x) and y == box_center_y)):  # move right
        speed = 100
    elif (y in y_lines  # we reside on the mid y line of any box
          and (x in range(box_center_x, box_center_x + 4 * width))):
        # we must travel down the y line until we hit the x line of
        # the rightmost box or leftmost box
        speed = 100
    elif(x == box_center_x):  # on the x middle of a leftmost box
        # travel to the x line of the box
        if(y in range(height + box_center_y, 2 * height + box_center_y)
           or y in range(3 * height + box_center_y, 4 * height + box_center_y)):
            speed = 100

    elif(x == 4 * width + box_center_x):  # on the y middle of a bottom box
        # travel to the x line of that box
        if(y in range(box_center_y, height + box_center_y)
           or y in range(2 * height + box_center_y, 3 * height + box_center_y)):
            speed = 100

    return speed      # Return the speed for pixel `p` here


