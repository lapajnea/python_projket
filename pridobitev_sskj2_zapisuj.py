import re
import http.client

stran = http.client.HTTPSConnection('fran.si')


def poenostavi(beseda):
    """Funckija poenostavi besedo tako da znake z akcenti zamenja za splošne znake. Šumnike pusti pri miru. tudi vse
     znake da v majhne. """
    beseda = beseda.lower()
    for znak in beseda:
        if znak in ['à', 'á', 'â']:
            beseda = beseda.replace(znak, 'a')
        if znak in ['è', 'é', 'ê']:
            beseda = beseda.replace(znak, 'e')
        if znak in ['ì', 'í', 'î']:
            beseda = beseda.replace(znak, 'i')
        if znak in ['ò', 'ó', 'ô']:
            beseda = beseda.replace(znak, 'o')
        if znak in ['ù', 'ú', 'û']:
            beseda = beseda.replace(znak, 'u')
        if znak == 'ŕ':
            beseda = beseda.replace(znak, 'r')
        if znak == 'ñ':
            beseda = beseda.replace(znak, 'nj')
    return beseda


ind = 4001

with open('besede_iz_sskj2.txt', 'a') as pisi:
    while ind <= 4884:
        print('stran:', ind)
        stran.request('GET', '/iskanje?page={0}&FilteredDictionaryIds=133&View=1&Query=%2A'.format(ind))
        text = stran.getresponse().read().decode()
        for beseda in re.findall(r'<a href="/133/sskj2-slovar-slovenskega-knjiznega-jezika-2/\d+/[a-z]{3,}\?page=\d+&amp;FilteredDictionaryIds=133&amp;View=1&amp;Query=\*">[^<]+</a>',text):
            beseda = re.split(r'">', beseda)[1]
            beseda = beseda[:-4]  # odstranim znake na koncu <\a>
            # odstranim besede, ki so prvi del zloženk (oblike: 'beseda' + '...')
            if '.' in beseda:
                continue
            beseda = poenostavi(beseda)  # olepšam besedo
            pisi.write(beseda + '\n')
        ind += 1




