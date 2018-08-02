"""Static operators for xml parsing."""

import os
import shutil

def clear_destination(path):
    """Identify if file exists. If so, remove it."""

    if os.path.isfile(path):
        if os.path.exists(path):
            os.remove(path)

    elif os.path.isdir(path):
        if os.path.exists(path):
            # accounts for OS error in fully deleting dir. in time.
            try:
                shutil.rmtree(path)
            except:
                shutil.rmtree(path)

def none_to_empty(word):
    """Reassign NoneType objects to empty strings."""

    if not word:
        word = ''
    else:
        word = word
    return word

def data_to_csv(data_input, clean, full, out_path, out_fiche, out_page, head, foot, data_type):
    """Export dataframe or series as .csv file."""

    save_path = find_unique_id(clean, full, out_path, out_fiche, out_page, data_type, 'csv')
    data_input.to_csv(save_path, header=head, index=foot)

def find_unique_id(clean_table, full, out_path, out_fiche, out_page, data_type, extension):

    def identify_id(i, clean_table, full, extension):
        """Identify count ID of table per page such that save path is unique."""

        # prepare path for clean tables.
        if clean_table:
            if full:
                table_id = '{}-{}-{}_table_clean_full_{}.{}'.format(out_fiche, out_page,
                                                                    str(i).zfill(2), data_type,
                                                                    extension)
            else:
                table_id = '{}-{}-{}_table_clean_part_{}.{}'.format(out_fiche, out_page,
                                                                    str(i).zfill(2), data_type,
                                                                    extension)
        # prepare path for non-clean tables.
        else:
            if full:
                table_id = '{}-{}-{}_table_imperfect_full_{}.{}'.format(out_fiche, out_page,
                                                                        str(i).zfill(2),
                                                                        data_type, extension)
            else:
                table_id = '{}-{}-{}_table_imperfect_part_{}.{}'.format(out_fiche, out_page,
                                                                        str(i).zfill(2),
                                                                        data_type, extension)

        return table_id

    # define iteration beginning and default path_found value.
    i = 1
    path_found = True

    # loop until a table index for the specific page-fiche combination is not found.
    # return the unique save path, combining the unique table index with other path strings.

    while path_found == True:
        table_id = identify_id(i, clean_table, full, extension)
        save_path = os.path.join(out_path, table_id)
        if not os.path.exists(save_path):
            path_found = False

        i += 1

    return save_path
