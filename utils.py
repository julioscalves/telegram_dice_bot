import random
import re


def assemble_message(result: dict):
    if 'total_with_modifiers' in result.keys():
        mod_sign = '-' if result['modifier_roll'] < 0 else '+'
        
        message = (
            f'([{result["roll"]}]) {mod_sign} ([{result["modifier_roll"]}]): [{result["total"]+result["modifier_total"]}]'
        )

    else:
        message = (
            f'[{result["roll"]}]: [{result["total"]}]'
        )

    return message


def parse_wod(text: str) -> dict:
    command = text.split()

    if len(command) == 2:
        dice_number = int(command[-1])
        difficulty = 6

    else:
        dice_number = int(command[-2])
        difficulty = int(command[-1])

    return wod(dice_number, difficulty)
    

def wod(dice_number: int, difficulty: int) -> dict:
    result = {}

    roll = [random.randint(1, 10) for _ in range(dice_number)]
    successes = filter(lambda x: x >= difficulty, roll)

    result['status'] = 'success'
    result['roll'] = roll
    result['success'] = len(successes)

    return result


def handle_modifiers(modifier: int, main_roll: int) -> dict:
    result = roll_dice(modifier[1:])

    return {
        'modifier_roll': result,
        'modifier_total': sum(modifier)
    }


def roll_dice(dices: str) -> dict:
    dice_number, dice_type = dices.split('d')
    dice_number, dice_type = int(dice_number), int(dice_type)

    roll = [random.randint(1, dice_type) for _ in range(dice_number)]

    return {
        'roll': roll,
        'total': sum(roll)
    }

def parse_dice(text: str) -> dict:
    result = {}
    command = text.split()
    dice_command = command[-1]

    dice_pattern = re.compile('([0-9]+d[0-9]+)')
    dices = dice_pattern.match(dice_command).group()
    modifiers = dice_command.replace(dices, '')

    dice_roll = roll_dice(dices)

    if len(modifiers) > 0:
        if 'd' in modifiers:
            modifier_roll = handle_modifiers()
        else:
            modifier_roll = int(modifiers)

        result = {
            *dices,
            *modifier_roll
        }

        result['total_with_modifiers'] = result['total'] + modifier_roll['total']

    else:
        result = {
            *dices
        }

    return result
