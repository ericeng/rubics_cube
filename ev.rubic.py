#!
#
# File: rubic.py
#
# Written by: G. Eric Engstrom
#
# Copyright (C) 2020, All Rights Reserved
#
# Date: 2020-02-23
#
# Released under the MIT Open Source License
# need MIT url here
#

#
# The purpose to demonstrate solving the Rubics cube using different Computer Science approaches.
#
# This file contains the data structures and algorithm for changing the state of the cube.
#
# Each algorithm includes this file, so they all share a common description of the same 'reality'.
#

# The cube has the following orientation:
#     White is Top, it is represented by 0
#     Yellow is Bottom, it is represented by 1
#
#     Looking down from the Top
#         Red is 12 o'clock, it is represented by 2
#         Green is 3 o'clock, it is represented by 3
#         Orange is 6 o'clock, it is represented by 4
#         Blue is 9 o'clock, it is represented by 5
#
# The cube status is a list of three layers:
#     Top represented by 0
#     Middle represented by 1
#     Bottom represented by 2
#
# There is only one algorithm:
#     Rotate Side ( side, direction )
#     
#     side can have one of six values.
#       These are also represented by the center squares immutable color
#         CUBE_WHITE
#         CUBE_YELLOW
#         CUBE_RED
#         CUBE_GREEN
#         CUBE_ORANGE
#         CUBE_BLUE
#
#     direction is clockwise or counter clockwise
#       clockwise, it is represented by 0
#       counter clockwise, it is represented by 1
#
#  All assignments of COLOR follow clockwise from TOP down with RED as 0, 1200, or 2400 (top of the clock, aka High Noon)
#

import copy
import random
import inspect

class Meta(type):
  def __repr__(self):
    # Inspiration: https://stackoverflow.com/a/6811020
    callerframerecord = inspect.stack()[1]  # 0 represents this line
    # 1 represents line at caller
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    # print(info.filename)  # __FILE__     -> Test.py
    # print(info.function)  # __FUNCTION__ -> Main
    # print(info.lineno)  # __LINE__     -> 13
    return str(info.lineno)

class __LINE__(metaclass=Meta):
  pass

def __FILE__():
  return inspect.currentframe().f_code.co_filename

DEBUG_ROTATE_LABELS = 0
DEBUG_ROTATE = 0
DEBUG_ROTATE_FACES = 0
DEBUG_CELLS = 0
DEBUG_CUBE = 1
DEBUG_PRINTSIDE = 0
DEBUG_TEST_ROTATE = 0

TEST_ROTATE = 1
TEST_ROTATE_BACK = 2

TEST_ROTATE_NO_WHITE = 0
TEST_ROTATE_NO_YELLOW = 1
TEST_ROTATE_NO_RED = 1
TEST_ROTATE_NO_GREEN = 1
TEST_ROTATE_NO_ORANGE = 1
TEST_ROTATE_NO_BLUE = 1

TEST_ROTATE_RANDOM_ITERATIONS_1 = 100
TEST_ROTATE_RANDOM_ITERATIONS_2 = 100

PRINT_SIDE_LABEL = 1

CUBE_CUBE = 0

CUBE_WHITE = 1
CUBE_YELLOW = 2
CUBE_RED = 3
CUBE_GREEN = 4
CUBE_ORANGE = 5
CUBE_BLUE = 6

CUBE_END = CUBE_BLUE + CUBE_BLUE

CUBE_DELAY = 100

ROTATE_CLOCKWISE = 0
ROTATE_COUNTER = 1

CUBE_TOP = 0
CUBE_MIDDLE = 1
CUBE_BOTTOM = 2

CUBE_NULL = 0
CUBE_EDGE = 1
CUBE_CORNER = 2
CUBE_ID = 3

CUBE_SIDE_COUNT = 8

CUBE_TYPE = 0

CUBE_ID_0 = 1
CUBE_ID_FACE_0 = 2
CUBE_ID_SPACER = 9

CUBE_EDGE_0 = 1
CUBE_EDGE_1 = 2
CUBE_EDGE_FACE_0 = 3
CUBE_EDGE_FACE_1 = 4
CUBE_EDGE_ROTATED_FACE_FROM = 5
CUBE_EDGE_ROTATED_FACE_TO = 6

CUBE_CORNER_0 = 1
CUBE_CORNER_1 = 2
CUBE_CORNER_2 = 3
CUBE_CORNER_FACE_0 = 4
CUBE_CORNER_FACE_1 = 5
CUBE_CORNER_FACE_2 = 6

CUBE_NIL = [ CUBE_NULL, CUBE_NULL, CUBE_NULL, CUBE_NULL, CUBE_NULL, CUBE_NULL, CUBE_NULL, CUBE_NULL ]

