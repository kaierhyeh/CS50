MAX_HEIGHT = 8

while True:
    try:
        height = int(input("Height: "))
        if 1 <= height <= MAX_HEIGHT:
            break
    except ValueError:
        pass

for i in range(1, height + 1):
    print(" " * (height - i) + "#" * i + "  " + "#" * i)

# -------------------------------------------------
# Need "try" and "except" to handle non-numeric input,
# and then use "pass" to silently reprompt.


# Version 1
# for i in range(height):
# 	print(" " * (height - (i + 1)) + "#" * (i + 1) + "  " + "#" * (i + 1))


# Version 0
# for i in range(height):
# 	for j in range(height - (i + 1)):
# 		print(" ", end="")
# 	print("#" * (i + 1) + "  " + "#" * (i + 1), end="")
# 	for j in range(height - (i + 1)):
# 		print(" ", end="")
# 	print("")
