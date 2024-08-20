from enum import Enum

class ISA(Enum):
    VIMA = "vima"
    AVX2 = "avx2"

class VVC_constants(Enum):
    CTU_size = 128

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

FIXED_TO_FRAC_POS = {
        (0     , 0     ) : 0,
        (0     , 0.25  ) : 1,
        (0     , 0.5   ) : 2,
        (0     , 0.75  ) : 3,
        (0.25  , 0     ) : 4,
        (0.25  , 0.25  ) : 5,
        (0.25  , 0.5   ) : 6,
        (0.25  , 0.75  ) : 7,
        (0.5   , 0     ) : 8,
        (0.5   , 0.25  ) : 9,
        (0.5   , 0.5   ) : 10,
        (0.5   , 0.75  ) : 11,
        (0.75  , 0     ) : 12,
        (0.75  , 0.25  ) : 13,
        (0.75  , 0.5   ) : 14,
        (0.75  , 0.75  ) : 15,
    }

FRAC_POS_TO_FIXED = {
        0  : (0     , 0     ),
        1  : (0     , 0.25  ),
        2  : (0     , 0.5   ),
        3  : (0     , 0.75  ),
        4  : (0.25  , 0     ),
        5  : (0.25  , 0.25  ),
        6  : (0.25  , 0.5   ),
        7  : (0.25  , 0.75  ),
        8  : (0.5   , 0     ),
        9  : (0.5   , 0.25  ),
        10 : (0.5   , 0.5   ),
        11 : (0.5   , 0.75  ),
        12 : (0.75  , 0     ),
        13 : (0.75  , 0.25  ),
        14 : (0.75  , 0.5   ),
        15 : (0.75  , 0.75  ),   
}

YUV_VIDEOS = {
    #C Class
    'RaceHorsesC' : {'yuv' : 'RaceHorsesC_832x480_30.yuv','res' : '832x480', 'bit_depth' : 8 },
    'BasketballDrill' : {'yuv' : 'BasketballDrill_832x480_50.yuv','res' : '832x480', 'bit_depth' : 8 },
    'BQMall' : { 'yuv' : 'BQMall_832x480_60.yuv','res' : '832x480', 'bit_depth' : 8 },
    'PartyScene' : { 'yuv' : 'PartyScene_832x480_50.yuv','res' : '832x480', 'bit_depth' : 8 },

    #B Class
    'BasketballDrive' : { 'yuv' : 'BasketballDrive_1920x1080_50.yuv','res' : '1920x1080', 'bit_depth' : 8 },
    'MarketPlace' : { 'yuv' : 'MarketPlace_1920x1080_60fps_10bit_420.yuv','res' : '1920x1080', 'bit_depth' : 10 },
    'RitualDance' : {'yuv' : 'RitualDance_1920x1080_60fps_10bit_420.yuv','res' : '1920x1080', 'bit_depth' : 10 },
    'Cactus': {'yuv' : 'Cactus_1920x1080_50.yuv','res' : '1920x1080', 'bit_depth' : 8 },
    'BQTerrace'  : { 'yuv' : 'BQTerrace_1920x1080_60.yuv','res' : '1920x1080', 'bit_depth' : 8 },
    
    #A2 Class
    'CatRobot' : { 'yuv' : 'CatRobot_3840x2160_60fps_10bit_420_jvet.yuv','res' : '3840x2160', 'bit_depth' : 10 },
    'DaylightRoad2' : {'yuv' : 'DaylightRoad2_3840x2160_60fps_10bit_420.yuv','res' : '3840x2160', 'bit_depth' : 10 },
    'ParkRunning3' : { 'yuv' : 'ParkRunning3_3840x2160_50fps_10bit_420.yuv','res' : '3840x2160', 'bit_depth' : 10 },

    #A1 Class
    'Campfire'  : { 'yuv' : 'Campfire_3840x2160_30fps_bt709_420_videoRange.yuv','res' : '3840x2160', 'bit_depth' : 10 },
    'Tango2' : { 'yuv' : 'Tango2_3840x2160_60fps_10bit_420.yuv','res' : '3840x2160', 'bit_depth' : 10 },
    'FoodMarket4' : { 'yuv' : 'FoodMarket4_3840x2160_60fps_10bit_420.yuv','res' : '3840x2160', 'bit_depth' : 10 },
}