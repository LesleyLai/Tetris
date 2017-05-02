"""
This file contains a class for list of ranking
"""

import getpass

class TetrisRankingList:
    """
    This class is a size-bounded list of the ranking data. The records
    are always sorted.
    """

    MAX_RANKING_RECORD = 10

    def __init__(self, filename):
        "Initializes the ranking list"
        self.__filename = filename
        self.__records = []
        self._read_ranking_file()

    def __len__(self):
        return len(self.__records)

    def __getitem__(self, index):
        ''' Get items inside the ranking list'''
        return self.__records[index]

    def add_record(self, score):
        """
        Adds a record of the score to the list
        """
        username = getpass.getuser()
        self.__records.append((score, username))
        # Sort by score
        self.__records = sorted(self.__records,
                                key=lambda record: -record[0])

        if len(self.__records) > TetrisRankingList.MAX_RANKING_RECORD:
            self.__records = self.__records[
                0:TetrisRankingList.MAX_RANKING_RECORD]

        self._write_ranking_file()

    def _read_ranking_file(self):
        '''Reads ranking list from the file.'''
        try:
            with open(self.__filename, 'r') as file:
                for line in file:
                    vals = line.split(',')
                    self.__records.append((int(vals[1]), vals[0]))
        except FileNotFoundError:
            pass

    def _write_ranking_file(self):
        ''' Updates the file of ranking list'''
        with open(self.__filename, 'w') as file:
            for score, username in self.__records:
                file.write(str(username) + ',' + \
                           str(score) + '\n')
