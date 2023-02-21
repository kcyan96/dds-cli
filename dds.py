
import sys
from ctypes import *

dds = cdll.LoadLibrary("dds.dll" if sys.platform == "win32" else "libdds.so")


""" Constants """
DDS_VERSION = 20900

DDS_HANDS = 4
DDS_SUITS = 4
DDS_STRAINS = 5

MAXNOOFBOARDS = 200
MAXNOOFTABLES = 40


""" Structs """
class deal(Structure):
    _fields_ = [("trump", c_int),
                ("first", c_int),
                ("currentTrickSuit", c_int * 3),
                ("currentTrickRank", c_int * 3),
                ("remainCards", c_uint * DDS_SUITS * DDS_HANDS)]

class dealPBN(Structure):
    _fields_ = [("trump", c_int),
                ("first", c_int),
                ("currentTrickSuit", c_int * 3),
                ("currentTrickRank", c_int * 3),
                ("remainCards", c_char * 80)]

class ddTableDeal(Structure):
    _fields_ = [("cards", c_uint * DDS_SUITS * DDS_HANDS)]

class ddTableDealPBN(Structure):
    _fields_ = [("cards", c_char * 80)]

class ddTableDeals(Structure):
    _fields_ = [("noOfTables", c_int),
                ("deals", ddTableDeal * (MAXNOOFTABLES * DDS_STRAINS))]

class ddTableDealsPBN(Structure):
    _fields_ = [("noOfTables", c_int),
                ("deals", ddTableDealPBN * (MAXNOOFTABLES * DDS_STRAINS))]

class ddTableResults(Structure):
    _fields_ = [("resTable", c_int * DDS_HANDS * DDS_STRAINS)]

class ddTablesRes(Structure):
    _fields_ = [("noOfBoards", c_int),
                ("results", ddTableResults * (MAXNOOFTABLES * DDS_STRAINS))]

class parResults(Structure):
    # index = 0 is NS view and index = 1 is EW view. 
    # By 'view' here meant which side that starts the bidding.
    _fields_ = [("parScore", c_char * 16 * 2),
                ("parContractsString", c_char * 128 * 2)]

class allParResults(Structure):
    _fields_ = [("presults", parResults * MAXNOOFTABLES)]

class parResultsDealer(Structure):
    # number: Number of contracts yielding the par score.
    # score: Par score for the specified dealer hand.
    # contracts: Par contract text strings. The first contract is in contracts[0], the last one in contracts[number-1]
    _fields_ = [("number", c_int),
                ("score", c_int),
                ("contracts", c_char * 10 * 10)]

class contractType(Structure):
    # undertricks: 0 = make; 1-13 = sacrifice
    # overTricks: 0-3; e.g. 1 for 4S + 1
    # level: 1-7
    # denom: 0 = No Trumps, 1 = trump Spades, 2 = trump Hearts, 3 = trump Diamonds, 4 = trump Clubs
    # seats: One of the cases N, E, S, W, NS, EW; 0 = N, 1 = E, 2 = S, 3 = W, 4 = NS, 5 = EW
    _fields_ = [("underTricks", c_int),
                ("overTricks", c_int),
                ("level", c_int),
                ("denom", c_int),
                ("seats", c_int)]

class parResultsMaster(Structure):
    # score: Sign acccording to NS view
    # number: Number of contracts giving the par score
    # contracts: Par contracts
    _fields_ = [("score", c_int),
                ("number", c_int),
                ("contracts", contractType * 10)]

class parTextResults(Structure):
    # parText: Short text for par information, e.g. Par -110: EW 2S  EW 2D+1
    # equal: TRUE in the normal case when it does not matter who starts the bidding. Otherwise, FALSE.
    _fields_ = [("parTextResults", c_char * 128 * 2),
                ("equal", c_int)]
    
class boards(Structure):
    _fields_ = [("noOfBoards", c_int),
                ("deals", deal * MAXNOOFBOARDS),
                ("target", c_int * MAXNOOFBOARDS),
                ("solutions", c_int * MAXNOOFBOARDS),
                ("mode", c_int * MAXNOOFBOARDS)]

class boardsPBN(Structure):
    _fields_ = [("noOfBoards", c_int),
                ("deals", dealPBN * MAXNOOFBOARDS),
                ("target", c_int * MAXNOOFBOARDS),
                ("solutions", c_int * MAXNOOFBOARDS),
                ("mode", c_int * MAXNOOFBOARDS)]

class futureTricks(Structure):
    _fields_ = [("nodes", c_int),
                ("cards", c_int),
                ("suit", c_int * 13),
                ("rank", c_int * 13),
                ("equals", c_int * 13),
                ("score", c_int * 13)]

class solvedBoards(Structure):
    _fields_ = [("noOfBoards", c_int),
                ("solvedBoards", futureTricks * MAXNOOFBOARDS)]

