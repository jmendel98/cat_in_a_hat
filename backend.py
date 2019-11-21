def char_by_char( input_string, pixel_cnt):
    "This function outputs data files for character by character display, binary atm"
    STRING_LENGTH = len(input_string)
    for ctr in range(0, STRING_LENGTH):
        ##EFFECTIVE CASE STATEMENT THAT PICKS THE RIGHT FILE FOR A CHARACTER
        char = input_string[ctr]
        if char in ['A', 'a']:
            temp_char_data = open(".\\Char_Images\\A.txt", "r").read().splitlines()
        elif char in ['B', 'b']:
            temp_char_data = open(".\\Char_Images\\B.txt", "r").read().splitlines()
        elif char in ['C', 'c']:
            temp_char_data = open(".\\Char_Images\\C.txt", "r").read().splitlines()
        elif char in ['D', 'd']:
            temp_char_data = open(".\\Char_Images\\D.txt", "r").read().splitlines()
        elif char in ['E', 'e']:
            temp_char_data = open(".\\Char_Images\\E.txt", "r").read().splitlines()
        elif char in ['F', 'f']:
            temp_char_data = open(".\\Char_Images\\F.txt", "r").read().splitlines()
        elif char in ['G', 'g']:
            temp_char_data = open(".\\Char_Images\\G.txt", "r").read().splitlines()
        elif char in ['H', 'h']:
            temp_char_data = open(".\\Char_Images\\H.txt", "r").read().splitlines()
        elif char in ['I', 'i']:
            temp_char_data = open(".\\Char_Images\\I.txt", "r").read().splitlines()
        elif char in ['J', 'j']:
            temp_char_data = open(".\\Char_Images\\J.txt", "r").read().splitlines()
        elif char in ['K', 'k']:
            temp_char_data = open(".\\Char_Images\\K.txt", "r").read().splitlines()
        elif char in ['L', 'l']:
            temp_char_data = open(".\\Char_Images\\L.txt", "r").read().splitlines()
        elif char in ['M', 'm']:
            temp_char_data = open(".\\Char_Images\\M.txt", "r").read().splitlines()
        elif char in ['N', 'n']:
            temp_char_data = open(".\\Char_Images\\N.txt", "r").read().splitlines()
        elif char in ['O', 'o']:
            temp_char_data = open(".\\Char_Images\\O.txt", "r").read().splitlines()
        elif char in ['p', 'p']:
            temp_char_data = open(".\\Char_Images\\P.txt", "r").read().splitlines()
        elif char in ['Q', 'q']:
            temp_char_data = open(".\\Char_Images\\Q.txt", "r").read().splitlines()
        elif char in ['R', 'r']:
            temp_char_data = open(".\\Char_Images\\R.txt", "r").read().splitlines()
        elif char in ['S', 's']:
            temp_char_data = open(".\\Char_Images\\S.txt", "r").read().splitlines()
        elif char in ['T', 't']:
            temp_char_data = open(".\\Char_Images\\T.txt", "r").read().splitlines()
        elif char in ['U', 'u']:
            temp_char_data = open(".\\Char_Images\\U.txt", "r").read().splitlines()
        elif char in ['V', 'v']:
            temp_char_data = open(".\\Char_Images\\V.txt", "r").read().splitlines()
        elif char in ['W', 'w']:
            temp_char_data = open(".\\Char_Images\\W.txt", "r").read().splitlines()
        elif char in ['X', 'x']:
            temp_char_data = open(".\\Char_Images\\X.txt", "r").read().splitlines()
        elif char in ['Y', 'y']:
            temp_char_data = open(".\\Char_Images\\Y.txt", "r").read().splitlines()                
        elif char in ['Z', 'z']:
            temp_char_data = open(".\\Char_Images\\Z.txt", "r").read().splitlines()
        elif char in [' ']:
            temp_char_data = open(".\\Char_Images\\space.txt", "r").read().splitlines()
        elif char in ['*']:
            temp_char_data = open(".\\Char_Images\checker1.txt", "r").read().splitlines()
        elif char in ['^']:
            temp_char_data = open(".\\Char_Images\\checker2.txt", "r").read().splitlines()
        ##FOR LOOP TO DESIGNATE THE ACTUAL INFORMATION TO THE INDIVIDUAL FILES    
        char_data = ''
        char_data = char_data.join(temp_char_data)
        for index in range (0, pixel_cnt):
            file_name = ".\\Hat_Data_Files\\pixel_data_hat"+ str(index+1) + ".txt"
            if char_data[index] in ['X']:
                open(file_name, "a").write('1')
            else:
                open(file_name, "a").write('0')
                
##Start of main funtion        
HEIGHT = input('Enter height of image: ')
WIDTH = input('Enter width of image:' )
Hat_Count = int(HEIGHT)*int(WIDTH)

for ctr in range (0, Hat_Count):
    file_name = ".\\Hat_Data_Files\\pixel_data_hat"+ str(ctr+1) + ".txt"
    f = open(file_name, "w+")
    
INPUT_STRING = input('Input string to be displayed:')

char_by_char(INPUT_STRING, Hat_Count)