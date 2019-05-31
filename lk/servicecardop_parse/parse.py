from struct import Struct


def formatRecord(record):
    t = record[0]
    va = record[1]
    vr = record[2]
    vs = record[3]
    rw = record[4]
    rs = record[5]
    rsg = record[6]
    mid = record[7] + record[8] + record[9] + record[10] + record[11] + record[12] + record[13] + record[14] + record[15] + record[16] + record[17] + record[18] + record[19] + record[20] + record[21] + record[22]
    res = []
    res.append(mid)
    res.append(t)
    res.append(va)
    res.append(vr)
    res.append(vs)
    res.append(rw)
    res.append(rs)
    res.append(rsg)
    return res


def read_records(fpath):
    res = []
    with open(fpath, 'rb') as fl:
        data = fl.read()
    if data == b'':
        return null
    l = len(data)
    headST = Struct('<i')
    busiST1 = Struct('<iiiiiiicccccccccccccccc')
    busiST2 = Struct('<illllllcccccccccccccccc')
    i = 0
    while i < l:
        hs = headST.unpack_from(data, i)
        f = hs[0] & 0x00000003;
        if f == 0 :
            busi = busiST1.unpack_from(data, i)
            t = formatRecord(busi)
            res.append(t)
            i += 44
        elif f == 1:
            busi = busiST2.unpack_from(data, i)
            busi[0] =  busi[0] & 0xfffffffc
            res.append(formatRecord(busi))
            i += 68
        else:
            print('error\n')
            break
    return res


if __name__ == '__main__':
	res = read_records('./8.log')
	print(res)