class RubicsCube:

  _1030 = CUBE_NIL
  _0000 = CUBE_NIL
  _0130 = CUBE_NIL
  _0300 = CUBE_NIL
  _0430 = CUBE_NIL
  _0600 = CUBE_NIL
  _0730 = CUBE_NIL
  _0900 = CUBE_NIL

  _SIDE_RED_OFFSET = 0
  _SIDE_GREEN_OFFSET = 2
  _SIDE_ORANGE_OFFSET = 4
  _SIDE_BLUE_OFFSET = 6

  _SIDE_INDEX_0000 = 0
  _SIDE_INDEX_0130 = 1
  _SIDE_INDEX_0300 = 2
  _SIDE_INDEX_0430 = 3
  _SIDE_INDEX_0600 = 4
  _SIDE_INDEX_0730 = 5
  _SIDE_INDEX_0900 = 6
  _SIDE_INDEX_1030 = 7

  _SIDE_RULE_0000_T = 0
  _SIDE_RULE_0130_T = 7
  _SIDE_RULE_0300_M = 7
  _SIDE_RULE_0430_B = 7
  _SIDE_RULE_0600_B = 0
  _SIDE_RULE_0730_B = 1
  _SIDE_RULE_0900_M = 1
  _SIDE_RULE_1030_T = 1

  _SIDE_WHITE_0000_T = 0
  _SIDE_WHITE_0130_T = 1
  _SIDE_WHITE_0300_T = 2
  _SIDE_WHITE_0430_T = 3
  _SIDE_WHITE_0600_T = 4
  _SIDE_WHITE_0730_T = 5
  _SIDE_WHITE_0900_T = 6
  _SIDE_WHITE_1030_T = 7

  _SIDE_YELLOW_0000_B = 0
  _SIDE_YELLOW_0130_B = 7
  _SIDE_YELLOW_0300_B = 6
  _SIDE_YELLOW_0430_B = 5
  _SIDE_YELLOW_0600_B = 4
  _SIDE_YELLOW_0730_B = 3
  _SIDE_YELLOW_0900_B = 2
  _SIDE_YELLOW_1030_B = 1

  _SIDE_RED_0000_T = 0
  _SIDE_RED_0130_T = 7
  _SIDE_RED_0300_M = 7
  _SIDE_RED_0430_B = 7
  _SIDE_RED_0600_B = 0
  _SIDE_RED_0730_B = 1
  _SIDE_RED_0900_M = 1
  _SIDE_RED_1030_T = 1

  _SIDE_GREEN_0000_T = 2
  _SIDE_GREEN_0130_T = 1
  _SIDE_GREEN_0300_M = 1
  _SIDE_GREEN_0430_B = 1
  _SIDE_GREEN_0600_B = 2
  _SIDE_GREEN_0730_B = 3
  _SIDE_GREEN_0900_M = 3
  _SIDE_GREEN_1030_T = 3

  _SIDE_ORANGE_0000_T = 4
  _SIDE_ORANGE_0130_T = 3
  _SIDE_ORANGE_0300_M = 3
  _SIDE_ORANGE_0430_B = 3
  _SIDE_ORANGE_0600_B = 4
  _SIDE_ORANGE_0730_B = 5
  _SIDE_ORANGE_0900_M = 5
  _SIDE_ORANGE_1030_T = 5

  _SIDE_BLUE_0000_T = 6
  _SIDE_BLUE_0130_T = 5
  _SIDE_BLUE_0300_M = 5
  _SIDE_BLUE_0430_B = 5
  _SIDE_BLUE_0600_B = 6
  _SIDE_BLUE_0730_B = 7
  _SIDE_BLUE_0900_M = 7
  _SIDE_BLUE_1030_T = 7

  _SIDE_WHITE = [ _SIDE_WHITE_0000_T, _SIDE_WHITE_0130_T, _SIDE_WHITE_0300_T, _SIDE_WHITE_0430_T, _SIDE_WHITE_0600_T, _SIDE_WHITE_0730_T, _SIDE_WHITE_0900_T, _SIDE_WHITE_1030_T ]
  _SIDE_YELLOW = [ _SIDE_YELLOW_0000_B, _SIDE_YELLOW_0130_B, _SIDE_YELLOW_0300_B, _SIDE_YELLOW_0430_B, _SIDE_YELLOW_0600_B, _SIDE_YELLOW_0730_B, _SIDE_YELLOW_0900_B, _SIDE_YELLOW_1030_B ]
  _SIDE_RED = [ _SIDE_RED_0000_T, _SIDE_RED_0130_T, _SIDE_RED_0300_M, _SIDE_RED_0430_B, _SIDE_RED_0600_B, _SIDE_RED_0730_B, _SIDE_RED_0900_M, _SIDE_RED_1030_T ]
  _SIDE_GREEN = [ _SIDE_GREEN_0000_T, _SIDE_GREEN_0130_T, _SIDE_GREEN_0300_M, _SIDE_GREEN_0430_B, _SIDE_GREEN_0600_B, _SIDE_GREEN_0730_B, _SIDE_GREEN_0900_M, _SIDE_GREEN_1030_T ]
  _SIDE_ORANGE = [ _SIDE_ORANGE_0000_T, _SIDE_ORANGE_0130_T, _SIDE_ORANGE_0300_M, _SIDE_ORANGE_0430_B, _SIDE_ORANGE_0600_B, _SIDE_ORANGE_0730_B, _SIDE_ORANGE_0900_M, _SIDE_ORANGE_1030_T ]
  _SIDE_BLUE = [ _SIDE_BLUE_0000_T, _SIDE_BLUE_0130_T, _SIDE_BLUE_0300_M, _SIDE_BLUE_0430_B, _SIDE_BLUE_0600_B, _SIDE_BLUE_0730_B, _SIDE_BLUE_0900_M, _SIDE_BLUE_1030_T ]

  _SIDE_INDEX = [ 0, _SIDE_WHITE, _SIDE_YELLOW, _SIDE_RED, _SIDE_GREEN, _SIDE_ORANGE, _SIDE_BLUE ]

  _CUBE_WR = [ CUBE_EDGE, CUBE_WHITE, CUBE_RED, CUBE_WHITE, CUBE_RED, CUBE_ID_SPACER, CUBE_ID_SPACER ]
  _CUBE_WG = [ CUBE_EDGE, CUBE_WHITE, CUBE_GREEN, CUBE_WHITE, CUBE_GREEN, CUBE_ID_SPACER, CUBE_ID_SPACER ]
  _CUBE_WO = [ CUBE_EDGE, CUBE_WHITE, CUBE_ORANGE, CUBE_WHITE, CUBE_ORANGE, CUBE_ID_SPACER, CUBE_ID_SPACER ]
  _CUBE_WB = [ CUBE_EDGE, CUBE_WHITE, CUBE_BLUE, CUBE_WHITE, CUBE_BLUE, CUBE_ID_SPACER, CUBE_ID_SPACER ]
  _CUBE_WRG = [ CUBE_CORNER, CUBE_WHITE, CUBE_RED, CUBE_GREEN, CUBE_WHITE, CUBE_RED, CUBE_GREEN ]
  _CUBE_WGO = [ CUBE_CORNER, CUBE_WHITE, CUBE_GREEN, CUBE_ORANGE, CUBE_WHITE, CUBE_GREEN, CUBE_ORANGE ]
  _CUBE_WOB = [ CUBE_CORNER, CUBE_WHITE, CUBE_ORANGE, CUBE_BLUE, CUBE_WHITE, CUBE_ORANGE, CUBE_BLUE ]
  _CUBE_WBR = [ CUBE_CORNER, CUBE_WHITE, CUBE_BLUE, CUBE_RED, CUBE_WHITE, CUBE_BLUE, CUBE_RED ]

  _CUBE_RG = [ CUBE_EDGE, CUBE_RED, CUBE_GREEN, CUBE_RED, CUBE_GREEN, CUBE_ID_SPACER, CUBE_ID_SPACER ]
  _CUBE_RGM = [ CUBE_EDGE, CUBE_RED, CUBE_GREEN, CUBE_RED, CUBE_GREEN, CUBE_ID_SPACER, CUBE_ID_SPACER ]
  _CUBE_GO = [ CUBE_EDGE, CUBE_GREEN, CUBE_ORANGE, CUBE_GREEN, CUBE_ORANGE, CUBE_ID_SPACER, CUBE_ID_SPACER ]
  _CUBE_GOM = [ CUBE_EDGE, CUBE_GREEN, CUBE_ORANGE, CUBE_GREEN, CUBE_ORANGE, CUBE_ID_SPACER, CUBE_ID_SPACER ]
  _CUBE_OB = [ CUBE_EDGE, CUBE_ORANGE, CUBE_BLUE, CUBE_ORANGE, CUBE_BLUE, CUBE_ID_SPACER, CUBE_ID_SPACER ]
  _CUBE_OBM = [ CUBE_EDGE, CUBE_ORANGE, CUBE_BLUE, CUBE_ORANGE, CUBE_BLUE, CUBE_ID_SPACER, CUBE_ID_SPACER ]
  _CUBE_BR = [ CUBE_EDGE, CUBE_BLUE, CUBE_RED, CUBE_BLUE, CUBE_RED, CUBE_ID_SPACER, CUBE_ID_SPACER ]
  _CUBE_BRM = [ CUBE_EDGE, CUBE_BLUE, CUBE_RED, CUBE_BLUE, CUBE_RED, CUBE_ID_SPACER, CUBE_ID_SPACER ]

  _CUBE_YR = [ CUBE_EDGE, CUBE_YELLOW, CUBE_RED, CUBE_YELLOW, CUBE_RED, CUBE_ID_SPACER, CUBE_ID_SPACER ]
  _CUBE_YG = [ CUBE_EDGE, CUBE_YELLOW, CUBE_GREEN, CUBE_YELLOW, CUBE_GREEN, CUBE_ID_SPACER, CUBE_ID_SPACER ]
  _CUBE_YO = [ CUBE_EDGE, CUBE_YELLOW, CUBE_ORANGE, CUBE_YELLOW, CUBE_ORANGE, CUBE_ID_SPACER, CUBE_ID_SPACER ]
  _CUBE_YB = [ CUBE_EDGE, CUBE_YELLOW, CUBE_BLUE, CUBE_YELLOW, CUBE_BLUE, CUBE_ID_SPACER, CUBE_ID_SPACER ]
  _CUBE_YGR = [ CUBE_CORNER, CUBE_YELLOW, CUBE_GREEN, CUBE_RED, CUBE_YELLOW, CUBE_GREEN, CUBE_RED ]
  _CUBE_YOG = [ CUBE_CORNER, CUBE_YELLOW, CUBE_ORANGE, CUBE_GREEN, CUBE_YELLOW, CUBE_ORANGE, CUBE_GREEN ]
  _CUBE_YBO = [ CUBE_CORNER, CUBE_YELLOW, CUBE_BLUE, CUBE_ORANGE, CUBE_YELLOW, CUBE_BLUE, CUBE_ORANGE ]
  _CUBE_YRB = [ CUBE_CORNER, CUBE_YELLOW, CUBE_RED, CUBE_BLUE, CUBE_YELLOW, CUBE_RED, CUBE_BLUE ]

  _CUBE_WED = [ CUBE_ID, CUBE_WHITE, CUBE_WHITE, CUBE_ID_SPACER, CUBE_ID_SPACER, CUBE_ID_SPACER, CUBE_ID_SPACER ]       # not currently used
  _CUBE_YED = [ CUBE_ID, CUBE_YELLOW, CUBE_YELLOW, CUBE_ID_SPACER, CUBE_ID_SPACER, CUBE_ID_SPACER, CUBE_ID_SPACER ]     # not currently used
  _CUBE_RED = [ CUBE_ID, CUBE_RED, CUBE_RED, CUBE_ID_SPACER, CUBE_ID_SPACER, CUBE_ID_SPACER, CUBE_ID_SPACER ]
  _CUBE_GED = [ CUBE_ID, CUBE_GREEN, CUBE_GREEN, CUBE_ID_SPACER, CUBE_ID_SPACER, CUBE_ID_SPACER, CUBE_ID_SPACER ]
  _CUBE_OED = [ CUBE_ID, CUBE_ORANGE, CUBE_ORANGE,CUBE_ID_SPACER, CUBE_ID_SPACER, CUBE_ID_SPACER, CUBE_ID_SPACER ]
  _CUBE_BED = [ CUBE_ID, CUBE_BLUE, CUBE_BLUE, CUBE_ID_SPACER, CUBE_ID_SPACER, CUBE_ID_SPACER, CUBE_ID_SPACER ]

  _CUBE_NIL = CUBE_NIL

  _cube = [ CUBE_NIL, CUBE_NIL, CUBE_NIL ]
  _cube_solved = [ CUBE_NIL, CUBE_NIL, CUBE_NIL ]

  def __init__( self ) :
    bot = [ RubicsCube._CUBE_YR, RubicsCube._CUBE_YGR, RubicsCube._CUBE_YG, RubicsCube._CUBE_YOG, RubicsCube._CUBE_YO, RubicsCube._CUBE_YBO, RubicsCube._CUBE_YB, RubicsCube._CUBE_YRB ]
    mid = [ RubicsCube._CUBE_RED, RubicsCube._CUBE_RGM, RubicsCube._CUBE_GED, RubicsCube._CUBE_GOM, RubicsCube._CUBE_OED, RubicsCube._CUBE_OBM, RubicsCube._CUBE_BED, RubicsCube._CUBE_BRM ] 
    top    = [ RubicsCube._CUBE_WR, RubicsCube._CUBE_WRG, RubicsCube._CUBE_WG, RubicsCube._CUBE_WGO, RubicsCube._CUBE_WO, RubicsCube._CUBE_WOB, RubicsCube._CUBE_WB, RubicsCube._CUBE_WBR ] 

    self._cube[ CUBE_TOP ] = copy.deepcopy( top )
    self._cube[ CUBE_MIDDLE ] = copy.deepcopy( mid )
    self._cube[ CUBE_BOTTOM ] = copy.deepcopy( bot )

    self._cube_solved = copy.deepcopy( self._cube )

  def _side_get( self, side_id_P ) :
    top = self._cube[ CUBE_TOP ]
    mid = self._cube[ CUBE_MIDDLE ]
    bot = self._cube[ CUBE_BOTTOM ]

    side = [ CUBE_NIL, CUBE_NIL, CUBE_NIL, CUBE_NIL, CUBE_NIL, CUBE_NIL, CUBE_NIL, CUBE_NIL ]

    if side_id_P == CUBE_WHITE :
      mid = top
      bot = top

    elif side_id_P == CUBE_YELLOW :
      top = bot
      mid = bot

    side[ RubicsCube._SIDE_INDEX_0000 ] = copy.deepcopy( top[ RubicsCube._SIDE_INDEX[ side_id_P ][RubicsCube._SIDE_INDEX_0000 ]] )
    side[ RubicsCube._SIDE_INDEX_0130 ] = copy.deepcopy( top[ RubicsCube._SIDE_INDEX[ side_id_P ][RubicsCube._SIDE_INDEX_0130 ]] )
    side[ RubicsCube._SIDE_INDEX_0300 ] = copy.deepcopy( mid[ RubicsCube._SIDE_INDEX[ side_id_P ][RubicsCube._SIDE_INDEX_0300 ]] )
    side[ RubicsCube._SIDE_INDEX_0430 ] = copy.deepcopy( bot[ RubicsCube._SIDE_INDEX[ side_id_P ][RubicsCube._SIDE_INDEX_0430 ]] )
    side[ RubicsCube._SIDE_INDEX_0600 ] = copy.deepcopy( bot[ RubicsCube._SIDE_INDEX[ side_id_P ][RubicsCube._SIDE_INDEX_0600 ]] )
    side[ RubicsCube._SIDE_INDEX_0730 ] = copy.deepcopy( bot[ RubicsCube._SIDE_INDEX[ side_id_P ][RubicsCube._SIDE_INDEX_0730 ]] )
    side[ RubicsCube._SIDE_INDEX_0900 ] = copy.deepcopy( mid[ RubicsCube._SIDE_INDEX[ side_id_P ][RubicsCube._SIDE_INDEX_0900 ]] )
    side[ RubicsCube._SIDE_INDEX_1030 ] = copy.deepcopy( top[ RubicsCube._SIDE_INDEX[ side_id_P ][RubicsCube._SIDE_INDEX_1030 ]] )
    
    return side

  def _side_put( self, side_id_P, side_P ) :
    top_id = CUBE_TOP
    mid_id = CUBE_MIDDLE
    bot_id = CUBE_BOTTOM

    if side_id_P == CUBE_WHITE :
      mid_id = CUBE_TOP
      bot_id = CUBE_TOP

    if side_id_P == CUBE_YELLOW :
      top_id = CUBE_BOTTOM
      mid_id = CUBE_BOTTOM

    self._cube[ top_id ][ RubicsCube._SIDE_INDEX[ side_id_P ][ RubicsCube._SIDE_INDEX_0000 ]] = copy.deepcopy( side_P[ RubicsCube._SIDE_INDEX_0000 ] )
    self._cube[ top_id ][ RubicsCube._SIDE_INDEX[ side_id_P ][ RubicsCube._SIDE_INDEX_0130 ]] = copy.deepcopy( side_P[ RubicsCube._SIDE_INDEX_0130 ] )
    self._cube[ mid_id ][ RubicsCube._SIDE_INDEX[ side_id_P ][ RubicsCube._SIDE_INDEX_0300 ]] = copy.deepcopy( side_P[ RubicsCube._SIDE_INDEX_0300 ] )
    self._cube[ bot_id ][ RubicsCube._SIDE_INDEX[ side_id_P ][ RubicsCube._SIDE_INDEX_0430 ]] = copy.deepcopy( side_P[ RubicsCube._SIDE_INDEX_0430 ] )
    self._cube[ bot_id ][ RubicsCube._SIDE_INDEX[ side_id_P ][ RubicsCube._SIDE_INDEX_0600 ]] = copy.deepcopy( side_P[ RubicsCube._SIDE_INDEX_0600 ] )
    self._cube[ bot_id ][ RubicsCube._SIDE_INDEX[ side_id_P ][ RubicsCube._SIDE_INDEX_0730 ]] = copy.deepcopy( side_P[ RubicsCube._SIDE_INDEX_0730 ] )
    self._cube[ mid_id ][ RubicsCube._SIDE_INDEX[ side_id_P ][ RubicsCube._SIDE_INDEX_0900 ]] = copy.deepcopy( side_P[ RubicsCube._SIDE_INDEX_0900 ] )
    self._cube[ top_id ][ RubicsCube._SIDE_INDEX[ side_id_P ][ RubicsCube._SIDE_INDEX_1030 ]] = copy.deepcopy( side_P[ RubicsCube._SIDE_INDEX_1030 ] )

  def _side_edge_color_get( self, side_id_P, side_P, side_index_P ) :
    if side_id_P == side_P[ side_index_P ][ CUBE_EDGE_FACE_0 ] :
      return side_P[ side_index_P ][ CUBE_EDGE_0 ]

    elif side_id_P == side_P[ side_index_P ][ CUBE_EDGE_FACE_1 ] :
      return side_P[ side_index_P ][ CUBE_EDGE_1 ]

    else :
      print( "illegal edge face", side_id_P, __FILE__(), "@", __LINE__ )
      exit()

  def _side_corner_color_get( self, side_id_P, side_P, side_index_P ) :
    if side_id_P == side_P[ side_index_P ][ CUBE_CORNER_FACE_0 ] :
      return side_P[ side_index_P ][ CUBE_CORNER_0 ]

    elif side_id_P == side_P[ side_index_P ][ CUBE_CORNER_FACE_1 ] :
      return side_P[ side_index_P ][ CUBE_CORNER_1 ]

    elif side_id_P == side_P[ side_index_P ][ CUBE_CORNER_FACE_2 ] :
      return side_P[ side_index_P ][ CUBE_CORNER_2 ]

    else :
      print( "illegal corner face", side_id_P, __FILE__(), "@", __LINE__ )
      exit()

  def _side_edge_white( self, direction_P, face_color_P ) :
    if direction_P == ROTATE_CLOCKWISE :
      if face_color_P == CUBE_RED :
        return CUBE_GREEN

      elif face_color_P == CUBE_GREEN :
        return CUBE_ORANGE

      elif face_color_P == CUBE_ORANGE :
        return CUBE_BLUE

      elif face_color_P == CUBE_BLUE :
        return CUBE_RED

      else :
        print( "illegal face", __FILE__(), "@", __LINE__ )
        exit()

    else :
      if face_color_P == CUBE_RED :
        return CUBE_BLUE

      elif face_color_P == CUBE_BLUE :
        return CUBE_ORANGE

      elif face_color_P == CUBE_ORANGE :
        return CUBE_GREEN

      elif face_color_P == CUBE_GREEN :
        return CUBE_RED

      else :
        print( "illegal face", __FILE__(), "@", __LINE__ )
        exit()

  def _side_edge_yellow( self, direction_P, face_color_P ) :
    diretion = direction_P
    if direction_P == ROTATE_CLOCKWISE :
      direction = ROTATE_COUNTER

    else :
      direction = ROTATE_CLOCKWISE

    return self._side_edge_white( direction, face_color_P )

  def _side_edge_red( self, direction_P, face_color_P ) :
    print( "_side_edge_red", direction_P, face_color_P )
    if direction_P == ROTATE_CLOCKWISE :
      if face_color_P == CUBE_WHITE :
        return CUBE_BLUE

      elif face_color_P == CUBE_BLUE :
        return CUBE_YELLOW

      elif face_color_P == CUBE_YELLOW :
        return CUBE_GREEN

      elif face_color_P == CUBE_GREEN :
        return CUBE_WHITE

      else :
        print( "illegal face", face_color_P, __FILE__(), "@", __LINE__ )
        exit()

    else :
      if face_color_P == CUBE_WHITE :
        return CUBE_GREEN

      elif face_color_P == CUBE_GREEN :
        return CUBE_YELLOW

      elif face_color_P == CUBE_YELLOW :
        return CUBE_BLUE

      elif face_color_P == CUBE_BLUE :
        return CUBE_WHITE

      else :
        print( "illegal face", face_color_P, __FILE__(), "@", __LINE__ )
        exit()

  def _side_edge_orange( self, direction_P, face_color_P ) :
    diretion = direction_P
    if direction_P == ROTATE_CLOCKWISE :
      direction = ROTATE_COUNTER

    else :
      direction = ROTATE_CLOCKWISE

    return self._side_edge_red( direction, face_color_P )

  def _side_edge_green( self, direction_P, face_color_P ) :
    if direction_P == ROTATE_CLOCKWISE :
      if face_color_P == CUBE_WHITE :
        return CUBE_RED

      elif face_color_P == CUBE_RED :
        return CUBE_YELLOW

      elif face_color_P == CUBE_YELLOW :
        return CUBE_ORANGE

      elif face_color_P == CUBE_ORANGE :
        return CUBE_WHITE

      else :
        print( "illegal face", __FILE__(), "@", __LINE__ )
        exit()

    else :
      if face_color_P == CUBE_WHITE :
        return CUBE_ORANGE

      elif face_color_P == CUBE_ORANGE :
        return CUBE_YELLOW

      elif face_color_P == CUBE_YELLOW :
        return CUBE_RED

      elif face_color_P == CUBE_RED :
        return CUBE_WHITE

      else :
        print( "illegal face", __FILE__(), "@", __LINE__ )
        exit()

  def _side_edge_blue( self, direction_P, face_color_P ) :
    diretion = direction_P
    if direction_P == ROTATE_CLOCKWISE :
      direction = ROTATE_COUNTER

    else :
      direction = ROTATE_CLOCKWISE

    return self._side_edge_green( direction, face_color_P )

  def _side_edge_face_get( self, direction_P, side_id_P, face_color_P ) :
    if side_id_P == CUBE_WHITE :
      return self._side_edge_white( direction_P, face_color_P )

    elif side_id_P == CUBE_YELLOW :
      return self._side_edge_yellow( direction_P, face_color_P )

    elif side_id_P == CUBE_RED :
      return self._side_edge_red( direction_P, face_color_P )

    elif side_id_P == CUBE_GREEN :
      return self._side_edge_green( direction_P, face_color_P )

    elif side_id_P == CUBE_ORANGE :
      return self._side_edge_orange( direction_P, face_color_P )

    elif side_id_P == CUBE_BLUE :
      return self._side_edge_blue( direction_P, face_color_P )

    else :
      print( "illegal side", "d", direction_P, "s", side_id_P, "f", face_color_P, __FILE__(), "@", __LINE__ )
      exit()

  def _side_deepcopy( self, side_P ) :
    self._1030 = copy.deepcopy( side_P[ RubicsCube._SIDE_INDEX_1030 ] )
    self._0000 = copy.deepcopy( side_P[ RubicsCube._SIDE_INDEX_0000 ] )
    self._0130 = copy.deepcopy( side_P[ RubicsCube._SIDE_INDEX_0130 ] )
    self._0300 = copy.deepcopy( side_P[ RubicsCube._SIDE_INDEX_0300 ] )
    self._0430 = copy.deepcopy( side_P[ RubicsCube._SIDE_INDEX_0430 ] )
    self._0600 = copy.deepcopy( side_P[ RubicsCube._SIDE_INDEX_0600 ] )
    self._0730 = copy.deepcopy( side_P[ RubicsCube._SIDE_INDEX_0730 ] )
    self._0900 = copy.deepcopy( side_P[ RubicsCube._SIDE_INDEX_0900 ] )

  def _rotate_face_edge_plus_cube_delay( self, cell_P, edge_P, edge_cell_P, edge_face_P ) :
    if cell_P[ CUBE_CORNER_FACE_0 ] == edge_P :
      cell_P[ CUBE_CORNER_FACE_0 ] = edge_cell_P[ edge_face_P ] + CUBE_DELAY

    elif cell_P[ CUBE_CORNER_FACE_1 ] == edge_P :
      cell_P[ CUBE_CORNER_FACE_1 ] = edge_cell_P[ edge_face_P ] + CUBE_DELAY

    elif cell_P[ CUBE_CORNER_FACE_2 ] == edge_P :
      cell_P[ CUBE_CORNER_FACE_2 ] = edge_cell_P[ edge_face_P ] + CUBE_DELAY

  def _rotate_face_edge( self, side_id_P, direction_P, corner_left_P, edge_P, corner_right_P ) :
    if( DEBUG_ROTATE_FACES == 1 ) :
      print( "\n\tcorner left", corner_left_P, "0000 middle", edge_P, "corner right", corner_right_P )

    if edge_P[ CUBE_EDGE_FACE_0 ] == side_id_P :
      edge = copy.deepcopy( edge_P[ CUBE_EDGE_FACE_1 ] )
      edge_P[ CUBE_EDGE_FACE_1 ] = self._side_edge_face_get( direction_P, side_id_P, edge_P[ CUBE_EDGE_FACE_1 ] )

      if( DEBUG_ROTATE_FACES == 1 ) :
        print( "edge", edge, edge_P[ CUBE_EDGE_FACE_1 ] )

      self._rotate_face_edge_plus_cube_delay( corner_left_P, edge, edge_P, CUBE_EDGE_FACE_1 )
      self._rotate_face_edge_plus_cube_delay( corner_right_P, edge, edge_P, CUBE_EDGE_FACE_1 )

    elif edge_P[ CUBE_EDGE_FACE_1 ] == side_id_P :
      edge = copy.deepcopy( edge_P[ CUBE_EDGE_FACE_0 ] )
      edge_P[ CUBE_EDGE_FACE_0 ] = self._side_edge_face_get( direction_P, side_id_P, edge_P[ CUBE_EDGE_FACE_0 ] )

      if( DEBUG_ROTATE_FACES == 1 ) :
        print( "edge", edge, edge_P[ CUBE_EDGE_FACE_0 ] )

      self._rotate_face_edge_plus_cube_delay( corner_left_P, edge, edge_P, CUBE_EDGE_FACE_0 )
      self._rotate_face_edge_plus_cube_delay( corner_right_P, edge, edge_P, CUBE_EDGE_FACE_0 )

    if( DEBUG_ROTATE_FACES == 1 ) :
      print( "\tcorner left", corner_left_P, "edge mid", edge_P, "corner right", corner_right_P, "}" )

  def _face_minus_cube_delay_face( self, cell_P, face_P ) :
    if cell_P[ face_P ] > CUBE_BLUE :
      cell_P[ face_P ] = cell_P[ face_P ] - CUBE_DELAY

  def _face_minus_cube_delay( self, cell_P ) :
    self._face_minus_cube_delay_face( cell_P, CUBE_CORNER_FACE_0 )
    self._face_minus_cube_delay_face( cell_P, CUBE_CORNER_FACE_1 )
    self._face_minus_cube_delay_face( cell_P, CUBE_CORNER_FACE_2 )

  def _side_assign( self, side_P, _0000_P, _0300_P, _0600_P, _0900_P, _0130_P, _0430_P, _0730_P, _1030_P ) :
    side_P[ RubicsCube._SIDE_INDEX_0000 ] = _0000_P
    side_P[ RubicsCube._SIDE_INDEX_0300 ] = _0300_P
    side_P[ RubicsCube._SIDE_INDEX_0600 ] = _0600_P
    side_P[ RubicsCube._SIDE_INDEX_0900 ] = _0900_P

    side_P[ RubicsCube._SIDE_INDEX_0130 ] = _0130_P
    side_P[ RubicsCube._SIDE_INDEX_0430 ] = _0430_P
    side_P[ RubicsCube._SIDE_INDEX_0730 ] = _0730_P
    side_P[ RubicsCube._SIDE_INDEX_1030 ] = _1030_P

  def _rotate_faces( self, direction_P, side_id_P, side_P ) :
    self._side_deepcopy( side_P )

    edge = 0
    
  # 0000 EDGE
    self._rotate_face_edge( side_id_P, direction_P, self._1030, self._0000, self._0130 )
  # 0300 EDGE
    self._rotate_face_edge( side_id_P, direction_P, self._0130, self._0300, self._0430 )
  # 0600 EDGE
    self._rotate_face_edge( side_id_P, direction_P, self._0430, self._0600, self._0730 )
  # 0900 EDGE
    self._rotate_face_edge( side_id_P, direction_P, self._0730, self._0900, self._1030 )

    self._face_minus_cube_delay( self._1030 )
    self._face_minus_cube_delay( self._0130 )
    self._face_minus_cube_delay( self._0430 )
    self._face_minus_cube_delay( self._0730 )

    if( DEBUG_ROTATE_FACES == 1 ) :
      print( "\tTOP:    ", self._1030, self._0000, self._0130 )
      print( "\tMIDDLE: ", self._0900, side_id_P, self._0300 )
      print( "\tBOTTOM: ", self._0730, self._0600, self._0430 )

    self._side_assign( side_P, self._0000, self._0300, self._0600, self._0900, self._0130, self._0430, self._0730, self._1030 )

    if( DEBUG_ROTATE_FACES == 1 ) :
      print( "\n" )
      print( "\tTOP:    ", side_P[ RubicsCube._SIDE_INDEX_1030 ], side_P[ RubicsCube._SIDE_INDEX_0000 ], side_P[ RubicsCube._SIDE_INDEX_0130 ] )
      print( "\tMIDDLE: ", side_P[ RubicsCube._SIDE_INDEX_0900 ], "[ . . . . . , ]", side_id_P, side_P[ RubicsCube._SIDE_INDEX_0300 ] )
      print( "\tBOTTOM: ", side_P[ RubicsCube._SIDE_INDEX_0730 ], side_P[ RubicsCube._SIDE_INDEX_0600 ], side_P[ RubicsCube._SIDE_INDEX_0430 ] )

  def _rotate_colors( self, direction_P, side_id_P, side_P ) :
    self._side_deepcopy( side_P )

    if DEBUG_ROTATE == 1 :
      print( "0000", self._0000, "0300", self._0300, "0600", self._0600, "0900", self._0900 )
      print( "1030", self._1030, "0130", self._0130, "0430", self._0430, "0730", self._0730 )

    if direction_P == ROTATE_CLOCKWISE :
      if DEBUG_ROTATE == 1 :
        print( "CLOCKWISE" )

      self._side_assign( side_P, self._0900, self._0000, self._0300, self._0600, self._1030, self._0130, self._0430, self._0730 )

    else :
      if DEBUG_ROTATE == 1 :
        print( "COUNTER" )

      self._side_assign( side_P, self._0300, self._0600, self._0900, self._0000, self._0430, self._0730, self._1030, self._0130 )

  def RotateSide( self, side_id_P, direction_P ) :
    if DEBUG_ROTATE == 1 :
      print( "RotateSide {" )

    side = self._side_get( side_id_P )

    self._rotate_faces( direction_P, side_id_P, side ) 
    self._rotate_colors( direction_P, side_id_P, side )

    self._side_put( side_id_P, side )

    if DEBUG_ROTATE == 1 :
      print( "RotateSide }" )

  def _debug_cube( self, flag_P, msg_P, side_id_P ) :
    if flag_P == DEBUG_CUBE and ( side_id_P == CUBE_CUBE ) :
      if msg_P != "" :
        print( msg_P )

      print( "top:,", self._cube[ CUBE_TOP ] )
      print( "mid:,", self._cube[ CUBE_MIDDLE ] )
      print( "bot:,", self._cube[ CUBE_BOTTOM ] )

    elif flag_P == DEBUG_CUBE and ( side_id_P <= CUBE_BLUE ) :
      print( msg_P, ",", self._side_get( side_id_P ))

  def PrintSide( self, flag_P, side_id_P ) :
    side = self._side_get( side_id_P )

    if DEBUG_PRINTSIDE == 1 :
      print( "PrintSide {", "flag_P == ", flag_P, "side_id_P == ", side_id_P )
      print( side )

    if flag_P == PRINT_SIDE_LABEL :
      if side_id_P == CUBE_WHITE :
        print( "\nWHITE SIDE %d" % CUBE_WHITE )

      elif side_id_P == CUBE_YELLOW :
        print( "\nYELLOW SIDE %d" % CUBE_YELLOW )

      elif side_id_P == CUBE_RED :
        print( "\nRED SIDE %d" % CUBE_RED )

      elif side_id_P == CUBE_GREEN :
        print( "\nGREEN SIDE %d" % CUBE_GREEN )

      elif side_id_P == CUBE_ORANGE :
        print( "\nORANGE SIDE %d" % CUBE_ORANGE )

      elif side_id_P == CUBE_BLUE :
        print( "\nBLUE SIDE %d" % CUBE_BLUE )

      else :
        print( "ERROR: invalid side", __FILE__(), " @ ", __LINE__ )
        exit()

    face_1030 = self._side_corner_color_get( side_id_P, side, RubicsCube._SIDE_INDEX_1030 )
    face_0000 = self._side_edge_color_get( side_id_P, side, RubicsCube._SIDE_INDEX_0000 )
    face_0130 = self._side_corner_color_get( side_id_P, side, RubicsCube._SIDE_INDEX_0130 )
    face_0300 = self._side_edge_color_get( side_id_P, side, RubicsCube._SIDE_INDEX_0300 )
    face_0430 = self._side_corner_color_get( side_id_P, side, RubicsCube._SIDE_INDEX_0430 )
    face_0600 = self._side_edge_color_get( side_id_P, side, RubicsCube._SIDE_INDEX_0600 )
    face_0730 = self._side_corner_color_get( side_id_P, side, RubicsCube._SIDE_INDEX_0730 )
    face_0900 = self._side_edge_color_get( side_id_P, side, RubicsCube._SIDE_INDEX_0900 )
    
    print( "  -------------" )
    print( "  |" , face_1030, "|", face_0000, "|", face_0130, "|" )
    print( "  -------------", )
    print( "  |" , face_0900, "|", side_id_P, "|", face_0300, "|" )
    print( "  -------------", )
    print( "  |" , face_0730, "|", face_0600, "|", face_0430, "|" )
    print( "  -------------\n" )

  def DebugCube( self, msg_P ) :
    self._debug_cube( 1, msg_P, CUBE_CUBE )

  def _test_resolve_msg( self, flag_P, side_id_P, status_P ) :
    if flag_P == TEST_ROTATE_BACK :
      if status_P == 1 :
        print( "**** SOLVED **** [", side_id_P, "]" )

      else :
        print( "** NOT SOLVED ** [", side_id_P, "]" )
        exit()

  def _test_resolve( self, flag_P, side_id_P ) :
    if side_id_P == CUBE_WHITE and TEST_ROTATE_NO_WHITE == 0 :
      return 0
      
    if side_id_P == CUBE_YELLOW and TEST_ROTATE_NO_YELLOW == 0 :
      return 0
      
    if side_id_P == CUBE_RED and TEST_ROTATE_NO_RED == 0 :
      return 0
      
    if side_id_P == CUBE_GREEN and TEST_ROTATE_NO_GREEN == 0 :
      return 0
      
    if side_id_P == CUBE_ORANGE and TEST_ROTATE_NO_ORANGE == 0 :
      return 0
      
    if side_id_P == CUBE_BLUE and TEST_ROTATE_NO_BLUE == 0 :
      return 0

    return 1

  def TestRotate( self, flag_P, msg_P, side_id_P, direction_P, iterations_P ) :
    if DEBUG_TEST_ROTATE == 1 :
      print( "TestRotate", flag_P, msg_P, side_id_P, direction_P, iterations_P )
      self.DebugCube( msg_P + "{" )

    for x in range( 0, iterations_P ) :
      self.RotateSide( side_id_P, direction_P )

    solved_missing_1 = CUBE_ID
    solved_missing_2 = CUBE_ID

    if side_id_P == CUBE_WHITE or side_id_P == CUBE_YELLOW :
      self.PrintSide( PRINT_SIDE_LABEL, CUBE_RED )
      self.PrintSide( PRINT_SIDE_LABEL, CUBE_GREEN )
      self.PrintSide( PRINT_SIDE_LABEL, CUBE_ORANGE )
      self.PrintSide( PRINT_SIDE_LABEL, CUBE_BLUE )

      solved_missing_1 = CUBE_WHITE
      solved_missing_2 = CUBE_YELLOW

    else :
      self.PrintSide( PRINT_SIDE_LABEL, CUBE_WHITE )
      self.PrintSide( PRINT_SIDE_LABEL, CUBE_YELLOW )

      if side_id_P == CUBE_RED :
        self.PrintSide( PRINT_SIDE_LABEL, CUBE_GREEN )
        self.PrintSide( PRINT_SIDE_LABEL, CUBE_BLUE )

        solved_missing_1 = CUBE_RED
        solved_missing_2 = CUBE_ORANGE

      elif side_id_P == CUBE_GREEN :
        self.PrintSide( PRINT_SIDE_LABEL, CUBE_RED )
        self.PrintSide( PRINT_SIDE_LABEL, CUBE_ORANGE )

        solved_missing_1 = CUBE_GREEN
        solved_missing_2 = CUBE_BLUE

      elif side_id_P == CUBE_ORANGE :
        self.PrintSide( PRINT_SIDE_LABEL, CUBE_GREEN )
        self.PrintSide( PRINT_SIDE_LABEL, CUBE_BLUE )

        solved_missing_1 = CUBE_RED
        solved_missing_2 = CUBE_ORANGE

      else :
        self.PrintSide( PRINT_SIDE_LABEL, CUBE_ORANGE )
        self.PrintSide( PRINT_SIDE_LABEL, CUBE_RED )

        solved_missing_1 = CUBE_GREEN
        solved_missing_2 = CUBE_BLUE

    if flag_P == TEST_ROTATE_BACK :
      if solved_missing_1 != CUBE_ID :
        self.PrintSide( PRINT_SIDE_LABEL, solved_missing_1 )

      if solved_missing_2 != CUBE_ID :
        self.PrintSide( PRINT_SIDE_LABEL, solved_missing_2 )

    close = "}"
    if flag_P == TEST_ROTATE_BACK :
      close = "} back to solved."

    self.DebugCube( msg_P + close )

    self._test_resolve_msg( flag_P, side_id_P, self._cube == self._cube_solved )

  def PrintCube( self ) :
    self.PrintSide( PRINT_SIDE_LABEL, CUBE_WHITE )
    self.PrintSide( PRINT_SIDE_LABEL, CUBE_YELLOW )
    self.PrintSide( PRINT_SIDE_LABEL, CUBE_RED )
    self.PrintSide( PRINT_SIDE_LABEL, CUBE_GREEN )
    self.PrintSide( PRINT_SIDE_LABEL, CUBE_ORANGE )
    self.PrintSide( PRINT_SIDE_LABEL, CUBE_BLUE )

  def _y_permutator_core( self, side_id_1_P, side_id_2_P, rotate_bracket_P, rotate_mid_P ) :
    self.RotateSide( side_id_1_P, rotate_bracket_P )
    self.RotateSide( side_id_2_P, rotate_mid_P )
    self.RotateSide( side_id_1_P, rotate_mid_P )
    self.RotateSide( side_id_2_P, rotate_bracket_P )

  def _y_permutator_clockwise( self, side_id_1_P, side_id_2_P ) :
    self._y_permutator_core( self, side_id_1_P, side_id_2_P, ROTATE_CLOCKWISE, ROTATE_COUNTER )

  def _y_permutator_counter( self, side_id_1_P, side_id_2_P ) :
    self._y_permutator_core( self, side_id_1_P, side_id_2_P, ROTATE_COUNTER, ROTATE_CLOCKWISE )

  def Y_Permutator( self, side_id_1_P, side_id_2_P, side_id_orientation_P ) :
    if side_id_1_P == CUBE_WHITE :
      if side_id_2_P == CUBE_YELLOW :
        print( "invalid side_2 for Y_Permutator", __LINE__ )
        exit()

      if side_id_orientation_P == CUBE_RED :
        if side_id_2_P == CUBE_GREEN :
          self._y_permutator_clockwise( CUBE_WHITE, CUBE_GREEN )

        elif side_id_2_P == CUBE_BLUE :
          self._y_permutator_counter( CUBE_WHITE, CUBE_BLUE )

        else :
          print( "invalid side_2 match, should be RED or BLUE was %d", side_id_2_P )
          exit()

      elif side_id_orientation_P == CUBE_GREEN :
        if side_id_2_P == CUBE_ORANGE :
          self._y_permutator_clockwise( CUBE_WHITE, CUBE_ORANGE )

        elif side_id_2_P == CUBE_RED :
          self._y_permutator_counter( CUBE_WHITE, CUBE_RED )

        else :
          print( "invalid side_2 match, should be RED or BLUE was %d", side_id_2_P )
          exit()

      elif side_id_orientation_P == CUBE_ORANGE :
        if side_id_2_P == CUBE_BLUE :
          self._y_permutator_clockwise( CUBE_WHITE, CUBE_BLUE )

        elif side_id_2_P == CUBE_GREEN :
          self._y_permutator_counter( CUBE_WHITE, CUBE_GREEN )

        else :
          print( "invalid side_2 match, should be RED or BLUE was %d", side_id_2_P )
          exit()

      elif side_id_orientation_P == CUBE_BLUE :
        if side_id_2_P == CUBE_RED :
          self._y_permutator_clockwise( CUBE_WHITE, CUBE_RED )

        elif side_id_2_P == CUBE_ORANGE :
          self._y_permutator_counter( CUBE_WHITE, CUBE_ORANGE )

        else :
          print( "invalid side_2 match, should be RED or BLUE was %d", side_id_2_P )
          exit()

      else :
        print( "invalid orientation for Y_Permutator", __LINE__ )


  def TestRotateRandom( self ) :
    rotation_list = [ -1 ] 

    j = random.randrange( 1, TEST_ROTATE_RANDOM_ITERATIONS_2, 1 )

    for i in range( 0, j ) :
      side_id = random.randrange( CUBE_WHITE, CUBE_BLUE + 1, 1 ) 
      direction = random.randrange( ROTATE_CLOCKWISE, ROTATE_COUNTER + 1, 1 ) 
      count = random.randrange( 0, 4 + 1, 1 ) 

      rotation_list.append( count )
      rotation_list.append( direction )
      rotation_list.append( side_id )

      self.TestRotate( TEST_ROTATE, "Random Wind", side_id, direction, count )

    rotate_list_cursor = len( rotation_list ) - 1
    for i in range( 0, j ) :
      side_id = rotation_list[ rotate_list_cursor ] 
      rotate_list_cursor -= 1

      direction = rotation_list[ rotate_list_cursor ] 
      rotate_list_cursor -= 1

      if direction == ROTATE_CLOCKWISE :
        direction = ROTATE_COUNTER
      else :
        direction = ROTATE_CLOCKWISE

      count = rotation_list[ rotate_list_cursor ] 
      rotate_list_cursor -= 1

      self.TestRotate( TEST_ROTATE, "Random Unwind", side_id, direction, count )

    return j

