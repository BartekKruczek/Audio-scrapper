# simple usage
# import time
# import throttle


# # limit to 3 calls
# # allow more every 1 second
# @throttle.wrap(1, 3)
# def aesthetic(*values):
#     return " ".join(values).upper()


# for index in range(10):
#     result = aesthetic("beautiful")

#     success = not result is throttle.fail

#     print(index, success)

#     time.sleep(0.23)

# complex usage
import time
import random
import throttle

# allow more every 1 second
delay = 1

# limit to 3 calls
limit = 3

# only check values less than 5 against the limit
key = lambda value: value < 5

# or Static()
valve = throttle.Valve()

# make some quick calls
for index in range(30):
    item = random.randrange(0, 8)

    allow = valve.check(delay, limit, item, key=key)

    print(item, allow)

    time.sleep(0.23)
