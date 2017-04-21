"""Simple Sprite sub-class that renders via a PangoFont"""
from pygame import sprite 
from olpcgames import pangofont

class TextSprite( sprite.Sprite ):
    """Sprite with a simple __text renderer"""
    image = rect = __text = __color = background = None
    def __init__( self, text=None, family=None, size=None, bold=False, italic=False, color=None, background=None ):
        super( TextSprite, self ).__init__( )
        self.__font = pangofont.PangoFont( family=family, size=size, bold=bold, italic=italic )
        self.set_color( color )
        self.set_background( background )
        self.set_text( text )
    def set_text( self, text ):
        """Set our __text string and doPaint to a graphic"""
        self.__text = text 
        self.doPaint( )
    def set_color( self, color =None):
        """Set our rendering colour (default white)"""
        self.__color = color or (255,255,255)
        self.doPaint()
    def set_background( self, color=None ):
        """Set our background __color, default transparent"""
        self.background = color 
        self.doPaint()
    def doPaint( self ):
        """Render our image and rect (or None,None)
        
        After a doPaint you will need to move the rect member to the 
        correct location on the screen.
        """
        if self.__text:
            self.image = self.__font.doPaint( self.__text, color = self.__color, background = self.background )
            currentRect = self.rect
            self.rect = self.image.get_rect()
            if currentRect:
                self.rect.center = currentRect.center 
        else:
            self.rect = None 
            self.image = None
