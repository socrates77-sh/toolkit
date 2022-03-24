# history:
# 2021/05/19  v1.0  initial

import re
import os
import sys
from pprint import pprint

VERSION = '1.0'

out_file = 'a.txt'
auth_file = r'E:\py\toolkit\authz'
proj_name = [
    'A680',
    '6070MPW-1',
    'A010',
    'A020',
    'A030',
    'A040',
    'A070',
    'A080',
    'A100',
    'A110',
    'A120',
    'A130',
    'A140',
    'A150',
    'A160',
    'A160_TEG',
    'A180',
    'A190',
    'A210',
    'A220',
    'A230',
    'A230_TEG',
    'A240',
    'A250',
    'A260',
    'A270',
    'A280',
    'A282',
    'A290',
    'A300',
    'A310',
    'A320',
    'A330',
    'A340',
    'A350',
    'A360',
    'A370',
    'A380',
    'A390',
    'A400',
    'A410',
    'A420',
    'A470',
    'A480',
    'A490',
    'A500',
    'A530',
    'A540',
    'A550',
    'A590',
    'A600',
    'A610',
    'A620',
    'A630',
    'A640',
    'A650',
    'A660',
    'A670',
    'A700',
    'A710',
    'A720',
    'A720_TEG',
    'A721',
    'A730',
    'A740',
    'A750',
    'A760',
    'A770',
    'A780',
    'A789',
    'A790',
    'A800',
    'A802',
    'A810',
    'A820',
    'A830',
    'A840',
    'A850',
    'A860',
    'A870',
    'A880',
    'A890',
    'A900',
    'A910',
    'A920',
    'A930',
    'A940',
    'A950',
    'A960',
    'A980',
    'A990',
    'B010',
    'B030',
    'B040',
    'B050',
    'B060',
    'B070',
    'B080',
    'B090',
    'B100',
    'B110',
    'MC10C5114(MC10016)',
    'MC10P5010(MC10P01)',
    'MC10P5010B(MC10P01B)',
    'MC10P5011(MC10P02)',
    'MC10P5110(MC10P11)',
    'MC10P5110B(MC10P11B)',
    'MC10P5223(MC10P78)',
    'MC20P6010(MC20P01)',
    'MC20P6011(MC20P02)',
    'MC20P6011B(MC20P02B)',
    'MC20P6020(MC20P801)',
    'MC20P6112(MC20P04)',
    'MC20P7011(MC20P22)',
    'MC20P7012(MC20P24)',
    'MC20P7012B(MC20P24B)',
    'MC20P7113(MC20P38)',
    'MC20P8113(MC20P68)',
    'MC3090',
    'MC30P6030(MC30P011)',
    'MC30P6040(MC30P081)',
    'MC30P6060',
    'MC31P5120(MC31P11)',
    'MC31P5130',
    'MC32E22',
    'MC32P5213(MC33P78)',
    'MC32P5312(MC33P116 4K)',
    'MC32P5312',
    'MC32P5314(MC33P116)',
    'MC32P7010(MC32P21)',
    'MC32P7012',
    'MC32P7020(MC32P821)',
    'MC32P7022',
    'MC32P7030',
    'MC32P7212(MC33P94)',
    'MC32P7212',
    'MC32P7312',
    'MC32P7510',
    'MC32P8112(MC32P64)',
    'MC32T8122(MTP1)',
    'MC32T8132(MTP2)',
    'MC33PA4',
    'MC34P6050(MC34P01)',
    'MC51F8114',
    'MC51P88',
    'MC6060MPW',
    'MC6070MPW',
    'MC60F7414',
    'MC6933',
    'MC8002B',
    'MC8004(MC32P7510_NMOS)',
    'MC8005(MC9034_NMOS)',
    'MC8011',
    'MC8012',
    'MC8013',
    'MC8014',
    'MC8242',
    'MC9001B',
    'MC9003B',
    'MC9009',
    'MC9012B',
    'MC9012B0V',
    'MC9029',
    'MC9029蝻拍',
    'MC9031',
    'MC9035B',
    'MC9039',
    'MC9050',
    'MC9080',
    'MC9081',
    'MPW6060',
    'MPW6070',
    'MPW7022',
    'MTP',
    'MTP2']


def read_file(file_name):
    try:
        f = open(file_name, 'r', encoding='big5', errors='ignore')
        txt = f.read()
    except Exception as e:
        print(e)
        sys.exit(1)

    return txt


def find_proj_name(txt):
    # [RD_SVN:/ProjectData/B010/Spec]
    p = re.compile('\[RD_SVN:\/ProjectData\/(.*?)\/Spec]')
    ret = re.findall(p, txt)
    pprint(ret)


