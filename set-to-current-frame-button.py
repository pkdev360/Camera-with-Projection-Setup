import nuke

camera = nuke.thisNode()

def set_to_current_frame():
    camera["projection_frame"].setValue(nuke.frame())

set_to_current_frame()