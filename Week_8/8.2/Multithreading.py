import threading

def range_sum(result, index, numFrom, numTo):
    """ Find the sum between two ranges and place the result into the
        passed result array at the passed index

    Args:
        result (List): A list of numbers
        index (Int): Where in the array to place the sum
        numFrom (Int): From what number to start counting
        numTo (Int): To what number to include and stop counting at
    """
    numbers = []
    for i in range(numFrom, numTo):
        numbers.append(i)
        
    result[index] = sum(numbers)

    
def main(ranges):
    """Takes several ranges of numbers in a list and finds the sum total of all the sums of those ranges.

    Args:
        ranges (List): A list of ranges that are also in a list format. Example: [ [5, 12] , [22, 35] ]
    """
    
    numberOfRanges = len(ranges)

    allThreads = [None] * numberOfRanges
    result = [0] * numberOfRanges

    for index in range(numberOfRanges):
        # Get the numbers to start and end on from the range array
        numFrom = ranges[index][0]
        numTo = ranges[index][1] + 1
        
        # Create and start the threads
        aThread = threading.Thread(target=range_sum, args=(result, index, numFrom, numTo))
        aThread.start()
        allThreads[index] = aThread

    # Join the finished threads back into the main thread
    for aThread in allThreads:
        aThread.join()
    
    # Print the results
    print(result)
    print(sum(result))




# ========== Running Code =============

# Test 1
ranges = [
    [1,5],
    [20,22]
]
main(ranges)

# Test 2
ranges = [
    [10, 20],
    [1, 5],
    [70, 80],
    [27, 92],
    [0, 16]
]
main(ranges)