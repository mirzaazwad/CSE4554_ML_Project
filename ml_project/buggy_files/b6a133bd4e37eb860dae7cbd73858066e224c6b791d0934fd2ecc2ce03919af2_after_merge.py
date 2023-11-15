    def storage_get_data(self, node_dict): 
        local_storage = {'knots': [], 'knotsnames': []} 

        if "knots" in self.SvLists:
            # implies "knotsnames" will be found too.. because that's how it works..
            for knot in self.SvLists['knots'].SvSubLists: 
                local_storage['knots'].append([knot.SvX, knot.SvY, knot.SvZ]) 

            for outname in self.SvLists['knotsnames'].SvSubLists: 
                local_storage['knotsnames'].append(outname.SvName) 
        
        # store anyway  
        node_dict['profile_sublist_storage'] = json.dumps(local_storage, sort_keys=True) 
        
        if self.filename:
            node_dict['path_file'] = bpy.data.texts[self.filename].as_string() 
        else:
            node_dict['path_file'] = ""