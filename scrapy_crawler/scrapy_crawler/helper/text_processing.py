class TextProcessing(object):
    def __init__():
        pass

    def string_concatenate_list_of_informations(self, elm):
        # put line(s) of informations into one line,
        # and strip all unnecessary \t and \n located at
        # the front and back side of the address info
        if len(company_info[key]) > 1:
            # if it consists of more than one line, then concatenate them into one string
            company_info[key] = '\n'.join([info_per_line.strip() for info_per_line in company_info[key]])
        else:
            company_info[key]  = company_info[key]
        company_info[key] = company_info[key].strip()
        return company_info

    def remove_null_element_within_list(self, company_info, key):
        # a list of information sometimes filled with an element of
        # unnecessary empty <li> that contains merely whitespace
        filtered_elms = []
        for line in company_info[key]:
            line = line.strip()
            if len(line) > 0:
                # if after being stripped, it still has some string in it,
                # then it is considered to be useful information.
                filtered_elms.append(line)
        company_info[key] = filtered_elms
        return company_info

    def convert_one_elm_list_into_string(self, company_info, key):
        # change list (that consists of only one element) to string. 
        # e.g. : change ```  'name': ['David']``` into ```'name' : 'David`  ```
        if company_info[key] != [] and company_info[key] != None:
            company_info[key] = company_info[key][0]
        else:
            company_info[key] = None
        return company_info

    def extract_integer_from_string(self, company_info, key):
        # extract integer from string
        # e.g. : extract ```23``` from ```  '23 worldwide' ``` string.
        if company_info[key] != [] and company_info[key] != None:
            to_int = [int(s) for s in company_info[key][0].split() if s.isdigit()]
            if to_int == []:
                company_info[key] = None
            else:
                company_info[key] = to_int
        else:
            company_info[key] = None
        company_info = self.convert_one_elm_list_into_string(company_info, key)
        return company_info