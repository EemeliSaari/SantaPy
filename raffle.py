import random


def shuffle_names(*args, index=0):

    names = [a[index] for a in args]

    random.shuffle(names)

    return names


def map_names(*args):

    return [(a, args[(i + 1) % len(args)]) for i, a in enumerate(args)]
