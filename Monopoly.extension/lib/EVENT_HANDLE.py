

from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent
# from System import EventHandler, Uri


from Autodesk.Revit.Exceptions import InvalidOperationException
import traceback


# Create a subclass of IExternalEventHandler
class SimpleEventHandler(IExternalEventHandler):
    """
    Simple IExternalEventHandler sample
    """

    # __init__ is used to make function from outside of the class to be executed by the handler. \
    # Instructions could be simply written under Execute method only
    def __init__(self, do_this):
        self.do_this = do_this
        self.kwargs = None
        self.OUT = None

    # Execute method run in Revit API environment.

    def Execute(self,  uiapp):
        try:
            try:
                # print "try to do event handler func"
                self.OUT = self.do_this(*self.kwargs)
            except:
                print("failed")
                print(traceback.format_exc())
        except InvalidOperationException:
            # If you don't catch this exeption Revit may crash.
            print("InvalidOperationException catched")

    def GetName(self):
        return "simple function executed by an IExternalEventHandler in a Form"
    
