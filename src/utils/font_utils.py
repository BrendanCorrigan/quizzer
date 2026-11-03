class FontUtils():
    
    # -----------------------------------------------
    # 
    # -----------------------------------------------
    @staticmethod
    def do_a_thing(self, success: bool = True) -> bool:
        '''
        do a thing
        
        Args:
            success (bool): if the thing to do is successful or not
        Returns:
            True if Successful, False otherwise.        
        '''
        return success

    @staticmethod
    # -----------------------------------------------
    # 
    # -----------------------------------------------
    def get_font_point_size(font, target_pixel_height: int) -> int:
        '''
        do a static thing
        
        Args:
            success (bool): if the thing to do is successful or not
        Returns:
            True if Successful, False otherwise.        
        '''
        found: bool = False
        point_size: int = 5

    
        return point_size
    

#	public int getFontPointSizeMatch(Font font, int targetPixelHeight) {
#		boolean found = false;
#		int pointSize = 5;
#		
#		for (int i = 0; i < targetPixelHeight && !found; i++) {
#
#			Font thisFont = new Font(font.getFontName(), font.getStyle(), i);
#			FontMetrics fm = super.getFontMetrics(thisFont);
#
#			if (fm.getAscent() > targetPixelHeight) {
#				found = true;
#				pointSize = i - 1;
#				
#				font = new Font(font.getFontName(), font.getStyle(), pointSize);
#				logger.debug("Point Size = " + pointSize);
#			}
#		}
#
#		logger.debug("point size: " + pointSize);
#		return pointSize;
#	}
#

    # -----------------------------------------------
    # 
    # -----------------------------------------------
    def __repr__(self) -> str:
        return(f"FontUtils")
