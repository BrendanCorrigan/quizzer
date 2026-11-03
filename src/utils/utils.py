from datetime import datetime, timedelta, date   
import json
import random
import string
import os
import re

class Utils:
    
    # -----------------------------------------------------------
    # Get the ordinal of a date e.g. 1st, 2nd, 3rd, 4th...
    # -----------------------------------------------------------
    @staticmethod
    def ordinal(n : int) -> str:
        '''
        Return the ordinal representation of a number.
        For example, 1 becomes "1st", 2 becomes "2nd", etc. 
        Arguments:
            n : int : The number to convert to an ordinal.
        Returns:
            str : The ordinal representation of the number.
        '''
        return str(n) + ("th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))
    
    # -----------------------------------------------------------
    # return a friendly timetamp... "Wednesday 25th October @ 20:18:21"
    # -----------------------------------------------------------
    @staticmethod
    def friendlyTimestamp(timestamper : datetime|None = None) -> str:
        '''
        Return a friendly timestamp string.
        If no datetime is provided, the current datetime is used.
        
        Arguments:
            timestamper : datetime|None : The datetime to format. Default is None.
        Returns:
            str : The formatted timestamp string.
        '''
        
        if timestamper == None:
            timestamper = datetime.now()

        return timestamper.strftime(f"%A {Utils.ordinal(timestamper.day)} %B @ %H:%M:%S")
    
    # -------------------------------------------------------------------
    #
    # -------------------------------------------------------------------
    # @staticmethod
    # def getDateFromFileName(filename) -> str:
    #     assert filename is not None, "A fileaname is required"
        
    #     file, ext  = os.path.splitext(filename)
    #     date = file.split("_")[1]
    #     return date
    
    
    @staticmethod
    def getDateFromFileName(filename) -> date|None:
        match = re.search(r'(\d{8})', filename) # CCYYMMDD
        if match:
            date_str = match.group(1)
            date = datetime.strptime(date_str, "%Y%m%d").date()
            return date
        return None
    
    # -------------------------------------------------------------------
    #
    # -------------------------------------------------------------------
    @staticmethod
    def getDatetimeFromFileName(filename) -> datetime:
        assert filename is not None, "A fileaname is required"
        
        file, ext  = os.path.splitext(filename)
        date = file.split("_")[1]
        date = datetime.strptime(date, "%Y%m%d")
        return date
    
    # -----------------------------------------------------------
    # create a random(ish) GUID...
    # -----------------------------------------------------------
    @staticmethod
    def guid(length : int = 5) -> str:
        '''
        Create a random GUID of the specified length.
        Each segment of the GUID consists of four digits, and segments are 
        separated by hyphens.
        
        Arguments:
            length : int : The number of segments in the GUID. Default is 5.
        Returns:
            str : The generated GUID.
        '''
        guid : str = f"{random.randint(0, 9999):04d}"
        for _ in range(1, length):
            guid += f"-{random.randint(0, 9999):04d}"

        return guid
    
    # -----------------------------------------------------------
    # Count words in a line of text...
    # -----------------------------------------------------------
    @staticmethod
    def extractWords(line : str) -> list:
        return re.sub(f'[{string.punctuation}]', '', line).split()

    # -----------------------------------------------------------
    @staticmethod
    def wordCount(line : str) -> int:
        return(len(Utils.extractWords(line)))


    # -----------------------------------------------------------
    # Convert a timer into seconds
    # -----------------------------------------------------------
    @staticmethod
    def covertTimeToSeconds(time : str) -> int:
        '''
        Convert a time string into total seconds.
        The time string can be in the format of "D:H:M:S", "H:M:S", "M:S", or "S". 
        
        Arguments:
            time : str : The time string to convert.   
        Returns:
            int : The total number of seconds.
        '''
        # assume format is DAYS:HOURS:MINS:SECONDS
        seconds = 0
        components = time.strip().split(":")
        if len(components) > 0:
            seconds = int(components[-1])
        if len(components) > 1:
            seconds += int(components[-2]) * 60
        if len(components) > 2:
            seconds += int(components[-3]) * 60 * 60
        if len(components) > 3:
            seconds += int(components[-4]) * 60 * 60 * 24

        return seconds

    # -----------------------------------------------------------
    # Convert a seconds to hours:mins:seconds
    # -----------------------------------------------------------
    @staticmethod
    def covertSecondsToTime(seconds : int) -> str:
        '''
        Convert seconds to a time string in the format "H:MM:SS".   
        
        Arguments:
            seconds : int : The number of seconds to convert.
        Returns:
            str : The time string in the format "H:MM:SS".
        '''        
        return str(timedelta(seconds=seconds))

    # -----------------------------------------------------------
    # Convert a seconds to hours:mins:seconds
    # -----------------------------------------------------------
    @staticmethod
    def friendlySecondsToTime(seconds : int) -> str:
        '''
        Convert seconds to a friendly time format.
        The format is "X Hours Y Minutes Z Seconds", omitting any zero values.  
        
        Arguments:
            seconds : int : The number of seconds to convert.
        Returns:
            str : The friendly time format.
        '''
        
        components = Utils.covertSecondsToTime(seconds).split(':')
        result = ""
        if components[0] != "0":
            result = f"{components[0]} Hours {components[1]} Minutes {components[2]} Seconds"
        elif components[1] != "00":
            result = f"{components[1]} Minutes {components[2]} Seconds"
        else:
            result = f"{components[2]} Seconds"
        return result
    
    # -----------------------------------------------------------
    # Determine the type of data being passed
    # -----------------------------------------------------------
    @staticmethod
    def listToString(list) -> str:
        result = '"' + '","'.join(map(str, list)) + '"'
        return result


    # -----------------------------------------------------------
    # Create boxes around the list of data
    # -----------------------------------------------------------
    @staticmethod
    def boxIt(values):
        '''
        Create a box around the provided list of values.
        
        Arguments:
            values : list : A list of lists containing the data to box.
        Returns:
            list[str] : A list of strings representing the boxed data.
        '''

        result = []

        top_box = "┌─┬─┐"
        mid_box = "│ │ │"
        sep_box = "├─┼─┤"
        bot_box = "└─┴─┘"

        widths = [1] *len(values[0])

        for row in values:
            for index, value in enumerate(row):
                width = len(str(value).strip())

                if (widths[index] < width):
                    widths[index] = width

        top    = top_box[0]
        sep    = sep_box[0]
        bot    = bot_box[0]
        
        for index, _ in enumerate(values[0]):
            width = widths[index]

            top    += f"{'':{top_box[1]}<{width}}{top_box[2]}"
            sep    += f"{'':{sep_box[1]}<{width}}{sep_box[2]}"
            bot    += f"{'':{bot_box[1]}<{width}}{bot_box[2]}"

        top    = (top[:-1] + top_box[4])
        sep    = (sep[:-1] + sep_box[4])
        bot    = (bot[:-1] + bot_box[4])

        result.append(str(top))
        
        for row in values:
            data = mid_box[0]
            for index, value in enumerate(row):
                width = widths[index]
                data += f"{str(value).strip():{width}}{mid_box[0]}"
            result.append(str(data))
            result.append(str(sep))

        del result[-1]
        result.append(str(bot))

        return result

    # -----------------------------------------------------------
    # Create boxes around the list of data
    # -----------------------------------------------------------
    @staticmethod
    def boxItWithHeadings(headings, values):
        temp = []
        temp.append(headings)
        return Utils.boxIt(temp + values)


    # -----------------------------------------------------------
    # Count the lines in a file...
    # -----------------------------------------------------------
    @staticmethod
    def countLinesInFile(file, encoding="utf-8"):
        linesInFile = 0

        count: int = 0
        try:
            with open(file, 'r', encoding=encoding) as f:
                for count, _ in enumerate(f):
                    pass

                linesInFile = count + 1

        except Exception as e:
            print(e)        

        return linesInFile


    # -----------------------------------------------------------
    # Return a configuration from the configuration file...
    # -----------------------------------------------------------
    @staticmethod
    def getConfig(file, name):
        result = None
        
        try:
            with open(file, 'r') as f:

                data = json.load(f)
                for item in data:
                    if item["name"] == name:
                        result = item
                    
        except Exception as e:
            print(e)        
            print(f"Not able to open or read from file {file}")

        if result == None:
            print(f"** warning **" )
            print(f"  No configuration '{name}' in file '{file}'" )
                    
        return result



        
    # -------------------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------------------
    @staticmethod
    def getSaveFileName(fileName):
        head, tail = os.path.split(fileName)
        root, ext = os.path.splitext(tail)
        fileName = f"data/save/{root}.json"
        return fileName


