import gi
from gi.repository import Gtk, Gdk

class TransparentWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Transparent Window Example")
        
        # Set the window to be transparent
        self.set_border_width(10)
        self.set_default_size(400, 300)
        self.connect("draw", self.on_draw)
        self.set_app_paintable(True)

        # Add a button to demonstrate that widgets are still visible
        button = Gtk.Button(label="Click Me")
        self.add(button)

    def on_draw(self, widget, cr):
        # Set the transparency of the window
        cr.set_source_rgba(0, 0, 0, 0)  # RGBA: 0% opacity for full transparency
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

if __name__ == "__main__":
    win = TransparentWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
