test = {"a" : 3}
try:
    c = test["a"]
    print(c)
except:
    print("nope")
finally:
    print("yeah")