cube = RubicsCube()

print( "BEG TEST {" )
cube.PrintCube()

cube.TestRotate( TEST_ROTATE, "WHITE => ROTATE_CLOCKWISE", CUBE_WHITE, ROTATE_CLOCKWISE, 1 )
cube.TestRotate( TEST_ROTATE, "WHITE => ROTATE_CLOCKWISE", CUBE_WHITE, ROTATE_CLOCKWISE, TEST_ROTATE_BACK )
cube.TestRotate( TEST_ROTATE, "WHITE => ROTATE_CLOCKWISE", CUBE_WHITE, ROTATE_CLOCKWISE, 3 )
cube.TestRotate( TEST_ROTATE, "WHITE => ROTATE_CLOCKWISE", CUBE_WHITE, ROTATE_CLOCKWISE, 4 )
cube.TestRotate( TEST_ROTATE_BACK, "WHITE => ROTATE_CLOCKWISE", CUBE_WHITE, ROTATE_CLOCKWISE, 2 ) # back to solved

cube.TestRotate( TEST_ROTATE, "YELLOW => ROTATE_CLOCKWISE", CUBE_YELLOW, ROTATE_CLOCKWISE, 1 )
cube.TestRotate( TEST_ROTATE, "YELLOW => ROTATE_CLOCKWISE", CUBE_YELLOW, ROTATE_CLOCKWISE, TEST_ROTATE_BACK )
cube.TestRotate( TEST_ROTATE, "YELLOW => ROTATE_CLOCKWISE", CUBE_YELLOW, ROTATE_CLOCKWISE, 3 )
cube.TestRotate( TEST_ROTATE, "YELLOW => ROTATE_CLOCKWISE", CUBE_YELLOW, ROTATE_CLOCKWISE, 4 )
cube.TestRotate( TEST_ROTATE_BACK, "YELLOW => ROTATE_CLOCKWISE", CUBE_YELLOW, ROTATE_CLOCKWISE, 2 ) # back to solved

