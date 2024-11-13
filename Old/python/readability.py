from cs50 import get_string
import string

blurb = get_string("Text: ").lower()
punct = 0
spc = 0
ltr = 0


for i in range(len(blurb)):
    if blurb[i] in ".!?":
        punct += 1
    elif blurb[i].isspace():
        spc += 1
    elif blurb[i].isalpha():
        ltr += 1


l = ltr * (100.0 / (spc + 1))
s = punct * (100.0 / (spc + 1))
index = 0.0588 * l - 0.296 * s - 15.8
grade = round(index)

if grade < 1:
    print("Before Grade 1")
elif grade >= 16:
    print("Grade 16+")
else:
    print(f"Grade {grade}")
