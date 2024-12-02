from lib.getInput import getInput
# URL: https://adventofcode.com/2024/day/2

def format_reports(reports):
    formatted_reports = []

    for report in reports:
        levels = [int(el) for el in report.replace("\n", "").split(" ") if el != ""]
        formatted_reports.append(levels)

    return formatted_reports


def check_if_safe(report):
    next_level = None
    increments = set()
    is_unsafe = False

    for index,level in enumerate(report):
        #* Get Next Level
        if index + 1 == len(report):
            break
        else:
            next_level = report[index + 1]

        level_diff = level - next_level

        #* Gets Increment if it is at most 3 levels apart
        if level_diff <= 3 and level_diff > 0:
            increments.add("increase")
    
        if level_diff < 0 and level_diff >= -3:
            increments.add("decrease")

        #* Checks If Level Fails due to Level Diff 
        if(
            level_diff == 0 or
            ( abs(level_diff) > 3)
        ):
            is_unsafe = True
                
        #* Check if it fails due to change in increment
        if len(increments) > 1:
            is_unsafe = True    

    return not is_unsafe

def Q1(reports):
    '''The unusual data (your puzzle input) consists of many reports, one report per line. Each report is a list of numbers called levels that are separated by spaces. For example:

    7 6 4 2 1
    1 2 7 8 9
    9 7 6 2 1
    1 3 2 4 5
    8 6 4 4 1
    1 3 6 7 9
    This example data contains six reports each containing five levels.

    The engineers are trying to figure out which reports are safe. The Red-Nosed reactor safety systems can only tolerate levels that are either gradually increasing or gradually decreasing. So, a report only counts as safe if both of the following are true:

    The levels are either all increasing or all decreasing.
    Any two adjacent levels differ by at least one and at most three.
    In the example above, the reports can be found safe or unsafe by checking those rules:

    7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
    1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
    9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
    1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
    8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
    1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.
    So, in this example, 2 reports are safe.

    Analyze the unusual data from the engineers. How many reports are safe?
    '''
    amount_safe = 0

    for report in reports:
        if check_if_safe(report):
            amount_safe += 1

    return amount_safe

def Q2(reports):
    '''The engineers are surprised by the low number of safe reports until they realize they forgot to tell you about the Problem Dampener.

    The Problem Dampener is a reactor-mounted module that lets the reactor safety systems tolerate a single bad level in what would otherwise be a safe report. It's like the bad level never happened!

    Now, the same rules apply as before, except if removing a single level from an unsafe report would make it safe, the report instead counts as safe.

    More of the above example's reports are now safe:

    7 6 4 2 1: Safe without removing any level.
    1 2 7 8 9: Unsafe regardless of which level is removed.
    9 7 6 2 1: Unsafe regardless of which level is removed.
    1 3 2 4 5: Safe by removing the second level, 3.
    8 6 4 4 1: Safe by removing the third level, 4.
    1 3 6 7 9: Safe without removing any level.
    Thanks to the Problem Dampener, 4 reports are actually safe!

    Update your analysis by handling situations where the Problem Dampener can remove a single level from unsafe reports. How many reports are now safe?
    '''
    amount_safe = 0

    
    
    for report in reports:
        if check_if_safe(report):
            amount_safe += 1
        else:
            #* When in doubt just remove everything I guess (WTF?)
            for index in range(len(report)):
                new_report = report.copy()
                new_report.pop(index)

                if check_if_safe(new_report):
                    amount_safe += 1
                    break

    return amount_safe

reports = format_reports(getInput("2"))
print( Q1(reports) )
print( Q2(reports) )