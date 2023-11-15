    def show_code_completion(self):
        """Display a completion list based on the current line"""
        # Note: unicode conversion is needed only for ExternalShellBase
        text = to_text_string(self.get_current_line_to_cursor())
        last_obj = self.get_last_obj()
        if not text:
            return

        obj_dir = self.get_dir(last_obj)
        if last_obj and obj_dir and text.endswith('.'):
            self.show_completion_list(obj_dir)
            return
        
        # Builtins and globals
        if not text.endswith('.') and last_obj \
           and re.match(r'[a-zA-Z_0-9]*$', last_obj):
            b_k_g = dir(builtins)+self.get_globals_keys()+keyword.kwlist
            for objname in b_k_g:
                if objname.startswith(last_obj) and objname != last_obj:
                    self.show_completion_list(b_k_g, completion_text=last_obj)
                    return
            else:
                return
        
        # Looking for an incomplete completion
        if last_obj is None:
            last_obj = text
        dot_pos = last_obj.rfind('.')
        if dot_pos != -1:
            if dot_pos == len(last_obj)-1:
                completion_text = ""
            else:
                completion_text = last_obj[dot_pos+1:]
                last_obj = last_obj[:dot_pos]
            completions = self.get_dir(last_obj)
            if completions is not None:
                self.show_completion_list(completions,
                                          completion_text=completion_text)
                return
        
        # Looking for ' or ": filename completion
        q_pos = max([text.rfind("'"), text.rfind('"')])
        if q_pos != -1:
            completions = self.get_cdlistdir()
            if completions:
                self.show_completion_list(completions,
                                          completion_text=text[q_pos+1:])
            return