from dct2.test_dct import *


def main():
    test_dct_correctness()
    sizes, times_custom, times_scipy = test_timing()
    plot_timings(sizes, times_custom, times_scipy)

if __name__ == "__main__":
    main()