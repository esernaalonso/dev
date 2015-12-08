#######################################
# imports

#######################################
# functionality

def isSublist(a, b):
    if a == []: return True
    if b == []: return False
    return b[:len(a)] == a or isSublist(a, b[1:])

#######################################
# execution

if __name__ == "__main__":
	pass