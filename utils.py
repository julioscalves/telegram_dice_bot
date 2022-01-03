import random
import re


def assemble_message(result: dict):
    if 'total_with_modifiers' in result.keys():
        if type(result['modifier_roll']) == list:
            modifier = sum(result['modifier_roll'])
        
        else:
            modifier = result['modifier_roll']
            
        mod_sign = '-' if modifier  < 0 else '+'
        message = (
            f'({result["roll"]}) {mod_sign} ({result["modifier_roll"]}): [{result["total"]+result["modifier_total"]}]'
        )

    else:
        message = (
            f'{result["roll"]}: [{result["total"]}]'
        )

    return message


def parse_wod(text: str) -> dict:
    try:
        command = text.split()

        if len(command) == 2:
            dice_number = int(command[-1])
            difficulty = 6

        else:
            dice_number = int(command[-2])
            difficulty = int(command[-1])

        return wod(dice_number, difficulty)

    except:
        return {
            'status': 'fail'
        } 
    

def wod(dice_number: int, difficulty: int) -> dict:
    result = {}

    roll = [random.randint(1, 10) for _ in range(dice_number)]
    successes = list(filter(lambda x: x >= difficulty, roll))

    result['status'] = 'success'
    result['roll'] = roll
    result['total'] = len(successes) - roll.count(1)

    return result


def handle_modifiers(modifier: int, main_roll: int) -> dict:
    result = roll_dice(modifier[1:])
    print(result)

    return {
        'modifier_roll': result['roll'],
        'modifier_total': result['total']
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
            modifier_roll = handle_modifiers(modifiers, dice_roll)
        else:
            modifier_roll = {
              'modifier_roll': int(modifiers),
              'modifier_total': int(modifiers)
            }

        result = {
            **dice_roll,
            **modifier_roll
        }

        result['total_with_modifiers'] = result['total'] + modifier_roll['modifier_total']

    else:
        result = {
            **dice_roll
        }

    return result
