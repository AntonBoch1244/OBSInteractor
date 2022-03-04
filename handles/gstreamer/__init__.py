import gi

gi.require_version("GLib", "2.0")
gi.require_version("Gst", "1.0")

from gi.repository import GLib
from gi.repository import Gst


class GStreamer:
    last_id: int = 0
    streams: dict = {}

    def __init__(self, argv=None):
        if argv is None:
            argv = []

        try:
            self.isInitialized, self.argv = Gst.init_check(argv)
        except GLib.Error as exception:
            print(exception)

        if not self.isInitialized:
            print("GStreamer not working with this arguments")

    def createNewStream(self, sid, caps=None, stream_type=8, stream_flags=2):
        # ** Explanation:
        # sid is new stream name, used only for gstreamer
        # caps can be None
        # stream_type is type of stream for demuxers
        #   I set it to 8 cause any stream we are creating here
        #   can contain subtitles, audio and video
        # stream_flags is transmitting flags for demuxers
        #   I set it to 2 cause of it is default behavior be selective
        stream: Gst.Stream

        if stream_type is Gst.StreamType:
            pass
        elif type(stream_type) is int:
            if stream_type in [1, 2, 4, 8, 16]:
                stream_type = Gst.StreamType(stream_type)
            else:
                print("stream_type MUST in 1, 2, 4, 8, 16. Defaulting to 8.")
                stream_type = Gst.StreamType(8)
        else:
            print(f"stream_type is {type(stream_type)} which is not allowed for.")
            stream_type = Gst.StreamType(8)

        if stream_flags is Gst.StreamFlags:
            pass
        elif type(stream_flags) is int:
            if stream_flags in [0, 1, 2, 4]:
                stream_flags = Gst.StreamFlags(stream_flags)
            else:
                print("stream_flags MUST in 0, 1, 2, 4. Defaulting to 2.")
                stream_flags = Gst.StreamFlags(2)
        else:
            print(f"stream_flags is {type(stream_flags)} which is not allowed for.")
            stream_flags = Gst.StreamFlags(2)

        new_caps = Gst.Caps.new_empty_simple("container")

        if caps is Gst.Caps:
            new_caps.append(caps)
        if type(caps) is str:
            caps = Gst.caps_from_string(caps)
        if not (caps is None or caps is Gst.Caps or type(caps) is str):
            print("caps MUST be as Gst.Caps or None or str.")

        stream = Gst.Stream(stream_id=sid, caps=new_caps, stream_type=stream_type, stream_flags=stream_flags)

        self.streams.update({sid: (self.last_id, stream)})

        self.last_id += 1

    def __del__(self):
        Gst.deinit()
