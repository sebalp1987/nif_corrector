from unidecode import unidecode
import re
import csv


symbols = '[!@#$.,-]'

#NIF (8 numeros y una letra)
#TIE
#Pasaporte


def id_conversor(tipo_doc, numero_doc):


    print('----------------------------------------------------------------------------')
    print('----------------------------------------------------------------------------')

    print(' ')

    print('ID a Analizar: ', tipo_doc + ' ' + numero_doc)
    print(' ')

    output = []

    if tipo_doc == 'C':
        doc_output, correct, reason = CIF_conversor(numero_doc)
        type_id = 'CIF'

    if tipo_doc == 'N' or tipo_doc == 'R':
        doc_output, correct, reason, type_id = NIF_conversor(numero_doc)

    if tipo_doc == 'P':
        print('Es un Pasaporte, imposible verificación')
        doc_output = str(numero_doc)
        doc_output = unidecode(doc_output)
        doc_output = doc_output.upper()
        doc_output = re.sub(symbols, '', doc_output)
        correct = False
        reason = ''
        type_id = 'Pasaporte'

    if tipo_doc == 'S' or tipo_doc == 'T':
        print('Toma valores no identificables')
        doc_output = 'N/A'
        correct = False
        reason = 'No Identificable'
        type_id = 'No Identificable'

    if tipo_doc == 'E':
        print('Empresa Extranjera de la CEE')
        doc_output = str(numero_doc)
        doc_output = unidecode(doc_output)
        doc_output = doc_output.upper()
        doc_output = re.sub(symbols, '', doc_output)
        correct = False
        reason = 'Empresa Extranjera de la CEE'
        type_id = 'Ext. CEE'

    if tipo_doc == 'X':
        print('Empresa Extranjera que no es de la CEE')
        doc_output = str(numero_doc)
        doc_output = unidecode(doc_output)
        doc_output = doc_output.upper()
        doc_output = re.sub(symbols, '', doc_output)
        correct = False
        reason = 'Empresa Extranjera que no es de la CEE'
        type_id = 'Ext. no CEE'






    return doc_output, correct, reason, type_id

def CIF_conversor(numero_doc):

    #https://es.wikipedia.org/wiki/C%C3%B3digo_de_identificaci%C3%B3n_fiscal

    doc_output =''
    correct = False
    reason = ''

    numero_doc = str(numero_doc)
    numero_doc = unidecode(numero_doc)
    numero_doc = numero_doc.upper()
    numero_doc = re.sub(symbols, '', numero_doc)

    length = 9

    first_character = ['A','B','C','D','E','F','G','H',
                       'J','N','P','Q','R','S','U','V','W']

    second_third_char = ['00','01','02','03','53','54',
                         '04','05','06','07','57','08','58',
                         '59','60','61','62','63','64','65',
                         '66','68','09','10','11','72','12',
                         '13','14','56','15','70', '16', '17','55','18','19',
                         '20','71','21','22','23','24','25','26','27',
                         '28','78','79','80','81','82','83','84','85','86',
                         '87','29','92','93','30','73','31','32',
                         '33','74','34','35','76','36','94','37','38','75','39',
                         '40','41','90','91','42','43','77','44','45','46','96',
                         '97','98','47','48','95','49','50','99','51','52']



    #REGLAS

    if len(numero_doc) != length:
        print('Length is not correct')
        doc_output = 'N/A'
        correct = False
        reason = 'Bad Length'

    else:
        num0 = numero_doc[0]
        num12 = numero_doc[1] + numero_doc[2]

        num_centrales_pares = numero_doc[2] + numero_doc[4] + numero_doc[6]
        num_centrales_impar = numero_doc[1] + numero_doc[3] + numero_doc[5] + numero_doc[7]


        num_last = numero_doc[-1]



        if num12 not in second_third_char:
            print('Second and Third Numbers do not match with a Province ID')
            doc_output = 'N/A'
            correct = False
            reason = 'Bad Second and Third Number'

        elif (num0 in ['P','Q','S','W'] or num12 == '00') and type(num_last) == int:
            print(type(num_last))
            print('Control Number is Bad Typo, it has to be a letter')
            doc_output = 'N/A'
            correct = False
            reason = 'CN must be letter'


        elif num0 in ['A','B','E','H'] and type(int(num_last)) == str:
            print('Control Number is Bad Typo, it has to be a Number')
            doc_output = 'N/A'
            correct = False
            reason = 'CN must be numeric'


        else:
            # Valor Numero de Control (num_last)
            suma_par = 0
            for i in num_centrales_pares:
                i = int(i)
                suma_par += i

            suma_impar = 0
            for i in num_centrales_impar:
                i = int(i)
                i = i * 2
                s = 0
                while i:
                    s += i % 10
                    i //= 10
                suma_impar += s

            suma_total = suma_par + suma_impar
            suma_total = str(suma_total)
            last_suma = 10 - int(suma_total[-1])
            last_suma = str(last_suma)
            last_suma = int(last_suma[-1])


            if int(num_last.isdigit() == True):
                if int(num_last) == last_suma:
                    print('Number is correctly Assigned')
                    doc_output = numero_doc
                    correct = True
                    reason = ''


                else:
                    print('Last Number is bad Calculated')
                    doc_output = 'N/A'
                    correct = False
                    reason = 'CN Bad Calculated'

            else:
                num = ['P', 'Q', 'S', 'W']
                if (num0 in num) or (num12 == '00'):
                    print('Number is correctly Assigned')
                    doc_output = numero_doc
                    correct = True
                    reason = ''

                else:
                    if num_last.isalpha():
                        print('Number is correctly Assigned')
                        doc_output = numero_doc
                        correct = True
                        reason = ''



    return doc_output, correct, reason




