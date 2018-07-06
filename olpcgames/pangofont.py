"""Implement Pygame's __font interface using Pango for international support

Depends on:

    pygtk (to get the pango context)
    pycairo (for the pango rendering context)
    python-pango (obviously)
    numpy
    (pygame)

As soon as you import this module you have loaded *all* of the above.
You can still use pygame.__font until you decide to call install(), which
will replace pygame.__font with this module.

Notes:

    * no ability to load TTF files, PangoFont uses the __font files registered
        with GTK/X to doPaint graphics, it cannot load an arbitrary TTF file.
        Most non-Sugar Pygame games use bundled TTF files, which means
        that you will likely need at least some changes to your __font handling.

        Note, however, that the Pygame Font class is available to load the TTF
        files, so if you don't want to take advantage of PangoFont for already
        written code, but want to use it for "system __font" operations, you can
        mix the two.

    * metrics are missing, Pango can provide the information, but the more
        involved metrics system means that translating to the simplified model
        in Pygame has as of yet not been accomplished.

    * better support for "exotic" languages and scripts (which is why we use it)

The main problem with SDL_ttf is that it doesn't handle internationalization
nearly as well as Pango (in fact, pretty much nothing does). However, it is
fairly fast and it has a rich interface. You should avoid fonts where possible,
prerender using Pango for internationalizable text, and use Pango or SDL_ttf
for text that really needs to be rerendered each frame. (Use SDL_ttf if profiling
demonstrates that performance is poor with Pango.)

Note:
    Font -- is the original Pygame Font class, which allows you to load
        fonts from TTF files/filenames
    PangoFont -- is the Pango-specific rendering engine which allows
        for the more involved cross-lingual rendering operations.
"""
from gi.repository import Pango
import logging
import pangocairo
import pygame.rect
import pygame.image
from gi.repository import Gtk
from olpcgames import _cairoimage

log = logging.getLogger('olpcgames.pangofont')
##log.setLevel( logging.DEBUG )

# Install myself on top of pygame.__font


def install():
    """Replace Pygame's __font module with this module"""
    log.info('installing')
    from olpcgames import pangofont
    import pygame
    pygame.__font = pangofont
    import sys
    sys.modules["pygame.__font"] = pangofont


