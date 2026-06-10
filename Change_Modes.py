import machine


class Modes:
    def __init__(self):
        self.Mode="sport"
    # Mode setup
    def Get_Mode_Settings(self,switch):
        if switch==100:
            self.Mode="sport"
        elif switch==50:
            self.Mode="climb"
        else:
            self.Mode="sport"
#         print(f"Selected Mode={self.Mode}")
        
        if self.Mode=="sport":
            return{
                "Max_Speed":        1,
                "Maximum_Angle":    60 ,
                "Minimum_Angle":    30,
                "Step":             30,
                "Delay":            10, 
            }
        
        if self.Mode=="climb":
            return{
                "Max_Speed":        0.6,
                "Maximum_Angle":    90,
                "Minimum_Angle":    0,
                "Step":             5,
                "Delay":            12, 
                "Accel_Delay":      200,
            }


