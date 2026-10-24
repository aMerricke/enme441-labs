# ENME 441 - Lab 2: Functions, Generators, and List Comprehension - Merrick Summers
#
# Fill in the functions below, following the assignment handout.  Each def
# line still needs its arguments -- work out from the handout what they are,
# what order they go in, and which of them have default values.  Do not change
# the function names, and submit this file without renaming it.


from copy import deepcopy


# Problem 1:
def between(x, a = 0, b = 0.3):
    """Return True if the value lies within the range, False if it does not."""
    return a <= x <= b


# Problem 2:
def rangef(max, step):
    """Yield successive values from 0 up to the maximum."""
    val = 0
    while val <= max:
        yield val
        val += step


# Problem 3:
def mirror(lst):
    """Return a new list; the list passed in must not be modified."""
    copied = deepcopy(lst)
    return copied + copied[::-1]


# Problem 4:
def sort_outside(lst, a, b):
    """Return a new list with the same elements reordered."""
    return sorted(lst, key=lambda x: not between(x, a, b))


# Problem 5:
def div_2_or_3():
    """Return the list described in the handout (one line of code)."""
    return [x for x in range(17) if x%2 == 0 or x%3 == 0]


# The code below runs only when this file is executed directly (for example,
# by pressing "Run" in Thonny).  It does not run when the autograder imports
# your functions.  Leave it as-is.
if __name__ == '__main__':

    for i in rangef(5, 0.5):
        print(i, end=' ')
    print()

    alist = list(rangef(1, 0.25))
    print(alist)
    print(mirror(alist))
    print(sort_outside(mirror(alist), 0, 0.3))

    print(div_2_or_3())
