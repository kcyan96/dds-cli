
import dds
import ctypes
import itertools
import sys


VUL = [[0,7,10,13], [3,6,9,12], [1,4,11,14], [2,5,8,15]]

def solve32(lines, vul):
    deals = dds.ddTableDealsPBN()
    deals.noOfTables = len(lines)
    for i in range(deals.noOfTables):
        deals.deals[i].cards = lines[i]
    
    mode = vul
    trumpFilter = (ctypes.c_int * dds.DDS_STRAINS)(0,0,0,0,0)
    tables = dds.ddTablesRes()
    pars = dds.allParResults()
    
    res = dds.CalcAllTablesPBN(ctypes.pointer(deals), mode, trumpFilter, ctypes.pointer(tables), ctypes.pointer(pars))
    if res != 1: return None
    res_ddt = [''.join([''.join([f'{r.resTable[s][h]:x}' for s in [3,2,1,0,4]]) for h in [0,2,1,3]]) for r in tables.results[:deals.noOfTables]]
    res_par = ["|".join([(ctypes.cast(p.parContractsString[s], ctypes.c_char_p).value + b';' + ctypes.cast(p.parScore[s], ctypes.c_char_p).value[3:]).decode('utf-8') for s in [0,1]]) for p in pars.presults[:deals.noOfTables]]
    return ['|'.join(x) for x in zip(res_ddt, res_par)]


inputs = [bytes(s[:-1], 'utf-8') for s in sys.stdin.readlines()]
boards = [[inputs[i] for i in range(len(inputs)) if i%16 in VUL[v]] for v in range(4)]
solved = [list(itertools.chain(*[solve32(boards[v][i:i+32], v) for i in range(0, len(boards[v]), 32)])) for v in range(4)]
result = [(boards[a][b], solved[a][b]) for a,b in [[(i, n//16*4 + x.index(n%16)) for i,x in enumerate(VUL) if n%16 in x][0] for n in range(sum(map(len, boards)))]]
assert all([x[0]==inputs[i] and x[1] is not None for i,x in enumerate(result)])
sys.stdout.write('\n'.join([s for b,s in result]))

