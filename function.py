def hitung_xy(vektor, kasusBaru):
    total = 0
    for i in range(len(kasusBaru)):
        total += vektor[i] * kasusBaru[i]
    return total

def hitung_bawah(data):
    total = 0
    for nilai in data:
        total += nilai * nilai
    hasil = total ** 0.5
    return hasil

def hitung_cosine(vektor, kasusBaru):
    xy = hitung_xy(vektor, kasusBaru)
    x = hitung_bawah(vektor)
    y = hitung_bawah(kasusBaru)
    if y == 0:
        return 0
    hasil_cosine = xy / (x * y)
    return hasil_cosine