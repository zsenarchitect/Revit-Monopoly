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
import FINDER
import DISPLAY
import time
import System
from Autodesk.Revit import DB
try:
    doc = __revit__.ActiveUIDocument.Document
    uidoc = __revit__.ActiveUIDocument
except:
    pass


def highlight_asset(asset, turn_on = True):
    """highlight asset.
    Args:
        asset(Asset): revit object
    """
    highlighter_symbol = FINDER.get_revit_obj_by_type_name("Highlighter")
    t = DB.Transaction(doc,"highlighter" )
    t.Start()
    vec = asset.revit_object.Location.Point  - highlighter_symbol.Location.Point
    DB.ElementTransformUtils.MoveElement(doc, highlighter_symbol.Id , vec)
    if turn_on:
        doc.ActiveView.UnhideElements (System.Collections.Generic.List[DB.ElementId]([highlighter_symbol.Id]))
    else:
        doc.ActiveView.HideElements (System.Collections.Generic.List[DB.ElementId]([highlighter_symbol.Id]))
    t.Commit()

def player_money_animation(player, money, is_gain, is_quick = False):
    """money animation on revit object. affect color, symbol, sound, gradient change.
    Args:
        player(Player): game player
        money(abs.int): revit object
        is_gain(bool): is gain or lose
    """


    # call sound
    
    money_symbol = FINDER.get_revit_obj_by_type_name("Money_Symbol")
    t = DB.Transaction(doc,"money" )
    t.Start()
    money_symbol.LookupParameter("text_display").Set("${}".format(money))
    vec = player.revit_object.Location.Point + DB.XYZ(0,0,4) - money_symbol.Location.Point
    # translation = DB.Transform.CreateTranslation(vec)
    DB.ElementTransformUtils.MoveElement(doc, money_symbol.Id , vec)
    
    
    mat = FINDER.get_material_by_name("money_positive") if is_gain else FINDER.get_material_by_name("money_negative")
    money_symbol.LookupParameter("money_mat.").Set(mat.Id)

    t.Commit()
    uidoc.RefreshActiveView()
    
    gate = player.game.board.map_key[0]
    step = 10 if is_quick else 30 
    for i in range(step + 1):

   

        t = DB.Transaction(doc,"frame update" )
        t.Start()
        # vec = player.revit_object.Location.Point + DB.XYZ(0,0,7) - money_symbol.Location.Point
        money_symbol.Location.Point += DB.XYZ(0,0,0.2*i/float(step))
        # CLOUD.change_sky(wind)
        gate.spin()
        setting = DB.OverrideGraphicSettings()
        if i > step * 0.3:
            opacity =  (i - step*0.3)/float((1-0.3)*step)
            # print opacity
            setting.SetSurfaceTransparency (opacity*100)
            doc.ActiveView.SetElementOverrides(money_symbol.Id, setting)
  
        t.Commit()


     
        uidoc.RefreshActiveView()
    uidoc.RefreshActiveView()
     


def player_rotate_animation(player, angle):
    """player rotate animation.
    Args:
        player(Player): game player
        angle(int): rotate angle
    """
    pass


def player_move_animation_single(player, target_asset, is_quick):
    SOUND.player_moving()


    initial_pt = player.revit_object.Location.Point
    final_pt = target_asset.revit_object.Location.Point

    # use this to look like playing stepping on head
    if target_asset.is_occupied:
        #print target_asset
        final_pt += DB.XYZ(0,0,3)
        pass

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
        DB.AdaptiveComponentInstanceUtils.MoveAdaptiveComponentInstance (player.revit_object , translation, True)
        

        t.Commit()
        return

   

    step = 5 if is_quick else 10 
    gate = player.game.board.map_key[0]
    for i in range(step + 1):
  
        pt_para = float(i)/step
        temp_location = arc.Evaluate(pt_para, True)

        t = DB.Transaction(doc,"frame update" )
        t.Start()
        player.revit_object.Location.Point = temp_location
        # CLOUD.change_sky(wind)
        gate.spin(is_default_speed = target_asset.position_index != 0)
        t.Commit()


        safety = 0.01#so there is never division by zero
        speed = -pt_para * (pt_para - 1) + safety#faster in middle
        pause_time = 0.25 + safety - speed# 1/4 is the peak value in normalised condition


        uidoc.RefreshActiveView()
     

    if target_asset.position_index == 0:
        
        player.go_thru_payday()

    return True

def player_move_animation(player, target_asset, is_quick = False):
    """player move animation.
    Args:
        player(Player): player object
        target_asset(Asset ): targt object
    """
    if target_asset.position_index < 0:

        player_move_animation_single(player, target_asset, is_quick)
        player.position_index = target_asset.position_index
        return

    current_position = player.position_index
    next_position = current_position # this is to assume the next position is the same as current position

    while player.position_index != target_asset.position_index:
        
        
        # this is to ensure all tile is reach
        # becasue if end in max marker index, the last tile will be formated to 0 and jump to gate. That is not right
        next_position += player.velocity
        next_position = next_position % (player.game.board.max_marker_index + 1)
       
        #print ("the next local position index is {}".format(next_position))
        local_target_asset = player.game.board.map_key[next_position]
        player_move_animation_single(player, local_target_asset, is_quick)
        
        player.position_index = local_target_asset.position_index
    

    # player.position_index = target_asset.position_index
    # print ("the player position index is {}".format(player.position_index))


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