def NIF_conversor(numero_doc):

    #https: // es.wikipedia.org / wiki / N % C3 % BAmero_de_identificaci % C3 % B3n_fiscal

    doc_output = ''
    correct = True
    reason = ''
    type_id = ''



    numero_doc = str(numero_doc)
    numero_doc = unidecode(numero_doc)
    numero_doc = numero_doc.upper()
    numero_doc = re.sub(symbols, '', numero_doc)

    num0 = numero_doc[0]
    numerical_values = numero_doc[1:-1]
    last_num = numero_doc[-1]

    num_control = {0:'T', 1:'R', 2:'W', 3:'A', 4:'G', 5:'M', 6:'Y', 7:'F', 8:'P',
                   9:'D', 10:'X', 11:'B', 12:'N', 13:'J', 14:'Z', 15:'S', 16:'Q',
                   17:'V', 18:'H', 19:'L', 20:'C', 21:'K', 22:'E'}

    lenght = 9

    if num0.isalpha() == False:
        type_id = 'ID español'
        print(type_id)
    elif num0 == 'K':
        type_id = 'Español menor de 14 años, sin DNI'
        print(type_id)
    elif num0 == 'L':
        type_id = 'Español mayor de 14 años sin NIE'
        print(type_id)
    elif num0 == 'M':
        type_id = 'Extranjero sin NIE'
        print(type_id)
    elif num0 == 'X' or num0 == 'Y' or num0 =='Z':
        type_id = 'Extranjero con NIE'
        print(type_id)
    else:
        type_id = 'No corresponde a un NIF válido'
        print(type_id)
        doc_output = 'N/A'
        correct = False
        reason = 'Not Valid ID'


    #REGLAS:

    if len(numero_doc) != 9:
        print('Length is not correct')
        doc_output = 'N/A'
        correct = False
        reason = 'Bad Length'

    elif num0 == 'K' or num0 == 'L':
        print('Underage person')
        doc_output = 'N/A'
        correct = False
        reason = 'Underage person < 18 years'

    elif num0 =='M':
        print('Foreigner without NIE')
        correct = True
        reason = ''

    elif int(numerical_values.isdigit() == False):
        print('Non numerical Values')
        doc_output = 'N/A'
        correct = False
        reason = 'Non-numerical Values'


    elif int(numerical_values.isdigit() == True):
        numerical_values = int(numerical_values)
        if num0.isdigit() == True:
            num0 = num0
        elif num0.isalpha() == True:
            if num0 == 'X':
                num0 = 0
            elif num0 == 'Y':
                num0 = 1
            elif num0 == 'Z':
                num0 = 2

        numerical_values = str(numerical_values)
        if len(numerical_values)< 7:
            numerical_values = numerical_values.rjust(7,'0')

        num = str(num0)+numerical_values

        letter = "TRWAGMYFPDXBNJZSQVHLCKE"[int(num)%23]

        if str(last_num) == str(letter):
            print('Number is correctly Assigned')
            doc_output = numero_doc
            correct = True
            reason = ''

        else:
            print('Last Number is bad Calculated')
            doc_output = 'N/A'
            correct = False
            reason = 'CN Bad Calculated'

    return doc_output, correct, reason, type_id

