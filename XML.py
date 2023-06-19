from bs4 import BeautifulSoup as Soup
from bs4.builder import XMLParsedAsHTMLWarning
import warnings

warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)


def typeTodigit(str):
    if str == 'whole':
        return '1'
    if str == 'half':
        return '2'
    if str == 'quarter':
        return '4'
    if str == 'eighth':
        return '8'
    if str == '16th':
        return '16'
    if str == '32nd':
        return '32'
    if str == '64th':
        return '64'

def process_xml(xml_file):
    with open(xml_file, 'r',encoding='utf-8') as xml:
        soup = Soup(xml.read(), 'lxml')
    measures = soup.findAll('measure')
    result = ""
    for measure in measures:
            notes = measure.findAll('note')
            for note in notes:
                step = note.find('step')
                if step is not None:
                    result += step.text
                else:
                    result += 'p'
                alter = note.find('alter')
                alt = ""

                if alter is not None:
                    if alter.text == '-1':
                        alt = '*'
                    if alter.text == '1':
                        alt = '#'

                type = note.find('type')
                if type is not None:
                    result += alt
                    result += typeTodigit(type.text)

                dot = note.find('dot')
                if dot is not None:
                    result += '.'
            result += ' '
    return result

