from quizzer.QuizUtils import QuizUtils
from quizzer import DEFAULT_THEME


class QuizTheme():
        
    # Sensible Defaults...
    DEFAULT_THEME_PRIMARY_COLOUR = "#F5F5F5"
    DEFAULT_THEME_SECONDARY_COLOUR = "#CECECE"
    DEFAULT_THEME_FONT_PRIMARY_COLOUR = "#161616"
    DEFAULT_THEME_FONT_SECONDARY_COLOUR = "#494949"
    
    DEFAULT_FONT_JUMBO_BOLD = ("Arial", 36, "bold")
    DEFAULT_FONT_LARGE_BOLD = ("Arial", 20, "bold")
    DEFAULT_FONT_MEDIUM = ("Arial", 16, "bold")
    DEFAULT_FONT_SMALL = ("Arial", 12, "normal")
    
    def __init__(self, theme_file_location: str = DEFAULT_THEME):
        
        theme = QuizUtils.load_theme(theme_file_location)
                
        self.theme_name = theme.get("name", "Unknown")
        
        self.background_colour = QuizTheme.DEFAULT_THEME_PRIMARY_COLOUR
        self.background_secondary_colour = QuizTheme.DEFAULT_THEME_SECONDARY_COLOUR
        self.font_primary_colour = QuizTheme.DEFAULT_THEME_FONT_PRIMARY_COLOUR      
        self.font_secondary_colour = QuizTheme.DEFAULT_THEME_FONT_SECONDARY_COLOUR
        
        self.small_font = QuizTheme.DEFAULT_FONT_SMALL
        self.medium_font = QuizTheme.DEFAULT_FONT_MEDIUM
        self.large_font = QuizTheme.DEFAULT_FONT_LARGE_BOLD
        self.jumbo_font = QuizTheme.DEFAULT_FONT_JUMBO_BOLD

        # ---------------------------------------------------------------------------------
        # Window information
        # ---------------------------------------------------------------------------------
        self.name = theme.get("title", "Quiz")

        self.window_width: int = 600
        self.window_height: int = 900
        if "window" in theme.keys():
            self.window_width  = theme["window"].get("width", 600)
            self.window_height = theme["window"].get("height", 900)
        
        # ---------------------------------------------------------------------------------
        # Basic font and colour configuration
        # ---------------------------------------------------------------------------------                
        self.quiz_directory = theme.get("quiz_directory", "quizzes")
        
        if "config" in theme.keys():
            self.background_colour = theme["config"].get("theme_primary_colour", QuizTheme.DEFAULT_THEME_PRIMARY_COLOUR)
            self.background_secondary_colour = theme["config"].get("theme_secondary_colour", QuizTheme.DEFAULT_THEME_SECONDARY_COLOUR)
            self.font_primary_colour = theme["config"].get("font_primary_colour", QuizTheme.DEFAULT_THEME_FONT_PRIMARY_COLOUR)
            self.font_secondary_colour = theme["config"].get("font_secondary_colour", QuizTheme.DEFAULT_THEME_FONT_SECONDARY_COLOUR)
            
            self.small_font = tuple(theme["config"].get("small_font", QuizTheme.DEFAULT_FONT_SMALL))
            self.medium_font = tuple(theme["config"].get("medium_font", QuizTheme.DEFAULT_FONT_MEDIUM))
            self.large_font = tuple(theme["config"].get("large_font", QuizTheme.DEFAULT_FONT_LARGE_BOLD))
            self.jumbo_font = tuple(theme["config"].get("jumbo_font", QuizTheme.DEFAULT_FONT_JUMBO_BOLD))
            
        # ---------------------------------------------------------------------------------
        # Quiz Logo
        # ---------------------------------------------------------------------------------                
        self.hasLogo = False
        if "logo" in theme.keys():
            self.logo = theme.get("logo", "")
            
            if "logo_duration" in theme.keys():
                self.logo_duration = theme.get("logo_duration", 1500)
                
            self.hasLogo = True        

        # ---------------------------------------------------------------------------------
        # Common images for assets of the quiz panels
        # ---------------------------------------------------------------------------------                
        self.thumbsUpImage_file   = "themes/default/assets/thumbs_up_740x740.png" 
        self.thumbsDownImage_file = "themes/default/assets/thumbs_down_740x740.png"
        self.tick_file  = "themes/default/assets/tick_alt2_120x120.png"
        self.cross_file = "themes/default/assets/cross_alt2_120x120.png"

        if "assets" in theme.keys():
            self.thumbsUpImage_file   = theme["assets"].get("thumbs_up",  "themes/default/assets/thumbs_up_740x740.png")                
            self.thumbsDownImage_file = theme["assets"].get("thumbs_down","themes/default/assets/thumbs_down_740x740.png")                
            self.tick_file   = theme["assets"].get("tick", "themes/default/assets/tick_alt2_120x120.png")                
            self.cross_file = theme["assets"].get("cross","themes/default/assets/cross_alt2_120x120.png")                

        # self.thumbsUpImage = QuizUtils.load_photoimage(thumbsUpImage_file, size=64)
        # self.thumbsDownImage = QuizUtils.load_photoimage(thumbsDownImage_file, size=64)
        # self.tickImage = QuizUtils.load_photoimage(tick_file, size=64)
        # self.crossImage = QuizUtils.load_photoimage(cross_file, size=64)
        
        # ---------------------------------------------------------------------------------
        # Footer
        # ---------------------------------------------------------------------------------
        self.show_footer = False
        if "window" in theme.keys():
            self.footer_image  = theme["window"].get("footer_image", "")
            if self.footer_image != "":
                self.show_footer = True
                            