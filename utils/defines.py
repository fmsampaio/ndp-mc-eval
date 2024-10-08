from enum import Enum

class ISA(Enum):
    VIMA = "vima"
    AVX2 = "avx2"

class VVC_constants(Enum):
    CTU_size = 128
    INTERP_WINDOW_WIDTH = 2048

class Pred_Modes(Enum):
    Inter = 0
    Intra = 1

class Token_offset(Enum):
    Blockstat = 0
    Frame = 1
    CU_position_x = 2
    CU_position_y = 3
    CU_x_size = 4
    CU_y_size = 5
    Metric = 6

    MV_x = 7
    MV_y = 8

    MVD_x = 7
    MVD_y = 8
    PredMode = -1


YUV_VIDEOS = {
    #C Class
    'RaceHorsesC' : {'yuv' : 'RaceHorsesC_832x480_30.yuv','res' : (832, 480), 'bit_depth' : 8 },
    'BasketballDrill' : {'yuv' : 'BasketballDrill_832x480_50.yuv','res' : (832, 480), 'bit_depth' : 8 },
    'BQMall' : { 'yuv' : 'BQMall_832x480_60.yuv','res' : (832, 480), 'bit_depth' : 8 },
    'PartyScene' : { 'yuv' : 'PartyScene_832x480_50.yuv','res' : (832, 480), 'bit_depth' : 8 },

    #B Class
    'BasketballDrive' : { 'yuv' : 'BasketballDrive_1920x1080_50.yuv','res' : (1920,1080), 'bit_depth' : 8 },
    'MarketPlace' : { 'yuv' : 'MarketPlace_1920x1080_60fps_10bit_420.yuv','res' : (1920,1080), 'bit_depth' : 10 },
    'RitualDance' : {'yuv' : 'RitualDance_1920x1080_60fps_10bit_420.yuv','res' : (1920,1080), 'bit_depth' : 10 },
    'Cactus': {'yuv' : 'Cactus_1920x1080_50.yuv','res' : (1920,1080), 'bit_depth' : 8 },
    'BQTerrace'  : { 'yuv' : 'BQTerrace_1920x1080_60.yuv','res' : (1920,1080), 'bit_depth' : 8 },
    
    #A2 Class
    'CatRobot' : { 'yuv' : 'CatRobot_3840x2160_60fps_10bit_420_jvet.yuv','res' : (3840,2160), 'bit_depth' : 10 },
    'DaylightRoad2' : {'yuv' : 'DaylightRoad2_3840x2160_60fps_10bit_420.yuv','res' : (3840,2160), 'bit_depth' : 10 },
    'ParkRunning3' : { 'yuv' : 'ParkRunning3_3840x2160_50fps_10bit_420.yuv','res' : (3840,2160), 'bit_depth' : 10 },

    #A1 Class
    'Campfire'  : { 'yuv' : 'Campfire_3840x2160_30fps_bt709_420_videoRange.yuv','res' : (3840,2160), 'bit_depth' : 10 },
    'Tango2' : { 'yuv' : 'Tango2_3840x2160_60fps_10bit_420.yuv','res' : (3840,2160), 'bit_depth' : 10 },
    'FoodMarket4' : { 'yuv' : 'FoodMarket4_3840x2160_60fps_10bit_420.yuv','res' : (3840,2160), 'bit_depth' : 10 },

    #Netflix sequences
    'Aerial' : { 'yuv' : 'Netflix_Aerial_4096x2160_60fps_10bit_420.y4m', 'res' : (4096, 2160), 'bit_depth' : 10 },
    'BarScene' : { 'yuv' : 'Netflix_BarScene_4096x2160_60fps_10bit_420.y4m', 'res' : (4096, 2160), 'bit_depth' : 10 },
    'Boat' : { 'yuv' : 'Netflix_Boat_4096x2160_60fps_10bit_420.y4m', 'res' : (4096, 2160), 'bit_depth' : 10 },
    'BoxingPractice' : { 'yuv' : 'Netflix_BoxingPractice_4096x2160_60fps_10bit_420.y4m', 'res' : (4096, 2160), 'bit_depth' : 10 },
    'Crosswalk' : { 'yuv' : 'Netflix_Crosswalk_4096x2160_60fps_10bit_420.y4m', 'res' : (4096, 2160), 'bit_depth' : 10 },
    'Dancers' : { 'yuv' : 'Netflix_Dancers_4096x2160_60fps_10bit_420.y4m', 'res' : (4096, 2160), 'bit_depth' : 10 },
    'DinnerScene' : { 'yuv' : 'Netflix_DinnerScene_4096x2160_60fps_10bit_420.y4m', 'res' : (4096, 2160), 'bit_depth' : 10 },
    'DrivingPOV' : { 'yuv' : 'Netflix_DrivingPOV_4096x2160_60fps_10bit_420.y4m', 'res' : (4096, 2160), 'bit_depth' : 10 },
    'Narrator' : { 'yuv' : 'Netflix_Narrator_4096x2160_60fps_10bit_420.y4m', 'res' : (4096, 2160), 'bit_depth' : 10 },
    'PierSeaside' : { 'yuv' : 'Netflix_PierSeaside_4096x2160_60fps_10bit_420.y4m', 'res' : (4096, 2160), 'bit_depth' : 10 },
    'RollerCoaster' : { 'yuv' : 'Netflix_RollerCoaster_4096x2160_60fps_10bit_420.y4m', 'res' : (4096, 2160), 'bit_depth' : 10 },
    'SquareAndTimelapse' : { 'yuv' : 'Netflix_SquareAndTimelapse_4096x2160_60fps_10bit_420.y4m', 'res' : (4096, 2160), 'bit_depth' : 10 },
    'ToddlerFountain' : { 'yuv' : 'Netflix_ToddlerFountain_4096x2160_60fps_10bit_420.y4m', 'res' : (4096, 2160), 'bit_depth' : 10 },
    'TunnelFlag' : { 'yuv' : 'Netflix_TunnelFlag_4096x2160_60fps_10bit_420.y4m', 'res' : (4096, 2160), 'bit_depth' : 10 },
    'WindAndNature' : { 'yuv' : 'Netflix_WindAndNature_4096x2160_60fps_10bit_420.y4m', 'res' : (4096, 2160), 'bit_depth' : 10 },
}