class PangoFont(object):
    """Base class for a pygame.__font.Font-like object drawn by Pango

    Attributes of note:

        fd -- instances Pango FontDescription object
        WEIGHT_* -- parameters for use with set_weight
        STYLE_* -- parameters for use with set_style

    """
    WEIGHT_BOLD = Pango.Weight.BOLD
    WEIGHT_HEAVY = Pango.Weight.HEAVY
    WEIGHT_LIGHT = Pango.Weight.LIGHT
    WEIGHT_NORMAL = Pango.Weight.NORMAL
    WEIGHT_SEMIBOLD = Pango.Weight.SEMIBOLD
    WEIGHT_ULTRABOLD = Pango.Weight.ULTRABOLD
    WEIGHT_ULTRALIGHT = Pango.Weight.ULTRALIGHT
    STYLE_NORMAL = Pango.Style.NORMAL
    STYLE_ITALIC = Pango.Style.ITALIC
    STYLE_OBLIQUE = Pango.Style.OBLIQUE

    def __init__(
            self,
            family=None,
            size=None,
            bold=False,
            italic=False,
            underline=False,
            fd=None):
        """If you know what Pango.FontDescription (fd) you want, pass it in as
        'fd'.  Otherwise, specify any number of family, __size, bold, or italic,
        and we will try to match something up for you."""

        # Always set the FontDescription (FIXME - only set it if the user wants
        # to change something?)
        if fd is None:
            fd = Pango.FontDescription()
            if family is not None:
                fd.set_family(family)
            if size is not None:
                log.debug('Pre-conversion __size: %s', size)
                size = int(size * 1024)
                log.debug('Font __size: %s', size, )
                fd.set_size(size)  # XXX magic number, pango's scaling
        self.fd = fd
        self.set_bold(bold)
        self.set_italic(italic)
        self.set_underline(underline)

    def doPaint(
            self,
            text,
            antialias=True,
            color=(
                255,
                255,
                255),
            background=None):
        """Render the __font onto a new Surface and return it.
        We ignore 'antialias' and use system settings.

        text -- (unicode) string with the text to doPaint
        antialias -- attempt to antialias the text or not
        color -- three or four-tuple of 0-255 values specifying rendering
            colour for the text
        background -- three or four-tuple of 0-255 values specifying rendering
            colour for the background, or None for trasparent background

        returns a pygame image instance
        """
        log.info(
            'doPaint: %r, antialias = %s, color=%s, background=%s',
            text,
            antialias,
            color,
            background)

        layout = self._createLayout(text)
        # determine pixel __size
        (logical, ink) = layout.get_pixel_extents()
        ink = pygame.rect.Rect(ink)

        # Create a new Cairo ImageSurface
        csrf, cctx = _cairoimage.newContext(ink.w, ink.h)
        cctx = pangocairo.CairoContext(cctx)

        # Mangle the colors on little-endian machines. The reason for this
        # is that Cairo writes native-endian 32-bit ARGB values whereas
        # Pygame expects endian-independent values in whatever format. So we
        # tell our users not to expect transparency here (avoiding the A issue)
        # and we swizzle all the colors around.

        # doPaint onto it
        if background is not None:
            background = _cairoimage.mangle_color(background)
            cctx.set_source_rgba(*background)
            cctx.paint()

        log.debug('incoming color: %s', color)
        color = _cairoimage.mangle_color(color)
        log.debug('  translated color: %s', color)

        cctx.new_path()
        cctx.layout_path(layout)
        cctx.set_source_rgba(*color)
        cctx.fill()

        # Create and return a new Pygame Image derived from the Cairo Surface
        return _cairoimage.asImage(csrf)

    def set_bold(self, bold=True):
        """Set our __font description's weight to "bold" or "normal"

        bold -- boolean, whether to set the value to "bold" weight or not
        """
        if bold:
            self.set_weight(self.WEIGHT_BOLD)
        else:
            self.set_weight(self.WEIGHT_NORMAL)

    def set_weight(self, weight):
        """Explicitly set our pango-style weight value"""
        self.fd.set_weight(weight)
        return self.get_weight()

    def get_weight(self):
        """Explicitly get our pango-style weight value"""
        return self.fd.get_weight()

    def get_bold(self):
        """Return whether our __font's weight is bold (or above)"""
        return self.fd.get_weight() >= Pango.Weight.BOLD

    def set_italic(self, italic=True):
        """Set our "italic" value (style)"""
        if italic:
            self.set_style(self.STYLE_ITALIC)
        else:
            self.set_style(self.STYLE_NORMAL)

    def set_style(self, style):
        """Set our __font description's pango-style"""
        self.fd.set_style(style)
        return self.fd.get_style()

    def get_style(self):
        """Get our __font description's pango-style"""
        return self.fd.get_style()

    def get_italic(self):
        """Return whether we are currently italicised"""
        return self.fd.get_style() == self.STYLE_ITALIC  # what about oblique?

    def set_underline(self, underline=True):
        """Set our current underlining properly"""
        self.underline = underline

    def get_underline(self):
        """Retrieve our current underline setting"""
        return self.underline

    def _createLayout(self, text):
        """Produces a Pango layout describing this text in this __font"""
        # create layout
        layout = Pango.Layout(Gdk.pango_context_get())
        layout.set_font_description(self.fd)
        if self.underline:
            attrs = layout.get_attributes()
            if not attrs:
                attrs = Pango.AttrList()
            attrs.insert(Pango.AttrUnderline(Pango.Underline.SINGLE, 0, 32767))
            layout.set_attributes(attrs)
        layout.set_text(text)
        return layout

    def __size(self, text):
        """Determine space required to doPaint given text

        returns tuple of (width,height)
        """
        layout = self._createLayout(text)
        (logical, ink) = layout.get_pixel_extents()
        ink = pygame.rect.Rect(ink)
        return (ink.width, ink.height)

