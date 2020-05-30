from urllib.parse import urlencode
from urllib.request import Request, urlopen
import re


def escape(string):
    string = re.sub('\r|\n|\t', '', string)
    xml_escaped = {'&nbsp;': ' ', '&gt;': '>', '&lt;': '<', '&amp;': '&'}
    for key, value in xml_escaped.items():
        string = re.sub(key, value, string)
    return string


def get_endereco(consulta):
    url = 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm'
    fields = {'relaxation': consulta, 'tipoCEP': 'ALL', 'semelhante': 'N'}

    request = Request(url, urlencode(fields).encode())
    result = urlopen(request).read()
    result = result.decode('iso-8859-1')

    result = escape(result)

    lista = []

    if 'DADOS NAO ENCONTRADOS' in result:
        lista.append('DADOS NAO ENCONTRADOS')
    else:
        result = re.search('CEP:</th></tr><tr>(.*?)</tr></table>', result).group(1)
        result = re.sub('<td(.*?)>', '', result)
        result = re.split('</tr><tr bgcolor="#C4DEE9">|</tr><tr>', result)
        for x in result:
            y = re.split('</td>', x)
            aux = dict()
            aux['logradouro'] = y[0].strip()
            aux['bairro'] = y[1].strip()
            aux['cidade'] = y[2].strip()
            aux['cep'] = y[3]
            lista.append(aux)
    return lista
