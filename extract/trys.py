# import re
# host = "https://www.la-razon.com/mundo/"
# link = "https://www.la-razon.com/mundo/2021/09/09/diaz-canel-recibe-a-morales-en-la-habana/"
# print(host.split("/")[-1])
# print(link.split("/")[1])
# is_well_formed_link = re.compile(r'^https?://.+/.+$')
# if not is_well_formed_link.match(link):
#     if host.split("/")[-1] == link.split("/")[1]:
#         link= link.split("/")
#         link.pop(0)
#         link.pop(0)
#         fix_link = ""
#         for l in link:
#             fix_link+= "/" + l

#         print(fix_link)
x = "soy una lista"
if type(x) is list:
    print("hola")
else:
    print("hi")
