import pandas as pd
import os
import nif_corrector

col_cod_fil = 'cl_codfiliacion'
col_nif = 'cl_nif'
col_tipo_doc = 'cl_cod_tipodoc'


def first_process_file(path, separator = ';'):
    file_df = pd.read_csv(path, sep = separator, dtype={'cl_codfiliacion':'str'}, encoding='latin1')

    for index, row in file_df.iterrows():
        tipo_doc = row[col_tipo_doc]
        nif = row[col_nif]
        try:
            import sys

            sys.stdout = open(os.devnull, 'w')
            doc_output, correct, reason, type_id = nif_corrector.id_conversor(tipo_doc, nif)
            sys.stdout = sys.__stdout__
        except:
            correct = False
        print(index)
        file_df.loc[index, 'correct_id'] = correct
        file_df.loc[index, 'type_id'] = type_id

    file_df.to_csv('file_processed.csv', sep = ';', index = False)



def process_file(input, path_output, separator = ';'):

    first_process_file(input, separator=separator)

    file_df_processed = pd.read_csv('file_processed.csv', sep=separator, encoding = 'latin1', dtype={'cl_codfiliacion':'str'})
    file_df_processed[col_cod_fil] = file_df_processed[col_cod_fil].apply(lambda x: x.zfill(10))

    file_df_processed['cod_global_unico'] = pd.Series(0,
                                                      index=file_df_processed.index)

    file_df_processed['cod_global_unico'] = file_df_processed.apply(
        lambda x: x['cl_nif']
        if x['correct_id'] == True
        else x['cl_codfiliacion'], axis=1)

    file_df_processed['cod_fil_repetido'] = pd.Series(0, index=file_df_processed.index)

    file_df_processed['cod_fil_repetido'] = file_df_processed.groupby('cod_global_unico')['cod_global_unico'].transform('count')

    file_df_processed.to_csv(path_output, sep = separator, quotechar='"', encoding='latin1', index= False)