MV_TO_FRAC_POS = {  (0,0) : 'I', (0,1) : 'S', (0,2) : 'S', (0,3) : 'S', (0,4) : 'Q0', (0,5) : 'S', (0,6) : 'S', (0,7) : 'S', (0,8) : 'H0', (0,9) : 'S', (0,10) : 'S', (0,11) : 'S', (0,12) : 'Q1', (0,13) : 'S', (0,14) : 'S', (0,15) : 'S', (1,0) : 'S', (1,1) : 'S', (1,2) : 'S', (1,3) : 'S', (1,4) : 'S', (1,5) : 'S', (1,6) : 'S', (1,7) : 'S', (1,8) : 'S', (1,9) : 'S', (1,10) : 'S', (1,11) : 'S', (1,12) : 'S', (1,13) : 'S', (1,14) : 'S', (1,15) : 'S', (2,0) : 'S', (2,1) : 'S', (2,2) : 'S', (2,3) : 'S', (2,4) : 'S', (2,5) : 'S', (2,6) : 'S', (2,7) : 'S', (2,8) : 'S', (2,9) : 'S', (2,10) : 'S', (2,11) : 'S', (2,12) : 'S', (2,13) : 'S', (2,14) : 'S', (2,15) : 'S', (3,0) : 'S', (3,1) : 'S', (3,2) : 'S', (3,3) : 'S', (3,4) : 'S', (3,5) : 'S', (3,6) : 'S', (3,7) : 'S', (3,8) : 'S', (3,9) : 'S', (3,10) : 'S', (3,11) : 'S', (3,12) : 'S', (3,13) : 'S', (3,14) : 'S', (3,15) : 'S', (4,0) : 'Q2', (4,1) : 'S', (4,2) : 'S', (4,3) : 'S', (4,4) : 'Q3', (4,5) : 'S', (4,6) : 'S', (4,7) : 'S', (4,8) : 'Q4', (4,9) : 'S', (4,10) : 'S', (4,11) : 'S', (4,12) : 'Q5', (4,13) : 'S', (4,14) : 'S', (4,15) : 'S', (5,0) : 'S', (5,1) : 'S', (5,2) : 'S', (5,3) : 'S', (5,4) : 'S', (5,5) : 'S', (5,6) : 'S', (5,7) : 'S', (5,8) : 'S', (5,9) : 'S', (5,10) : 'S', (5,11) : 'S', (5,12) : 'S', (5,13) : 'S', (5,14) : 'S', (5,15) : 'S', (6,0) : 'S', (6,1) : 'S', (6,2) : 'S', (6,3) : 'S', (6,4) : 'S', (6,5) : 'S', (6,6) : 'S', (6,7) : 'S', (6,8) : 'S', (6,9) : 'S', (6,10) : 'S', (6,11) : 'S', (6,12) : 'S', (6,13) : 'S', (6,14) : 'S', (6,15) : 'S', (7,0) : 'S', (7,1) : 'S', (7,2) : 'S', (7,3) : 'S', (7,4) : 'S', (7,5) : 'S', (7,6) : 'S', (7,7) : 'S', (7,8) : 'S', (7,9) : 'S', (7,10) : 'S', (7,11) : 'S', (7,12) : 'S', (7,13) : 'S', (7,14) : 'S', (7,15) : 'S', (8,0) : 'H1', (8,1) : 'S', (8,2) : 'S', (8,3) : 'S', (8,4) : 'Q6', (8,5) : 'S', (8,6) : 'S', (8,7) : 'S', (8,8) : 'H2', (8,9) : 'S', (8,10) : 'S', (8,11) : 'S', (8,12) : 'Q7', (8,13) : 'S', (8,14) : 'S', (8,15) : 'S', (9,0) : 'S', (9,1) : 'S', (9,2) : 'S', (9,3) : 'S', (9,4) : 'S', (9,5) : 'S', (9,6) : 'S', (9,7) : 'S', (9,8) : 'S', (9,9) : 'S', (9,10) : 'S', (9,11) : 'S', (9,12) : 'S', (9,13) : 'S', (9,14) : 'S', (9,15) : 'S', (10,0) : 'S', (10,1) : 'S', (10,2) : 'S', (10,3) : 'S', (10,4) : 'S', (10,5) : 'S', (10,6) : 'S', (10,7) : 'S', (10,8) : 'S', (10,9) : 'S', (10,10) : 'S', (10,11) : 'S', (10,12) : 'S', (10,13) : 'S', (10,14) : 'S', (10,15) : 'S', (11,0) : 'S', (11,1) : 'S', (11,2) : 'S', (11,3) : 'S', (11,4) : 'S', (11,5) : 'S', (11,6) : 'S', (11,7) : 'S', (11,8) : 'S', (11,9) : 'S', (11,10) : 'S', (11,11) : 'S', (11,12) : 'S', (11,13) : 'S', (11,14) : 'S', (11,15) : 'S', (12,0) : 'Q8', (12,1) : 'S', (12,2) : 'S', (12,3) : 'S', (12,4) : 'Q9', (12,5) : 'S', (12,6) : 'S', (12,7) : 'S', (12,8) : 'Q10', (12,9) : 'S', (12,10) : 'S', (12,11) : 'S', (12,12) : 'Q11', (12,13) : 'S', (12,14) : 'S', (12,15) : 'S', (13,0) : 'S', (13,1) : 'S', (13,2) : 'S', (13,3) : 'S', (13,4) : 'S', (13,5) : 'S', (13,6) : 'S', (13,7) : 'S', (13,8) : 'S', (13,9) : 'S', (13,10) : 'S', (13,11) : 'S', (13,12) : 'S', (13,13) : 'S', (13,14) : 'S', (13,15) : 'S', (14,0) : 'S', (14,1) : 'S', (14,2) : 'S', (14,3) : 'S', (14,4) : 'S', (14,5) : 'S', (14,6) : 'S', (14,7) : 'S', (14,8) : 'S', (14,9) : 'S', (14,10) : 'S', (14,11) : 'S', (14,12) : 'S', (14,13) : 'S', (14,14) : 'S', (14,15) : 'S', (15,0) : 'S', (15,1) : 'S', (15,2) : 'S', (15,3) : 'S', (15,4) : 'S', (15,5) : 'S', (15,6) : 'S', (15,7) : 'S', (15,8) : 'S', (15,9) : 'S', (15,10) : 'S', (15,11) : 'S', (15,12) : 'S', (15,13) : 'S', (15,14) : 'S', (15,15) : 'S', }

