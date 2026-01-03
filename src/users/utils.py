def get_largest_serial_number_from_ids(id_list):
    """
    Given a list of IDs in the format 'OIJODO20220001' where the last 4 characters are the zero-padded serial number,
    return the largest serial number as an integer.
    """
    max_serial = 0
    for id_str in id_list:
        try:
            if len(id_str) >= 4:
                serial_str = id_str[-4:]
                serial_num = int(serial_str)
                if serial_num > max_serial:
                    max_serial = serial_num
        except ValueError:
            continue
    return max_serial
