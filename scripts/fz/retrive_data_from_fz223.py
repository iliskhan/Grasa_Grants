import os
import json

import xml.etree.ElementTree as ET

def retrieve(file_path):

    ns = {'xmlns':'http://zakupki.gov.ru/223fz/types/1',
          'ns2':'http://zakupki.gov.ru/223fz/purchase/1'}

    data = dict()

    xmlData223 = ET.parse(file_path)

    root = xmlData223.getroot()

    name = file_path.split('_')[1].split('/')[1]

    item = root.find('ns2:body/'
                     'ns2:item', ns)

    if name == 'purchaseNotice':
        purchaseNotice = item.find('ns2:purchaseNoticeData', ns)
    if name == 'purchaseNoticeAE':
        purchaseNotice = item.find('ns2:purchaseNoticeAEData', ns)
    if name == 'purchaseNoticeOA':
        purchaseNotice = item.find('ns2:purchaseNoticeOAData', ns)
    if name == 'purchaseNoticeOK':
        purchaseNotice = item.find('ns2:purchaseNoticeOKData', ns)
    if name == 'purchaseNoticeZK':
        purchaseNotice = item.find('ns2:purchaseNoticeZKData', ns)
    if name == 'purchaseNoticeAESMBO':
        purchaseNotice = item.find('ns2:purchaseNoticeAESMBOData', ns)
    if name == 'purchaseNoticeZKESMBO':
        purchaseNotice = item.find('ns2:purchaseNoticeZKESMBOData', ns)
    if name == 'purchaseNoticeKESMBO':
        purchaseNotice = item.find('ns2:purchaseNoticeKESMBOData', ns)
    if name == 'purchaseNoticeZPESMBO':
        purchaseNotice = item.find('ns2:purchaseNoticeZPESMBOData', ns)


    data['registrationNumber'] = purchaseNotice.find('ns2:registrationNumber', ns).text

    data['createDateTime'] = purchaseNotice.find('ns2:createDateTime', ns).text

    data['urlEIS'] = purchaseNotice.findtext('ns2:urlEIS', namespaces = ns)
    data['urlVSRZ'] = purchaseNotice.findtext('ns2:urlVSRZ', namespaces = ns)

    data['name'] = purchaseNotice.find('ns2:name', ns).text

    data['fullName'] = purchaseNotice.find('ns2:customer/'
                                         'xmlns:mainInfo/'
                                         'xmlns:fullName', ns).text

    data['shortName'] = purchaseNotice.find('ns2:customer/'
                                         'xmlns:mainInfo/'
                                         'xmlns:shortName', ns).text

    data['legalAddress'] = purchaseNotice.find('ns2:customer/'
                                         'xmlns:mainInfo/'
                                         'xmlns:legalAddress', ns).text

    data['purchaseCodeName'] = purchaseNotice.find('ns2:purchaseCodeName', ns).text

    data['place'] = purchaseNotice.findtext('ns2:documentationDelivery/'
                                            'xmlns:place', namespaces=ns)

    lot = purchaseNotice.find('ns2:lots/'
                              'xmlns:lot/'
                              'xmlns:lotData', ns)
    data['currency'] = lot.find('xmlns:currency/'
                                'xmlns:code', ns).text

    data['initialSum'] = lot.find('xmlns:initialSum', ns).text

    data['submisionStartDate'] = purchaseNotice.findtext('ns2:applSubmisionStartDate', namespaces=ns)

    data['submissionCloseDateTime'] = purchaseNotice.findtext('ns2:submissionCloseDateTime', namespaces=ns)

    return data


def main():
    path = '../../data/223/all_files/'

    path_AE223 = '../../data/223/data_AE223/'
    path_fz223 = '../../data/223/data_fz223/'
    path_OA223 = '../../data/223/data_OA223/'
    path_OK223 = '../../data/223/data_OK223/'
    path_ZK223 = '../../data/223/data_ZK223/'
    path_AESMBO223 = '../../data/223/data_AESMBO223/'
    path_ZPESMBO223 = '../../data/223/data_ZPESMBO223/'
    path_KESMBO223 = '../../data/223/data_KESMBO223/'
    path_ZKESMBO223 = '../../data/223/data_ZKESMBO223/'

    data_AE223 = []
    data_fz223 = []
    data_OA223 = []
    data_OK223 = []
    data_ZK223 = []
    data_AESMBO223 = []
    data_ZPESMBO223 = []
    data_KESMBO223 = []
    data_ZKESMBO223 = []

    for i in os.listdir(path):

        file_path = os.path.join(path, i)

        if i.endswith('.xml') and i.startswith('purchaseNotice_'):
            data_fz223.append(retrieve(file_path))

        if i.endswith('.xml') and i.startswith('purchaseNoticeAE'):
            data_AE223.append(retrieve(file_path))

        if i.endswith('.xml') and i.startswith('purchaseNoticeOA'):
            data_OA223.append(retrieve(file_path))

        if i.endswith('.xml') and i.startswith('purchaseNoticeOK'):
            data_OK223.append(retrieve(file_path))

        if i.endswith('.xml') and i.startswith('purchaseNoticeZK'):
            data_ZK223.append(retrieve(file_path))

        if i.endswith('.xml') and i.startswith('purchaseNoticeAESMBO'):
            data_AESMBO223.append(retrieve(file_path))

        if i.endswith('.xml') and i.startswith('purchaseNoticeZKESMBO'):
            data_ZKESMBO223.append(retrieve(file_path))

        if i.endswith('.xml') and i.startswith('purchaseNoticeKESMBO'):
            data_KESMBO223.append(retrieve(file_path))

        if i.endswith('.xml') and i.startswith('purchaseNoticeZPESMBO'):
            data_ZPESMBO223.append(retrieve(file_path))


        if i != '.gitkeep':
            os.remove(file_path)


    with open(f'{path_fz223}/info_fz223.json', 'w', encoding='utf8') as f:
        json.dump(data_fz223, f, ensure_ascii=False, indent=4)
    with open(f'{path_AE223}/info_AE223.json', 'w', encoding='utf8') as f:
        json.dump(data_AE223, f, ensure_ascii=False, indent=4)
    with open(f'{path_OA223}/info_OA223.json', 'w', encoding='utf8') as f:
        json.dump(data_OA223, f, ensure_ascii=False, indent=4)
    with open(f'{path_OK223}/info_OK223.json', 'w', encoding='utf8') as f:
        json.dump(data_OK223, f, ensure_ascii=False, indent=4)
    with open(f'{path_ZK223}/info_ZK223.json', 'w', encoding='utf8') as f:
        json.dump(data_ZK223, f, ensure_ascii=False, indent=4)
    with open(f'{path_AESMBO223}/info_AESMBO223.json', 'w', encoding='utf8') as f:
        json.dump(data_AESMBO223, f, ensure_ascii=False, indent=4)
    with open(f'{path_ZPESMBO223}/info_ZPESMBO223.json', 'w', encoding='utf8') as f:
        json.dump(data_ZPESMBO223, f, ensure_ascii=False, indent=4)
    with open(f'{path_KESMBO223}/info_KESMBO223.json', 'w', encoding='utf8') as f:
        json.dump(data_KESMBO223, f, ensure_ascii=False, indent=4)
    with open(f'{path_ZKESMBO223}/info_ZKESMBO223.json', 'w', encoding='utf8') as f:
        json.dump(data_ZKESMBO223, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
