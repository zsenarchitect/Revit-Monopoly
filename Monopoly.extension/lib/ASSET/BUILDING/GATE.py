from ASSET import Asset


class Gate(Asset):
    
    def spin(self, is_default_speed = True):
        current_angle = self.revit_object.LookupParameter("angle").AsDouble()
        if is_default_speed:
            step = 0.05
        else:
            step = 0.5
        new_angle = (current_angle + step) % 360
        self.revit_object.LookupParameter("angle").Set(new_angle)
        # call ANIMATION function
