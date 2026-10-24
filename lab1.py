# ENME 441 - Lab 1: Python Loops - Merrick Summers
#
# Fill in the functions below, following the assignment handout.  Each def
# line still needs its arguments -- work out from the handout what they are
# and what order they go in.  Do not change the function names, and submit
# this file without renaming it.


def ln_taylor_terms(x: float, n: int) -> float:
    """Return the approximation of f(x) for a fixed number of terms."""
    result = 0
    for k in range(1, n + 1):
        result += (-1) ** (k - 1) * (x - 1) ** k / k
    return result


def ln_taylor_tol(x: float, tol: float) -> tuple[float, int]:
    """Return the approximation of f(x) and the number of terms used."""
    k = 0
    total = 0
    mag_last_term = float('inf')
    while mag_last_term >= tol:
        k += 1
        total += (-1) ** (k - 1) * (x - 1) ** k / k
        mag_last_term = abs((-1) ** (k - 1) * (x - 1) ** k / k)
    return total, k


# The code below runs only when this file is executed directly.  It does not run when the autograder imports
# your functions.  Leave it as-is.
if __name__ == '__main__':

    x = 0.5

    approx = ln_taylor_terms(x, 5)
    print(f'f({x}) ~= {approx:.9f} with 5 terms')

    approx, k = ln_taylor_tol(x, 1e-7)
    print(f'f({x}) ~= {approx:.9f} with {k} terms')
