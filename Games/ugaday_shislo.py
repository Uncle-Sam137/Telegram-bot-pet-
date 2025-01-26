async def play(n, state):
    data = await state.get_data()
    x = data.get('iskomoe')
    tries = data.get('tries')
    try:
        n = int(n)
    except:
        return 'Вводить нужно число'
    await state.update_data(iskomoe=x, tries=tries+1)

    if n > x:
        return 'Слишком много, попробуй еще раз'
    elif n < x:
        return 'Слишком мало, попробуй еще раз'

    return 'Вы угадали, поздравляю!'