cube.TestRotate( TEST_ROTATE, "RED => ROTATE_CLOCKWISE", CUBE_RED, ROTATE_CLOCKWISE, 1 )
cube.TestRotate( TEST_ROTATE, "RED => ROTATE_CLOCKWISE", CUBE_RED, ROTATE_CLOCKWISE, TEST_ROTATE_BACK )
cube.TestRotate( TEST_ROTATE, "RED => ROTATE_CLOCKWISE", CUBE_RED, ROTATE_CLOCKWISE, 3 )
cube.TestRotate( TEST_ROTATE, "RED => ROTATE_CLOCKWISE", CUBE_RED, ROTATE_CLOCKWISE, 4 )
cube.TestRotate( TEST_ROTATE_BACK, "RED => ROTATE_CLOCKWISE", CUBE_RED, ROTATE_CLOCKWISE, 2 ) # back to solved

cube.TestRotate( TEST_ROTATE, "ORANGE => ROTATE_CLOCKWISE", CUBE_ORANGE, ROTATE_CLOCKWISE, 1 )
cube.TestRotate( TEST_ROTATE, "ORANGE => ROTATE_CLOCKWISE", CUBE_ORANGE, ROTATE_CLOCKWISE, TEST_ROTATE_BACK )
cube.TestRotate( TEST_ROTATE, "ORANGE => ROTATE_CLOCKWISE", CUBE_ORANGE, ROTATE_CLOCKWISE, 3 )
cube.TestRotate( TEST_ROTATE, "ORANGE => ROTATE_CLOCKWISE", CUBE_ORANGE, ROTATE_CLOCKWISE, 4 )
cube.TestRotate( TEST_ROTATE_BACK, "ORANGE => ROTATE_CLOCKWISE", CUBE_ORANGE, ROTATE_CLOCKWISE, 2 ) # back to solved

