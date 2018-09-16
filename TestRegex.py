import re

line =  " RONEY (CROSSTALK)"
print(re.sub(r'\(\w+\)','',line))