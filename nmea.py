# Tällaista on NMEA-data, jota luimme mittareilta. Neljän rivin setti
# tulee kerran sekunnissa

# Vwr on suhteellinen tuuli. Suunta asteina, nopeus kts sekä m/s
# Vwt on tosi tuuli, samat arvot
# Vpw on vmg eli velocity made good, etenemisnopeus kohti merkkiä (datassa 0.00)
# Hdm on magneettinen kulkusuunta

# Tässä ei ole veneen nopeutta, se tulee toisesta sarjapiuhasta, ihan
# samannäköisenä. Itse asiassa silvan vehkeet on tietenkin käyttäneet
# tähän tuulimittarilta tulevan tiedon laskentaan lokitietoakin, mutta
# sitä ei vaan näytetä tässä.

test = [
    '$HCHDM,182,M',
    '$HCHDM,183,M',
    '$HCHDM,183,M',
    '$HCHDM,183,M',
    '$IIVPW,00.00,N,,',
    '$IIVPW,00.00,N,,',
    '$IIVPW,00.00,N,,',
    '$IIVPW,00.00,N,,',
    '$IIVWR,138,R,03.4,N,01.7,M,,',
    '$IIVWR,139,R,03.5,N,01.8,M,,',
    '$IIVWR,139,R,03.6,N,01.8,M,,',
    '$IIVWR,140,R,03.5,N,01.8,M,,',
    '$IIVWR,140,R,03.6,N,01.8,M,,',
    '$IIVWT,139,R,03.3,N,01.6,M,,',
    '$IIVWT,139,R,03.4,N,01.7,M,,',
    '$IIVWT,140,R,03.5,N,01.8,M,,',
    '$IIVWT,141,R,03.6,N,01.8,M,,'
]




class Nmea(str):
    def __init__(self, string):
        args = string.split(',')
        opcode, params = args[0], args[1:]
        self.data = classes[opcode](params)

class Vw(list):
    def __init__(self, params):
        list.__init__(self, params)
        self.wind_speed_and_angle = float(params[0])
        self.wind_side = params[1]
        self.knots = float(params[2])
        self.meters_per_second = float(params[4])
        kmh = params[6]
        if len(kmh) > 0:
            self.kilometers_per_hour = float(kmh)
        else:
            self.kilometers_per_hour = self.meters_per_second * 3600 / 1000



class Vwr(Vw):
    pass

class Vwt(Vw):
    pass

class Vpw(list):
    def __init__(self, params):
        list.__init__(self, params)
        self.knots = float(params[0])
        ms = params[2]
        if len(ms) > 1:
            self.meters_per_second = float(ms)
        else:
            self.meters_per_second = self.knots * 90 * 60 / 10000
        
class Hdm(list):
    def __init__(self, params):
        list.__init__(self, params)
        self.heading = float(params[0])



classes = {
    '$HCHDM': Hdm,
    '$IIVPW': Vpw,
    '$IIVWR': Vwr,
    '$IIVWT': Vwt
}





if __name__ == "__main__":
    import doctest
    doctest.testmod()
