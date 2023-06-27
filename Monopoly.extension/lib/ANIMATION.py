"""handle 
player move between location.--->call SOUNDS
player rotate in spot.
UFO spon and decent/ascent
NPC move.
money fly
gate spin
cloud move
asset show and hide gradient effect
    """
import ERROR_HANDLE
import SOUND
from Autodesk.Revit import DB
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

def player_money_animation(player, money, is_gain):
    """money animation on revit object. affect color, symbol, sound, gradient change.
    Args:
        player(Player): game player
        money(abs.int): revit object
        is_gain(bool): is gain or lose
    """
    pass

    # call sound


def player_rotate_animation(player, angle):
    """player rotate animation.
    Args:
        player(Player): game player
        angle(int): rotate angle
    """
    pass


def player_move_animation_single(player, target_asset):
    SOUND.player_moving()


    initial_pt = player.revit_obj.Location.Point
    final_pt = target_asset.revit_object.Location.Point

    # use this to look like playing stepping on head
    if target_asset.is_occupied:
        final_pt += DB.XYZ(0,0,3)

    try:
        line = DB.Line.CreateBound(initial_pt, final_pt)
        mid_pt = line.Evaluate(0.5, True)
        mid_pt_new = DB.XYZ(mid_pt.X, mid_pt.Y, mid_pt.Z + line.Length/2.0)
        arc = DB.Arc.Create(initial_pt, final_pt, mid_pt_new)
    except:#line too short, just update data and leave
        t = DB.Transaction(doc,"move" )
        t.Start()
        #print (target.Location)
        #print (player)

        #revit_object = doc.GetElement(player.Id)
        vec = final_pt - initial_pt
        #DB.ElementTransformUtils.MoveElement(doc, player.Id,vec)

        translation = DB.Transform.CreateTranslation(vec)
        """
        >>>>>>>>>>>>>>>>>also neeed to condider orienting object to the direction of travel"""
        DB.AdaptiveComponentInstanceUtils.MoveAdaptiveComponentInstance (player.revit_obj , translation, True)
        

        t.Commit()
        return

   

    step = 20 
    for i in range(step + 1):
  
        pt_para = float(i)/step
        temp_location = arc.Evaluate(pt_para, True)

        t = DB.Transaction(doc,"frame update" )
        t.Start()
        player.revit_obj.Location.Point = temp_location
        # CLOUD.change_sky(wind)
        # MONEY_GATE.spin_gate()
        t.Commit()


        safety = 0.01#so there is never division by zero
        speed = -pt_para * (pt_para - 1) + safety#faster in middle
        pause_time = 0.25 + safety - speed# 1/4 is the peak value in normalised condition


        uidoc.RefreshActiveView()
     



    return True

def player_move_animation(player, target_asset):
    """player move animation.
    Args:
        player(Player): player object
        target_asset(Asset ): targt object
    """


    current_position = player.position_index
    next_position = current_position # this is to assume the next position is the same as current position

    while next_position != target_asset.position_index:
        
        
        # this is to ensure all tile is reach
        # becasue if end in max marker index, the last tile will be formated to 0 and jump to gate. That is not right
        next_position = next_position % (player.board.max_marker_index + 1)
       
        #print ("the next local position index is {}".format(next_position))
        local_target_asset = player.board.map_key[next_position]
        player_move_animation_single(player, local_target_asset)
        

        next_position += 1

    player.position_index = target_asset.position_index


def gradually_appear(element, time_interval):
    """gradually appear element.
    Args:
        element(revit object): revit object
        time_interval(int): time interval
    """
    pass

def gradually_disappear(element, time_interval):
    """gradually disappear element.
    Args:
        element(revit object): revit object
        time_interval(int): time interval
    """
    pass