from IPCalc import IPCalc, InvalidMaskException, InvalidIPException


if __name__ == '__main__':

    try:
        ip = IPCalc(input('Podaj IP: '), input('Podaj Maskę: '))
        print(ip)
    except InvalidMaskException:
        print('Podana maska jest nieprawidłowa')
    except InvalidIPException:
        print('Podany adres IP jest nieprawidłowy')
