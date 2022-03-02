import gi

gi.require_version("Gst", "1.0")

from gi.repository import Gst


class GStreamer:

    def __init__(self, argv):
        if not Gst.init_check(argv)[0]:
            print("GStreamer not working with this arguments")

    def __del__(self):
        Gst.deinit()
