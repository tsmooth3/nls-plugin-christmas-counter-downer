"""
Christmas Counter Downer board module implementation.
"""
import datetime
import logging
import os

from PIL import Image
from boards.base_board import BoardBase
from data.data import Data
from renderer.matrix import Matrix

from . import __board_name__, __description__, __version__

debug = logging.getLogger("scoreboard")

# ---- Main class --------------------------------------------------------------
class Christmas(BoardBase):
    """
    The **Christmas Counter Downer** displays a countdown to Christmas.
    """

    def __init__(self, data: Data, matrix: Matrix, sleepEvent):
        super().__init__(data, matrix, sleepEvent)

        # Board metadata from package
        self.board_name = __board_name__
        self.board_version = __version__
        self.board_description = __description__
        
        # Get configuration values with defaults
        self.data = data
        self.matrix = matrix
        self.sleepEvent = sleepEvent
        self.sleepEvent.clear()

        # Resolve paths relative to the plugin directory
        self.board_dir = self._get_board_directory()

        # Access standard application config
        self.font = data.config.layout.font
        self.font.large = data.config.layout.font_large_2
        self.font.medium = data.config.layout.font_medium
        self.font.scroll = data.config.layout.font_xmas
        self.scroll_pos = self.matrix.width

        # custom variables
        self.almost_there = False
        self.days_to_xmas = 0
        self.hours_to_xmas = 0
        self.minutes_to_xmas = 0
        self.seconds_to_xmas = 0

    def _get_board_directory(self):
        """Get the absolute path to this board's directory."""
        import inspect
        board_file = inspect.getfile(self.__class__)
        return os.path.dirname(os.path.abspath(board_file))

    # -------- Rendering --------
    def render(self):
        debug.info("Rendering Christmas Counter Downer")

        self.matrix.clear()

        self.update_countdown()

        if self.days_to_xmas == -1:
            #today is christmas
            self.xmas_today()
        else:
            #today is not Christmas
            if self.days_to_xmas <= 101: 
                self.xmas_countdown()

    def update_countdown(self):

        #get today's date
        today = datetime.datetime.now()
        
        # for testing
        now = datetime.datetime.now()
        td = datetime.timedelta(days=15, hours=2, minutes=17)
        #today = now + td
        
        #find the next christmas
        if today.month == 12 and today.day > 25:
            xmas_year = today.year + 1
        else:
            xmas_year = today.year

        xmas = datetime.datetime(xmas_year,12,25)
        
        #calculate days to xmas
        time_to_xmas = xmas - today
        self.days_to_xmas = time_to_xmas.days
        self.hours_to_xmas = time_to_xmas.seconds // 3600
        self.minutes_to_xmas = (time_to_xmas.seconds % 3600) // 60
        self.seconds_to_xmas = time_to_xmas.seconds % 60
        if time_to_xmas.total_seconds() < 180:
            self.almost_there = True
        else:
            self.almost_there = False

        debug.info(f"Christmas Countdown: {self.almost_there} : {self.days_to_xmas:02}d {self.hours_to_xmas:02}h {self.minutes_to_xmas:02}m {self.seconds_to_xmas:02}s")
    
    def xmas_today(self) :
        #  it's Christmas!

        duration = 15
        i = 0
        scroll_rate = .01
            
        debug.info("It's Christmas!")

        while not self.sleepEvent.is_set():

            self.matrix.clear()

            xmas_scroll_text = self.matrix.draw_text(
                (self.scroll_pos,12),
                "MERRY CHRISTMAS!",
                font=self.font.scroll,
                fill=(0,255,0)
                )
            
            xmas_scroll_text_width = xmas_scroll_text["size"][0] + 3
            
            xmas_image = Image.open(f'{self.board_dir}/assets/images/sleigh.png')
            self.matrix.draw_image((self.scroll_pos + xmas_scroll_text_width,4), xmas_image)

            xmas_content_width = xmas_scroll_text_width + 48

            if(self.scroll_pos < (0 - xmas_content_width) ): self.scroll_pos = self.matrix.width

            i += scroll_rate
            self.scroll_pos -= 1

            self.matrix.render()
            #sleep(scroll_rate)
            self.sleepEvent.wait(scroll_rate)

            if(i > duration) : break

    def xmas_countdown(self) :
        
        debug.info("Christmas Counter Downer")
        loopTime = 10
        if self.almost_there: 
            loopTime = 180
        
        for _ in range(loopTime):
            self.update_countdown()
            
            self.matrix.clear()
            if self.days_to_xmas == -1:
                self.almost_there = False
                self.xmas_today()
                break

            #draw countdown to xmas
            self.matrix.draw_text(
                (10,10),
                f"{self.days_to_xmas} days",
                font=self.font.medium,
                fill=(0,255,0)
            )
            self.matrix.draw_text(
                (10,25),
                f"{self.hours_to_xmas:02}:{self.minutes_to_xmas:02}:{self.seconds_to_xmas:02}",
                font=self.font.medium,
                fill=(0,255,0)
            )
        
            #choose one of three daily images to draw based on days to xmas and draw it
            if self.days_to_xmas % 3 == 0:
                xmas_image = Image.open(f'{self.board_dir}/assets/images/xmas_tree.png').resize((48,48))
            elif self.days_to_xmas % 3 == 2:
                xmas_image = Image.open(f'{self.board_dir}/assets/images/candy_cane.png').resize((48,48))
            else:
                xmas_image = Image.open(f'{self.board_dir}/assets/images/gbread.png').resize((48,48))

            self.matrix.draw_image((75,2), xmas_image)
           
            # bottom text
            self.matrix.draw_text(
                (15,52), 
                "'TIL CHRISTMAS", 
                font=self.font.medium,
                fill=(255,0,0)
             )

            self.matrix.render()
            self.sleepEvent.wait(1)