class playTraceBin(Structure):
    _fields_ = [("number", c_int),
                ("suit", c_int * 52),
                ("rank", c_int * 52)]

class playTracePBN(Structure):
    _fields_ = [("number", c_int),
                ("cards", c_char * 106)]

class playTracesBin(Structure):
    _fields_ = [("noOfBoards", c_int),
                ("plays", playTraceBin * MAXNOOFBOARDS)]

class playTracesPBN(Structure):
    _fields_ = [("noOfBoards", c_int),
                ("plays", playTracePBN * MAXNOOFBOARDS)]

class solvedPlay(Structure):
    _fields_ = [("number", c_int),
                ("tricks", c_int * 53)]

class solvedPlays(Structure):
    _fields_ = [("noOfBoards", c_int),
                ("solved", solvedPlay * MAXNOOFBOARDS)]
    
class DDSInfo(Structure):
    # system: 0=unknown, 1=Windows, 2=Cygwin, 3=Linux, 4=Apple
    # compiler: 0=unknown, 1=Microsoft Visual C++, 2=mingw, 3=GNU, 4=clang
    # constructor: 0=none, 1=DllMain, 2=Unix-style
    # threading: 0=none, 1=Windows(native), 2=OpenMP, 3=GCD, 4=Boost, 5=STL, 6=TBB, 7=STLIMPL(for_each), 8=PPLIMPL(for_each)
    _fields_ = [("major", c_int),
                ("minor", c_int),
                ("patch", c_int),
                ("versionString", c_char * 10),
                ("system", c_int),
                ("numBits", c_int),
                ("compiler", c_int),
                ("constructor", c_int),
                ("numCores", c_int),
                ("threading", c_int),
                ("noOfThreads", c_int),
                ("threadSizes", c_char * 128),
                ("systemString", c_char * 1024)]


""" Functions """

# CalcDDtable(ddTableDeal tableDeal, ddTableResults* tablep)
CalcDDtable = dds.CalcDDtable
CalcDDtable.argtypes = [ddTableDeal, POINTER(ddTableResults)]
CalcDDtable.restype = c_int

# CalcDDtablePBN(ddTableDealPBN tableDealPBN, ddTableResults* tablep)
CalcDDtablePBN = dds.CalcDDtablePBN
CalcDDtablePBN.argtypes = [ddTableDealPBN, POINTER(ddTableResults)]
CalcDDtablePBN.restype = c_int

# CalcAllTables(ddTableDeals* dealsp, int mode, int trumpFilter[5], ddTablesRes* resp, allParResults* presp)
CalcAllTables = dds.CalcAllTables
CalcAllTables.argtypes = [POINTER(ddTableDeals), c_int, c_int * DDS_STRAINS, POINTER(ddTablesRes), POINTER(allParResults)]
CalcAllTables.restype = c_int

# CalcAllTablesPBN(ddTableDealsPBN* dealsp, int mode, int trumpFilter[5], ddTablesRes* resp, allParResults* presp)
CalcAllTablesPBN = dds.CalcAllTablesPBN
CalcAllTablesPBN.argtypes = [POINTER(ddTableDealsPBN), c_int, c_int * DDS_STRAINS, POINTER(ddTablesRes), POINTER(allParResults)]
CalcAllTablesPBN.restype = c_int

# Par(ddTableResults* tablep, parResults* presp, int vulnerable)
Par = dds.Par
Par.argtypes = [POINTER(ddTableResults), POINTER(parResults), c_int]
Par.restype = c_int

# DealerPar(ddTableResults* tablep, parResultsDealer* presp, int dealer, int vulnerable)
DealerPar = dds.DealerPar
DealerPar.argtypes = [POINTER(ddTableResults), POINTER(parResultsDealer), c_int, c_int]
DealerPar.restype = c_int

# DealerParBin(ddTableResults* tablep, parResultsMaster* presp, int dealer, int vulnerable)
DealerParBin = dds.DealerParBin
DealerParBin.argtypes = [POINTER(ddTableResults), POINTER(parResultsMaster), c_int, c_int]
DealerParBin.restype = c_int

# ConvertToDealerTextFormat(parResultsMaster* pres, char* resp)
ConvertToDealerTextFormat = dds.ConvertToDealerTextFormat
ConvertToDealerTextFormat.argtypes = [POINTER(parResultsMaster), c_char_p]
ConvertToDealerTextFormat.restype = c_int

# SidesPar(ddTableResults* tablep, parResultsDealer* sidesRes[2], int vulnerable)
SidesPar = dds.SidesPar
SidesPar.argtypes = [POINTER(ddTableResults), parResultsDealer * 2, c_int]
SidesPar.restypes = c_int

# SidesParBin(ddTableResults* tablep, parResultsMaster sidesRes[2], int vulnerable)
SidesParBin = dds.SidesParBin
SidesParBin.argtypes = [POINTER(ddTableResults), parResultsMaster * 2, c_int]
SidesParBin.restype = c_int