MV_TO_FRAC_POS_QUARTER = {  
    (0,0)   : 0,
    (0,4)   : 1,
    (0,8)   : 2,
    (0,12)  : 3,
    (4,0)   : 4 ,
    (4,4)   : 5 ,
    (4,8)   : 6 ,
    (4,12)  : 7 ,
    (8,0)   : 8 ,
    (8,4)   : 9 ,
    (8,8)   : 10,
    (8,12)  : 11,
    (12,0)  : 12,
    (12,4)  : 13,
    (12,8)  : 14,
    (12,12) : 15,
 }

FRAC_POS_LIST = [
    'I', 'H0', 'H1', 'H2', 'Q0', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11'
]

INTERP_OPERATIONS = {
    0 : ['I'],
    1 : ['V', 'V'],
    2 : ['V'],
    3 : ['V', 'V'],
    4 : ['H', 'H'],
    5 : ['H', 'H', 'V', 'V'],
    6 : ['H', 'H', 'V'],
    7 : ['H', 'H', 'V', 'V'],
    8 : ['H'],
    9 : ['H', 'V', 'V'],
    10 : ['H', 'V'],
    11 : ['H', 'V', 'V'],
    12 : ['H', 'H'],
    13 : ['H', 'H', 'V', 'V'],
    14 : ['H', 'H', 'V'],
    15 : ['H', 'H', 'V', 'V'],
}

FRAC_INTERP_DEPENDENCIES = {
    0  : [] ,
    1  : [[2]] ,
    2  : [] ,
    3  : [[2]] ,
    4  : [[8]] ,
    5  : [[8, 4, 6], [2, 1, 9]] ,
    6  : [[2, 10]] ,
    7  : [[8, 4, 6], [2, 3, 11]] ,
    8  : [] ,
    9  : [[8, 10]] ,
    10 : [[8], [2]] ,
    11 : [[8, 10]] ,
    12 : [[8]] ,
    13 : [[8, 12, 14], [2, 1, 9]] ,
    14 : [[2, 10]] ,
    15 : [[8, 12, 14], [2, 3, 11]] ,
}

FRAC_HALF_POS = [2, 8]
