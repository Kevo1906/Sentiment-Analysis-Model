host = "https://www.lostiempos.com/actualidad"
link = "/actualidad/mundo/20210909/eeuu-dice-adios-grandes-intervenciones-militares-aniversario-del-11s"

if host.split("/")[-1] == link.split("/")[1]:
    link= link.split("/")
    link.pop(0)
    link.pop(0)
    fix_link = ""
    for l in link:
        fix_link+= "/" + l

    print(fix_link)