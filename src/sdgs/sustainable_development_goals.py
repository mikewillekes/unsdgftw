import codecs
import csv
from csv import DictReader
from dataclasses import dataclass

# Local application imports
from config import config

"""https://unstats.un.org/sdgs/report/2021/"""


@dataclass
class SustainableDevelopmentGoal:
    goal_category_num: str
    goal_category_short: str
    goal_category_long: str
    goal_sub_category:str
    goal_num: str
    goal: str

def load_sdgs():
    """Load the full set of all SDGs"""

    sdgs = []
    
    # This CSV file was generated in Excel. It's utf-8 with a BOM (byte-order-mark)
    # so we need to specify the correct encoding.
    # See: https://stackoverflow.com/a/60614459
    with codecs.open(config.SDGS_FILENAME, 'r', encoding='utf-8-sig') as fp:
        reader = DictReader(fp)
        for record in reader:
            sdgs.append(
                SustainableDevelopmentGoal(
                    record['goal_category_num'],
                    record['goal_category_short'],
                    record['goal_category_long'],
                    record['goal_sub_category'],
                    record['goal_num'],
                    record['goal']
                )
            )
    return sdgs


def main(): 
    for goal in load_sdgs():
        print(f'{goal.goal_num} >> {goal.goal}')


if __name__ == "__main__":
    main()