# ConvertToSidesTextFormat(parResultsMaster* pres, parTextResults * resp)
ConvertToSidesTextFormat = dds.ConvertToSidesTextFormat
ConvertToSidesTextFormat.argtypes = [POINTER(parResultsMaster), POINTER(parTextResults)]
ConvertToSidesTextFormat.restype = c_int

# CalcPar(ddTableDeal, int ulnerable, ddTablesRes* tablep, parResults* presp)
CalcPar = dds.CalcPar
CalcPar.argtypes = [ddTableDeal, c_int, POINTER(ddTableResults), POINTER(parResults)]
CalcPar.restype = c_int

# CalcParPBN(ddTableDealPBN tableDealPBN, ddTableResults* tablep, int vulnerable, parResults* presp)
CalcParPBN = dds.CalcParPBN
CalcParPBN.argtypes = [ddTableDealPBN, POINTER(ddTableResults), c_int, POINTER(parResults)]
CalcParPBN.restype = c_int

# SolveBoard(deal dl, int target, int solutions, int mode, futureTricks* futp, int threadIndex)
SolveBoard = dds.SolveBoard
SolveBoard.argtypes = [deal, c_int, c_int, c_int, POINTER(futureTricks), c_int]
SolveBoard.restype = c_int

# SolveBoardPBN(dealPBN dlPBN, int target, int solutions, int mode, futureTricks* futp, int threadIndex)
SolveBoardPBN = dds.SolveBoardPBN
SolveBoardPBN.argtypes = [dealPBN, c_int, c_int, c_int, POINTER(futureTricks), c_int]
SolveBoardPBN.restype = c_int

# SolveAllChunksBin(boards* bop, solvedBoards* solvedp, int chunkSize)
SolveAllChunksBin = dds.SolveAllChunksBin
SolveAllChunksBin.argtypes = [POINTER(boards), POINTER(solvedBoards), c_int]
SolveAllChunksBin.restype = c_int

# SolveAllBoards(boardsPBN* bop, solvedBoards* solvedp)
SolveAllBoards = dds.SolveAllBoards
SolveAllBoards.argtypes = [POINTER(boardsPBN), POINTER(solvedBoards)]
SolveAllBoards.restype = c_int

# AnalysePlayBin(deal dl, playTraceBin play, solvedPlay* solved, int thrId)
AnalysePlayBin = dds.AnalysePlayBin
AnalysePlayBin.argtypes = [deal, playTraceBin, POINTER(solvedPlay), c_int]
AnalysePlayBin.restype = c_int

# AnalysePlayPBN(dealPBN dlPBN, playTracePBN playPBN, solvedPlay* solvedp, int thrId)
AnalysePlayPBN = dds.AnalysePlayPBN
AnalysePlayPBN.argtypes = [dealPBN, playTracePBN, POINTER(solvedPlay), c_int]
AnalysePlayPBN.restype = c_int

# AnalyseAllPlaysBin(boards* bop, playTracesBin* plp, solvedPlays* solvedp, int chunkSize)
AnalyseAllPlaysBin = dds.AnalyseAllPlaysBin
AnalyseAllPlaysBin.argtypes = [POINTER(boards), POINTER(playTracesBin), POINTER(solvedPlays), c_int]
AnalyseAllPlaysBin.restype = c_int

# AnalyseAllPlaysPBN(boardsPBN* bopPBN, playTracesPBN* plpPBN, solvedPlays* solvedp, int chunkSize)
AnalyseAllPlaysPBN = dds.AnalyseAllPlaysPBN
AnalyseAllPlaysPBN.argtypes = [POINTER(boardsPBN), POINTER(playTracesPBN), POINTER(solvedPlays), c_int]
AnalyseAllPlaysPBN.restype = c_int

# SetThreading(int code)
SetThreading = dds.SetThreading
SetThreading.argtypes = [c_int]
SetThreading.restype = None

# SetMaxThreads(int userThreads)
SetMaxThreads = dds.SetMaxThreads
SetMaxThreads.argtypes = [c_int]
SetMaxThreads.restype = None

# SetResources(int maxMemoryMB, int maxThreads)
SetResources = dds.SetResources
SetResources.argtypes = [c_int, c_int]
SetResources.restype = None

# FreeMemory()
FreeMemory = dds.FreeMemory
FreeMemory.argtypes = None
FreeMemory.restype = None

# GetDDSInfo(DDSInfo* info)
GetDDSInfo = dds.GetDDSInfo
GetDDSInfo.argtypes = [POINTER(DDSInfo)]
GetDDSInfo.restype = None

# ErrorMessage(int code, char line[80])
ErrorMessage = dds.ErrorMessage
ErrorMessage.argtypes = [c_int, c_char * 80]
ErrorMessage.restype = None

