import nuke


def set_projection(has_projection=False):
    camera = nuke.thisNode()

    # Toggle between "Add Projection"/"Remove Projection" button.
    if has_projection:
        data = {"add_projection": False,
                "del_projection": True,
                "tile_color": 65535}
    else:
        data = {"add_projection": True,
                "del_projection": False,
                "tile_color": 0}

    camera["add_projection"].setVisible(data["add_projection"])
    camera["del_projection"].setVisible(data["del_projection"])
    camera["tile_color"].setValue(data["tile_color"])

    # other knobs can be added for showing or hiding them when
    # the proj. setup added or removed.
    knobs = ["projection_frame"]

    # Show/hide the knob(s) while adding/removing the proj. setup.
    for knob in knobs:
        camera[knob].setVisible(has_projection)

    # Create or Delete the projection setup.
    if has_projection:
        # Create Frame hold node for camera
        framehold_cam = nuke.nodes.FrameHold()
        framehold_cam.setInput(0, camera)
        framehold_cam.setXYpos(int(camera.xpos()), int(camera.ypos()) + 150)
        framehold_cam["first_frame"].setExpression(
            f"parent.{camera.name()}.knob.projection_frame")

        append_id_knob(id(camera), framehold_cam)

        # Create Frame hold node for source frame.
        framehold_cam.selectOnly()
        nukescripts.node_copypaste()
        framehold_src = nuke.selectedNode()
        framehold_src.setXYpos(int(camera.xpos()) + 150,
                               int(camera.ypos()) + 100)

        # Project3D node
        project3d = nuke.nodes.Project3D2()
        project3d.setInput(0, framehold_src)
        project3d.setInput(1, framehold_cam)
        project3d.setXYpos(int(framehold_src.xpos()),
                           int(framehold_src.ypos() + 50))
        append_id_knob(id(camera), project3d)

        # Set projection frame and projection frame ranges.
        first_frame = int(nuke.root()["first_frame"].getValue())
        last_frame = int(nuke.root()["last_frame"].getValue())
        camera["projection_frame"].setRange(first_frame, last_frame)
        camera["projection_frame"].setValue(nuke.frame())

    # Remove projection nodes.
    else:
        for node in nuke.allNodes():
            camera_id_knob = node.knobs().get("camera_id")
            if camera_id_knob and camera_id_knob.value() == str(id(camera)):
                nuke.delete(node)


def append_id_knob(id_, target_node):
    id_knob = nuke.Text_Knob("camera_id", "camera id", str(id_))
    id_knob.setVisible(False)
    target_node.addKnob(id_knob)
