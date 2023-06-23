# Revit-Monopoly

---

##dev-diary-01: 2023-06-23
You can play monopoly directly in Revit. All game logic handled in python.
Previously I have tried a version where all attr stored in revit family object. It turns out to be very inconvinient to update all families when game design change, and it seems I have to manage two set of data together becasue processed python data need to save back to revit families.

So this time, i will be only store key information that will not get changed in revit objects, such as position index, event card descrioption, etc. ANything that is longterm.

Another thing I have larned from the battleship game development  is that a good UI window and a in-game curser can real make thing interesting. And shared-family can be a great solution to add sub-element control in game.

I have also learned that freeform rotation is possible when main model hosted to a adptive point. This will make the animation much better than before, becasue now player piece can face the direction of travel, that is a big visual improvement.