from lib.getInput import getInput
from collections import defaultdict
# URL: https://adventofcode.com/2024/day/5

class Rule:
    def __init__(self):
        self.before = set()
        self.after = set()
    
    def __str__(self):
        return f"{self.before} {self.after}"

def mapRules(rules_list):
    rules = defaultdict(Rule)
    for rule in rules_list:
        goes_before, goes_after = rule.split("|")
        rules[goes_before].after.add(goes_after)
        rules[goes_after].before.add(goes_before)
    return rules


def fetchPages(rules, pages, take_valid_pages = True):
    def isValidNumber(rules, numbers, index, number):
        left, right = index - 1, index + 1


        is_valid = True
        while left >= 0:
            check_number = numbers[left]
            if check_number in rules[number].after:
                is_valid = False
            left -= 1
            
        while right < len(numbers):
            check_number = numbers[right]

            if check_number in rules[number].before:
                is_valid = False

            right += 1

        return is_valid

    result = []
    for page in pages:
        numbers = page.split(",")
        is_valid = True

        for number_index, number in enumerate(numbers):
            if not isValidNumber(rules, numbers, number_index, number):
                is_valid = False

        if (
            (take_valid_pages and is_valid) or 
            (not take_valid_pages and not is_valid)
        ):
            result.append(numbers)

    return result
    
def sortPages(rules, pages):
    result = []
    for page in pages:
        sorted = []
        numbers = set(page)
        while len(numbers) > 0:
            for number in numbers:
                valid_position = True

                for checked_number in numbers:
                    if number == checked_number:
                        continue
                        
                    if number in rules[checked_number].after:
                        valid_position = False
                        break

                if valid_position:
                    sorted.append(number)
                    numbers.remove(number)
                    break
        result.append(sorted)
    return result

def countMiddleNumbers(pages):
    number = 0
    for page in pages:
        number += int(page[(len(page) // 2)])
    return number

def Q1(rules, pages):
    '''The Elf must recognize you, because they waste no time explaining that the new sleigh launch safety manual updates won't print correctly. Failure to update the safety manuals would be dire indeed, so you offer your services.

    Safety protocols clearly indicate that new pages for the safety manuals must be printed in a very specific order. The notation X|Y means that if both page number X and page number Y are to be produced as part of an update, page number X must be printed at some point before page number Y.

    The Elf has for you both the page ordering rules and the pages to produce in each update (your puzzle input), but can't figure out whether each update has the pages in the right order.

    For example:

    47|53
    97|13
    97|61
    97|47
    75|29
    61|13
    75|53
    29|13
    97|29
    53|29
    61|53
    97|53
    61|29
    47|13
    75|47
    97|75
    47|61
    75|61
    47|29
    75|13
    53|13

    75,47,61,53,29
    97,61,53,29,13
    75,29,13
    75,97,47,61,53
    61,13,29
    97,13,75,29,47
    The first section specifies the page ordering rules, one per line. The first rule, 47|53, means that if an update includes both page number 47 and page number 53, then page number 47 must be printed at some point before page number 53. (47 doesn't necessarily need to be immediately before 53; other pages are allowed to be between them.)

    The second section specifies the page numbers of each update. Because most safety manuals are different, the pages needed in the updates are different too. The first update, 75,47,61,53,29, means that the update consists of page numbers 75, 47, 61, 53, and 29.

    To get the printers going as soon as possible, start by identifying which updates are already in the right order.

    In the above example, the first update (75,47,61,53,29) is in the right order:

    75 is correctly first because there are rules that put each other page after it: 75|47, 75|61, 75|53, and 75|29.
    47 is correctly second because 75 must be before it (75|47) and every other page must be after it according to 47|61, 47|53, and 47|29.
    61 is correctly in the middle because 75 and 47 are before it (75|61 and 47|61) and 53 and 29 are after it (61|53 and 61|29).
    53 is correctly fourth because it is before page number 29 (53|29).
    29 is the only page left and so is correctly last.
    Because the first update does not include some page numbers, the ordering rules involving those missing page numbers are ignored.

    The second and third updates are also in the correct order according to the rules. Like the first update, they also do not include every page number, and so only some of the ordering rules apply - within each update, the ordering rules that involve missing page numbers are not used.

    The fourth update, 75,97,47,61,53, is not in the correct order: it would print 75 before 97, which violates the rule 97|75.

    The fifth update, 61,13,29, is also not in the correct order, since it breaks the rule 29|13.

    The last update, 97,13,75,29,47, is not in the correct order due to breaking several rules.

    For some reason, the Elves also need to know the middle page number of each update being printed. Because you are currently only printing the correctly-ordered updates, you will need to find the middle page number of each correctly-ordered update. In the above example, the correctly-ordered updates are:

    75,47,61,53,29
    97,61,53,29,13
    75,29,13
    These have middle page numbers of 61, 53, and 29 respectively. Adding these page numbers together gives 143.

    Of course, you'll need to be careful: the actual list of page ordering rules is bigger and more complicated than the above example.

    Determine which updates are already in the correct order. What do you get if you add up the middle page number from those correctly-ordered updates?
    '''
    mapped_rules = mapRules(rules)
    valid_pages = fetchPages(mapped_rules, pages)
    return countMiddleNumbers(valid_pages)

def Q2(rules, pages):
    '''For each of the incorrectly-ordered updates, use the page ordering rules to put the page numbers in the right order. For the above example, here are the three incorrectly-ordered updates and their correct orderings:

    75,97,47,61,53 becomes 97,75,47,61,53.
    61,13,29 becomes 61,29,13.
    97,13,75,29,47 becomes 97,75,47,29,13.
    After taking only the incorrectly-ordered updates and ordering them correctly, their middle page numbers are 47, 29, and 47. Adding these together produces 123.

    Find the updates which are not in the correct order. What do you get if you add up the middle page numbers after correctly ordering just those updates?
    '''
    mapped_rules = mapRules(rules)
    invalid_pages = fetchPages(mapped_rules, pages, False)
    sorted_pages = sortPages(mapped_rules, invalid_pages)
    return countMiddleNumbers(sorted_pages)

rules = getInput("5a")
pages = getInput("5b")

print( Q1(rules, pages) )
print( Q2(rules, pages) )