cube.TestRotate( TEST_ROTATE, "GREEN => ROTATE_CLOCKWISE", CUBE_GREEN, ROTATE_CLOCKWISE, 1 )
cube.TestRotate( TEST_ROTATE, "GREEN => ROTATE_CLOCKWISE", CUBE_GREEN, ROTATE_CLOCKWISE, TEST_ROTATE_BACK )
cube.TestRotate( TEST_ROTATE, "GREEN => ROTATE_CLOCKWISE", CUBE_GREEN, ROTATE_CLOCKWISE, 3 )
cube.TestRotate( TEST_ROTATE, "GREEN => ROTATE_CLOCKWISE", CUBE_GREEN, ROTATE_CLOCKWISE, 4 )
cube.TestRotate( TEST_ROTATE_BACK, "GREEN => ROTATE_CLOCKWISE", CUBE_GREEN, ROTATE_CLOCKWISE, 2 ) # back to solved

cube.TestRotate( TEST_ROTATE, "BLUE => ROTATE_CLOCKWISE", CUBE_BLUE, ROTATE_CLOCKWISE, 1 )
cube.TestRotate( TEST_ROTATE, "BLUE => ROTATE_CLOCKWISE", CUBE_BLUE, ROTATE_CLOCKWISE, TEST_ROTATE_BACK )
cube.TestRotate( TEST_ROTATE, "BLUE => ROTATE_CLOCKWISE", CUBE_BLUE, ROTATE_CLOCKWISE, 3 )
cube.TestRotate( TEST_ROTATE, "BLUE => ROTATE_CLOCKWISE", CUBE_BLUE, ROTATE_CLOCKWISE, 4 )
cube.TestRotate( TEST_ROTATE_BACK, "BLUE => ROTATE_CLOCKWISE", CUBE_BLUE, ROTATE_CLOCKWISE, 2 ) # back to solved

print( "START OF MUTLI SIDE ROTATIONS" )
iterations_total = 0
for y in range( 0, TEST_ROTATE_RANDOM_ITERATIONS_1 ) :
  for x in range( CUBE_WHITE, CUBE_BLUE + 1 ) :
    iterations = cube.TestRotateRandom() 
    iterations_total += iterations
    print( iterations )

cube.PrintCube()
if cube._cube == cube._cube_solved :
  print( "\tCUBE SOLVED after %d random iterations" % iterations_total )
else :
  print( "\tCUBE UNSOLVED ****************** after %d random iterations" % iterations_total )

print( "END TEST }" )
