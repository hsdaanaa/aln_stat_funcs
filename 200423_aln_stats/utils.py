import os
#----------------------------------------------------------------------------------------------------------------
def get_file_paths_from_dir(dir_path, ext = None):
    """takes an input directory and returns
    a list of files in that directory. given
    an input file extension, only files with
    that ext. are included in the list.
    
    parameters
    ----------
    input_cwd: str
       path to directory
    ext: None
       extension to use to filter for file types
    verbose: 0,1
        set to 1 for debugging
    
    returns
    -------
    list"""
    
    # checks if input type is valid
    assert isinstance(dir_path, str), 'your input path was not a string'
    assert os.path.isdir(dir_path) == True, 'your input directory was invalid'

    list_of_files = []
    # get files and folder in cwd
    dir_path = os.path.abspath(dir_path)
    files_folders_in_cwd = os.listdir(dir_path)
    
    # loops over file_folder list and appends file
    # names to list, if ext is specified by the user,
    # only files with the .ext are appended to the list.
    # otherwise, all files are appended to the list.
    for item in files_folders_in_cwd:
        path_to_item = os.path.join(dir_path, item) # allows returning full path of file
        
        if os.path.isfile(path_to_item) == True: 
            if ext != None:    # this allows filtering for files with specific exts.
                
                if type(ext) == list: # this allows fetching files with different .exts
                    for extension in ext:
                        if item.endswith(extension):
                            list_of_files.append(path_to_item)
                else:
                    item.endswith(ext)
                    list_of_files.append(path_to_item)
            else:
                list_of_files.append(path_to_item)

    return list_of_files
#----------------------------------------------------------------------------------------------------------------
def substring_delim(parent_str, delim1, delim2, start_pos_search, include_delim_if_firspos = False, verbose = 0, get_type = 'str'):
    """
    parses a string between two delimiter strings
    input: parent string to search, delimiters 1 and 2 and pos within string to start search
    return: parsed string and position of last delimiter
        this allows parsing the next item from the second limiter if necessary
        return pos is -1 for cases in which the delimiters are not found
    delim1 == "firstpos"
        parse from first position in string to delim2
    delim2 == "endpos"
        parse from delim2 to end of string
	verbose is an optional parameter, set to one for extra output (for debugging)
    get_type is an optional parameter, set 'int'/'float' for integer/float output from substring.
        
    general strategy: 
        get endpos of delim1 and startpos of delim2
        parse betw delimiters
        return substring and startpos of delim2
        handle firstpos and lastpos and errors
	note:
		should confirm:
			parent_str, delim1, delim2 are strings
			start_pos_search is an int
			start_pos_search is within parent_str?
    """
        
    if (verbose == 1):
        print("\n-------- within substring_delim function -----------")

	# check for improper inputs (copied from Hassan's code)
    assert isinstance(parent_str, str), 'ValueError: Input string must be str.' #raises error if parent_str0 not str.
    assert isinstance(start_pos_search, int), 'Search index must be int.' #raises error if pos not int.
    assert start_pos_search < len(parent_str),'start_pos out of parent_str range' #raises error if search pos not in range of parent_str.
    assert isinstance(delim1, str), 'Delimiter 1 must be str' #raises error if delimiter not string.
    assert isinstance(delim2, str), 'Delimiter 2 must be str' #raises error if delimiter not string.

    if (verbose == 1):
        print("str_sample: " + parent_str)
        print("delim1: " + delim1)
        
   # get delim1 start and end
    if (delim1 == "firstpos"):
        delim1_stpos = 0
        delim1_endpos = 0
    else:
        delim1_stpos = parent_str.find(delim1, start_pos_search, len(parent_str))
        delim1_endpos = delim1_stpos + len(delim1) - 1
        if (delim1_stpos < 0):
            print("delim1: " + delim1 + " not found in " + parent_str)
            return "", -1
        
    if (verbose == 1):
        print("delim1_stpos = " + str(delim1_stpos))
        print("delim1_endpos = " + str(delim1_endpos))
        print("str_sample: " + parent_str)
        print("delim2: " + delim2)
        
   # get delim2 start and end
    if (delim2 == "lastpos"):
        delim2_stpos = len(parent_str)
        delim2_endpos = len(parent_str)
    else:
        delim2_stpos = parent_str.find(delim2, delim1_endpos + 1, len(parent_str))  # delim2 must come after delim1
        delim2_endpos = delim2_stpos + len(delim2) - 1
        if (delim2_stpos < 0):
            print("delim2: " + delim2 + " not found in " + parent_str)
            return "", -1
        
    if (verbose == 1):
        print("delim2_stpos = " + str(delim2_stpos))
        print("delim2_endpos = " + str(delim2_endpos))

    # extract substring from parent_str from (delim1_endpos + 1) to (delim2_stpos - 1) - beware of how the limits are coded
    if include_delim_if_firspos == True:
        if (delim1 == "firstpos") == True:
            sub_str = parent_str[delim1_endpos:delim2_stpos]
    else:
        sub_str = parent_str[delim1_endpos + 1:delim2_stpos]

    
    if (verbose == 1):
        print("extract start: " + str(delim1_endpos + 1))
        print("extract end: " + str(delim2_stpos))
        print("extracted search string: " + sub_str)
        print("-------- end substring_delim function -----------\n")
        
    
    if get_type == 'str':                      # str default
        
        return sub_str, delim2_stpos
       
        
    # tests if sub_str found is float, if true, extacts as float, otherwise error.
    elif get_type == 'float': 
        
        try:                                   
            if '.' in sub_str:                    # floats type always contain '.'
                sub_str = float(sub_str)      

                return sub_str, delim2_stpos

            else:                                  # handles error if '.' not found; can't be float.
                print('ValueError: substring not float')

        except ValueError:                         # handles error if sub_string is str; can't be converted to float
            print('ValueError: substring not float')

            
    # tests if sub_string found is int, if true, extracts as int type, otherwise error. 
    elif get_type == 'int':
        
        try:
            if not '.' in sub_str:      # int type never contain '.'s
                sub_str = int(sub_str)    
                
                return sub_str, delim2_stpos  
            
            else:                                         # handles error if '.' found; can't be int.
                print('ValueError: substring not int')
                
        except ValueError:                                # handles error if sub_string is str; can't be converted to int
            print('ValueError: substring not int')       
#----------------------------------------------------------------------------------------------------------------
def cds_to_dict(input_path, delim2, delim1 = '>', verbose = 0):
    """takes an input path to a fasta file and delimiters between 
    an identifier, creates a dictionary with identifier: sequence"""
    
    cds_seq_dict = {}

    with open(input_path, 'r') as file:
        for line in file:
            if line.startswith(delim1):
                cds_name, pos = substring_delim(line, delim1, delim2, 0)
                cds_name = cds_name.rstrip('\n')
                key = line[1:].rstrip('\n')
                cds_seq_dict[cds_name] = ''
            else:
                cds_seq_dict[cds_name] += line.rstrip('\n')
            
    return cds_seq_dict
#----------------------------------------------------------------------------------------------------------------
def map_dict_vals(input_dict, func_name): 
    new_dict = {}
    
    for key in input_dict:
        value = input_dict[key]
        new_value = func_name(value)
        new_dict[key] = new_value
        
    return new_dict