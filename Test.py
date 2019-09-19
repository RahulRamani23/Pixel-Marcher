import unittest
from Marcher import findPath, all_colour_speed
from Map import Map

#####################################################################
#                                                                   #
#   There will be other test cases when your code is graded.        #
#   Feel free to modify the test cases here, this file will         #
#   not be submitted. These are just for reference.                 #
#                                                                   #
#   All timings are on BV473 machines with no one else logged in,   #
#   averaged across several runs. (Mathlab tends to be slower)      #
#                                                                   #
#   You can check how many users are logged in using the command    #
#   'uptime' on the machine. (People might SSH-ing in)              #
#                                                                   #
#   All tests can be run as follows:                                #
#      python3 Test.py                                              #
#                                                                   #
#   Individial tests can be run as follows:                         #
#      python3 Test.py Test.test_Gradient_One        (etc)          #
#                                                                   #
#####################################################################


# Speed function(1)
# The speed at the pixel b is dependent on the amount of
# white it has.
def white_speed(mp, p):
    pb = mp.pixels[p]
    dst = (pb[0])**2 + (pb[1])**2 + (pb[2])**2
    return ((dst/100.0) ** 0.5) + 0.01

# Speed function(2)
# The speed at the pixel is dependent on the hue of the pixel
def hue_speed(mp, p):
    r,g,b = mp.pixels[p]
    r,g,b = r/255,g/255,b/255
    mi,ma = min(r,g,b), max(r,g,b)
    if mi == ma:
        return 1
    elif ma == r:
        hue = (g-b)/(ma-mi)
    elif ma == g:
        hue = 2 + (b-r)/(ma-mi)
    else:
        hue = 4 + (r-g)/(ma-mi)
    hue *= 60
    hue += (360 if hue < 0 else 0)
    return hue + 1  # +1 to avoud errors with 0


"""
Make sure that you test *yourself* that the path is stored correctly in the Map
object. This will be tested when you hand it in. Don't miss the start and end
pixels in the path - you will lose marks if you do.
"""

class TestMarcher(unittest.TestCase):

    # Time on my solution ~0.26s
    def test_One(self):
        inp = Map("images/water.ppm")
        cost = findPath(inp, hue_speed)
        inp.outputPath()
        self.assertAlmostEqual(cost, 1.601784327, 5)

    # Time on my solution ~0.27s
    def test_Two(self):
        inp = Map("images/spiral.ppm")
        cost = findPath(inp, hue_speed)
        inp.outputPath()
        self.assertAlmostEqual(cost, 14.49090829, 5)

    # If we have black and white mazes, using weight function (2)
    #   makes sure that the Pixel Marcher always tries to walk along
    #   the white paths and solves the maze!

    # Time on my solution ~0.24s
    def test_Maze(self):
        inp = Map("images/maze.ppm")
        cost = findPath(inp, white_speed)
        inp.outputPath()
        self.assertAlmostEqual(cost, 28.09135288, 5)

    # Time on my solution ~0.87s
    def test_Maze_Big(self):
        inp = Map("images/bigmaze.ppm")
        cost = findPath(inp, white_speed)
        inp.outputPath()
        self.assertAlmostEqual(cost, 19.53492146, 5)

    # The following two test cases use the same image. You might
    # want to run them separately when debugging because they will
    # will over write the (already existing) output file.

    # Time on my solution ~0.06s
    def test_Gradient_One(self):
        inp = Map("images/grad.ppm")
        cost = findPath(inp, hue_speed)
        inp.outputPath()
        self.assertAlmostEqual(cost, 2.5939828, 5)

    # Time on my solution ~0.07s
    def test_Gradient_Two(self):
        inp = Map("images/grad.ppm")
        cost = findPath(inp, white_speed)
        inp.outputPath()
        self.assertAlmostEqual(cost, 5.8539818, 5)

    # This is just to help you run the function from Part (ii)
    #   The autotester will actually be checking the path to make
    #   sure that all the conditions given are satisfied, but here
    #   it is going to be your job to do so.

    def test_25_Colours(self):
        inp = Map("images/25colours.ppm")

        # Currently being run with your solution... But this
        #   will be replaced with a call to mine.
        findPath(inp, all_colour_speed)

        # Outputs both the path and gradient along it.
        # Uncomment these out if you want to use them

        inp.outputPath()
        # inp.outputGradient()


if __name__ == "__main__":
    unittest.main()