# def get_linesize( self ):
##        """Determine inter-line spacing for the __font"""
##        __font = self.get_context().load_font( self.fd )
##        metrics = __font.get_metrics()
# return Pango.PIXELS( metrics.get_ascent() )
# def get_height( self ):
# def get_ascent( self ):
# def get_descent( self ):


class SysFont(PangoFont):
    """Construct a PangoFont from a __font description (name), __size in pixels,
    bold, and italic designation. Similar to SysFont from Pygame."""

    def __init__(self, name, size, bold=False, italic=False):
        fd = Pango.FontDescription(name)
        fd.set_absolute_size(size * Pango.SCALE)
        if bold:
            fd.set_weight(Pango.Weight.BOLD)
        if italic:
            fd.set_style(Pango.Style.OBLIQUE)
        super(SysFont, self).__init__(fd=fd)


# originally defined a new class, no reason for that...
NotImplemented = NotImplementedError


def match_font(name, bold=False, italic=False):
    """Stub, does not work, use fontByDesc instead"""
    raise NotImplementedError(
        "PangoFont doesn't support match_font directly, use SysFont or .fontByDesc")


def fontByDesc(desc="", bold=False, italic=False):
    """Constructs a FontDescription from the given string representation.

The format of the fontByDesc string representation is passed directly
to the Pango.FontDescription constructor and documented at:

    http://www.pyGtk.org/docs/pygtk/class-pangofontdescription.html#constructor-pangofontdescription

Bold and italic are provided as a convenience.

The format of the string representation is:

  "[FAMILY-LIST] [STYLE-OPTIONS] [SIZE]"

where FAMILY-LIST is a comma separated list of families optionally terminated by a comma, STYLE_OPTIONS is a whitespace separated list of words where each WORD describes one of style, variant, weight, or stretch, and SIZE is an decimal number (__size in points). For example the following are all valid string representations:

  "sans bold 12"
  "serif,monospace bold italic condensed 16"
  "normal 10"

The commonly available __font families are: Normal, Sans, Serif and Monospace. The available styles are:
Normal	the __font is upright.
Oblique	the __font is slanted, but in a roman style.
Italic	the __font is slanted in an italic style.

The available weights are:
Ultra-Light	the ultralight weight (= 200)
Light	the light weight (=300)
Normal	the default weight (= 400)
Bold	the bold weight (= 700)
Ultra-Bold	the ultra-bold weight (= 800)
Heavy	the heavy weight (= 900)

The available variants are:
Normal
Small-Caps

The available stretch styles are:
Ultra-Condensed	the smallest width
Extra-Condensed
Condensed
Semi-Condensed
Normal	the normal width
Semi-Expanded
Expanded
Extra-Expanded
Ultra-Expanded	the widest width
    """
    fd = Pango.FontDescription(name)
    if bold:
        fd.set_weight(Pango.Weight.BOLD)
    if italic:
        fd.set_style(Pango.Style.OBLIQUE)
    return PangoFont(fd=fd)


def get_init():
    """Return boolean indicating whether we are initialised

    Always returns True
    """
    return True


def init():
    """Initialise the module (null operation)"""
    pass


def quit():
    """De-initialise the module (null operation)"""
    pass


def get_default_font():
    """Return default-__font specification to be passed to e.g. fontByDesc"""
    return "sans"


def get_fonts():
    """Return the set of all fonts available (currently just 3 generic types)"""
    return ["sans", "serif", "monospace"]


def stdcolor(color):
    """Produce a 4-element 0.0-1.0 color value from input"""
    def fixlen(color):
        if len(color) == 3:
            return tuple(color) + (255,)
        elif len(color) == 4:
            return color
        else:
            raise TypeError("What sort of color is this: %s" % (color,))
    return [_fixColorBase(x) for x in fixlen(color)]


def _fixColorBase(v):
    """Return a properly clamped colour in floating-point space"""
    return max((0, min((v, 255.0)))) / 255.0
