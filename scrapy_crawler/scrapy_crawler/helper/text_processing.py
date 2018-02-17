class TextProcessing:
    def string_concatenate_list_of_informations(self, elm):
        # put line(s) of informations into one line,
        # and strip all unnecessary \t and \n located at
        # the front and back side of the address info
        if len(elm) > 1:
            # if it consists of more than one line, then concatenate them into one string
            elm = '\n'.join([info_per_line.strip() for info_per_line in elm])
        else:
            elm  = elm
        elm = elm.strip()
        return elm

    def remove_null_element_within_list(self, elm):
        # a list of information sometimes filled with an element of
        # unnecessary empty <li> that contains merely whitespace
        filtered_elms = []
        for line in elm:
            line = line.strip()
            if len(line) > 0:
                # if after being stripped, it still has some string in it,
                # then it is considered to be useful information.
                filtered_elms.append(line)
        elm = filtered_elms
        return elm

    def convert_one_elm_list_into_string(self, elm):
        # change list (that consists of only one element) to string. 
        # e.g. : change ```  'name': ['David']``` into ```'name' : 'David`  ```
        if elm != [] and elm != None:
            elm = elm[0]
        else:
            elm = None
        return elm

    def extract_integer_from_string(self, elm):
        # extract integer from string
        # e.g. : extract ```23``` from ```  '23 worldwide' ``` string.
        if elm != [] and elm != None:
            to_int = [int(s) for s in elm[0].split() if s.isdigit()]
            if to_int == []:
                elm = None
            else:
                elm = to_int
        else:
            elm = None
        elm = self.convert_one_elm_list_into_string(elm)
        return elm