def project_auth(name):
    txt = ''
    txt += '\n[RD_SVN:/ProjectData/%s/Application]\n' % name
    txt += '@AE=rw\n'
    txt += '@ana=rw\n'
    txt += '@dig=rw\n'
    txt += '@eng=\n'
    txt += '@fae=r\n'
    txt += '@lay=rw\n'
    txt += '@pro=\n'
    txt += '@qua=\n'

    txt += '\n[RD_SVN:/ProjectData/%s/Basic_Data]\n' % name
    txt += '@AE=rw\n'
    txt += '@ana=rw\n'
    txt += '@dig=rw\n'
    txt += '@eng=rw\n'
    txt += '@fae=\n'
    txt += '@lay=rw\n'
    txt += '@pro=r\n'
    txt += '@qua=rw\n'

    txt += '\n[RD_SVN:/ProjectData/%s/Dig]\n' % name
    txt += '@AE=rw\n'
    txt += '@ana=rw\n'
    txt += '@dig=rw\n'
    txt += '@eng=\n'
    txt += '@fae=\n'
    txt += '@lay=rw\n'
    txt += '@pro=\n'
    txt += '@qua=\n'

    txt += '\n[RD_SVN:/ProjectData/%s/FAE]\n' % name
    txt += '@AE=rw\n'
    txt += '@ana=rw\n'
    txt += '@dig=rw\n'
    txt += '@eng=\n'
    txt += '@fae=rw\n'
    txt += '@lay=rw\n'
    txt += '@pro=\n'
    txt += '@qua=\n'

    txt += '\n[RD_SVN:/ProjectData/%s/Fail Analysis]\n' % name
    txt += '@AE=rw\n'
    txt += '@ana=rw\n'
    txt += '@dig=rw\n'
    txt += '@eng=\n'
    txt += '@fae=\n'
    txt += '@lay=rw\n'
    txt += '@pro=\n'
    txt += '@qua=\n'

    txt += '\n[RD_SVN:/ProjectData/%s/IP]\n' % name
    txt += '@AE=rw\n'
    txt += '@ana=rw\n'
    txt += '@dig=rw\n'
    txt += '@eng=\n'
    txt += '@fae=\n'
    txt += '@lay=rw\n'
    txt += '@pro=\n'
    txt += '@qua=\n'

    txt += '\n[RD_SVN:/ProjectData/%s/Layout]\n' % name
    txt += '@AE=rw\n'
    txt += '@ana=rw\n'
    txt += '@dig=rw\n'
    txt += '@eng=\n'
    txt += '@fae=\n'
    txt += '@lay=rw\n'
    txt += '@pro=\n'
    txt += '@qua=\n'

    txt += '\n[RD_SVN:/ProjectData/%s/Project_Management]\n' % name
    txt += '@AE=\n'
    txt += '@ana=\n'
    txt += '@dig=\n'
    txt += '@eng=\n'
    txt += '@fae=\n'
    txt += '@lay=\n'
    txt += '@pro=\n'
    txt += '@qua=\n'

    txt += '\n[RD_SVN:/ProjectData/%s/R0释放]\n' % name
    txt += '@AE=rw\n'
    txt += '@ana=rw\n'
    txt += '@dig=rw\n'
    txt += '@eng=rw\n'
    txt += '@fae=\n'
    txt += '@lay=rw\n'
    txt += '@pro=\n'
    txt += '@qua=rw\n'

    txt += '\n[RD_SVN:/ProjectData/%s/Review]\n' % name
    txt += '@AE=rw\n'
    txt += '@ana=rw\n'
    txt += '@dig=rw\n'
    txt += '@eng=rw\n'
    txt += '@fae=\n'
    txt += '@lay=rw\n'
    txt += '@pro=\n'
    txt += '@qua=rw\n'

    txt += '\n[RD_SVN:/ProjectData/%s/Spec]\n' % name
    txt += '@AE=rw\n'
    txt += '@ana=rw\n'
    txt += '@dig=rw\n'
    txt += '@eng=r\n'
    txt += '@fae=\n'
    txt += '@lay=rw\n'
    txt += '@pro=\n'
    txt += '@qua=\n'

    txt += '\n[RD_SVN:/ProjectData/%s/Test_Specification]\n' % name
    txt += '@AE=rw\n'
    txt += '@ana=rw\n'
    txt += '@dig=rw\n'
    txt += '@eng=rw\n'
    txt += '@fae=\n'
    txt += '@lay=rw\n'
    txt += '@pro=\n'
    txt += '@quar=\n'

    txt += '\n[RD_SVN:/ProjectData/%s/User_Manual]\n' % name
    txt += '@AE=rw\n'
    txt += '@ana=rw\n'
    txt += '@dig=rw\n'
    txt += '@eng=r\n'
    txt += '@fae=r\n'
    txt += '@lay=r\n'
    txt += '@pro=r\n'
    txt += '@qua=r\n'

    txt += '\n[RD_SVN:/ProjectData/%s/Verify]\n' % name
    txt += '@AE=rw\n'
    txt += '@ana=rw\n'
    txt += '@dig=rw\n'
    txt += '@eng=rw\n'
    txt += '@fae=\n'
    txt += '@lay=rw\n'
    txt += '@pro=\n'
    txt += '@qua=r\n'

    txt += '\n[RD_SVN:/ProjectData/%s/产品发布]\n' % name
    txt += '@AE=rw\n'
    txt += '@ana=rw\n'
    txt += '@dig=rw\n'
    txt += '@eng=rw\n'
    txt += '@fae=\n'
    txt += '@lay=rw\n'
    txt += '@pro=\n'
    txt += '@qua=\n'

    return txt


def main():
    # txt = read_file(auth_file)
    txt = project_auth(proj_name[0])
    # print(txt)

    with open(out_file, 'w+') as f:
        f.write(txt)


if __name__ == '__main__':
    main()
