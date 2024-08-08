import dash

def init_callback(app:dash.Dash):

    def find_differences_between_lists(prev_list, curr_list):
        differences = []

        for prev_dict, curr_dict in zip(prev_list, curr_list):
            diff = {'id': prev_dict['id']}
            for key in prev_dict:
                if prev_dict[key] != curr_dict[key]:
                    diff[key] = curr_dict[key]
            if len(diff) > 1:  # Only add if there are differences other than 'id'
                differences.append(diff)
        
        return differences

    @app.callback(
        dash.Input("tag_name_input", "value"), 
        dash.Input("variable_input", "value"), 
        dash.Input("datatype_input", "value"), 
        dash.Input("unit_input", "value"), 
        dash.Input("display_name_input", "value"), 
        dash.Input("description_input", "value"),
        dash.Input("opcua_address_input", "value"),
        dash.Input("node_namespace_input", "value")
        )
    def create_tag(name, variable, datatype, unit, display_name, description, opcua_address, node_namespace):
        r"""
        Documentation here
        """

        if variable:

            dash.set_props("unit_input", {'disabled': False})
            if name and datatype and unit:

                dash.set_props("create_tag_button", {'disabled': False})
                dash.set_props("create_tag_button", {'disabled': False})

            else:
                
                dash.set_props("create_tag_button", {'disabled': True})
        
        else:

            dash.set_props("unit_input", {'disabled': True})
            dash.set_props("create_tag_button", {'disabled': True})

    @app.callback(
        dash.Output("description_input", "value"),
        dash.Input("description_radio_button", "value")
    )
    def enable_description(enable:bool):
        r"""
        Documentation here
        """
        dash.set_props("description_input", {'disabled': not enable})
        return ""
    
    @app.callback(
        dash.Output("opcua_address_input", "value"),
        dash.Input("opcua_radio_button", "value")
    )
    def enable_opcua(enable:bool):
        r"""
        Documentation here
        """
        dash.set_props("opcua_address_input", {'disabled': not enable})
        return ""
    
    @app.callback(
        dash.Output("display_name_input", "value"),
        dash.Input("display_name_radio_button", "value")
    )
    def enable_display(enable:bool):
        r"""
        Documentation here
        """
        dash.set_props("display_name_input", {'disabled': not enable})
        return ""
    
    @app.callback(
        dash.Output('tags_datatable', 'data', allow_duplicate=True),
        dash.Input('tags_page', 'pathname'),
        prevent_initial_call=True
        )
    def display_page(pathname):
        r"""
        Documentation here
        """
        if pathname=="/tags":
            
            return app.tags_table_data()
        
    @app.callback(
        dash.Output('tags_datatable', 'data', allow_duplicate=True),
        dash.Input('create_tag_button', 'n_clicks'),
        dash.State("tag_name_input", "value"), 
        dash.State("datatype_input", "value"), 
        dash.State("unit_input", "value"), 
        dash.State("display_name_input", "value"), 
        dash.State("description_input", "value"),
        dash.State("opcua_address_input", "value"),
        dash.State("node_namespace_input", "value"),
        prevent_initial_call=True
    )
    def displayClick(
        btn1, 
        tag_name,
        datatype,
        unit,
        display_name,
        description,
        opcua_address,
        node_namespace,
        allow_duplicate=True
        ):
        r"""
        Documentation here
        """
        if "create_tag_button" == dash.ctx.triggered_id:


            message = app.automation.cvt.set_tag(
                name=tag_name,
                unit=unit,
                data_type=datatype,
                description=description,
                display_name=display_name,
                opcua_address=opcua_address,
                node_namespace=node_namespace
            )
            
            if message:
                
                dash.set_props("modal-body", {"children": message})
                dash.set_props("modal-centered", {'is_open': True})
                
            return app.tags_table_data()
        
    @app.callback(
        dash.Output('tags_datatable', 'data'),
        dash.Input('tags_datatable', 'active_cell'),
        dash.State('tags_datatable', 'data_previous'),
        dash.State('tags_datatable', 'data')
        )
    def delete_update_tags(active_cell, previous, current):

        print(f"Active Cell: {active_cell} - Previous: {previous} - Current: {current}")

        if previous is None:
            dash.exceptions.PreventUpdate()

        elif active_cell==None and current: # DELETE TAG

            removed_rows = [row for row in previous if row not in current]
            
            for row in removed_rows:
                _id = row['id']
                app.automation.cvt.delete_tag(id=_id)
                # message = f"Do you want to delete Tag ID: {_id}?"
                # dash.set_props("modal-update-delete-tag-body", {"children": message})
                # dash.set_props("modal-update_delete-centered", {'is_open': True})

        else: # UPDATE TAG DEFINITION
            to_updates = find_differences_between_lists(previous, current)
            tag_to_update = to_updates[0]
            tag_id = tag_to_update.pop("id")
            app.automation.cvt.update_tag(id=tag_id, **tag_to_update)
            # message = f"Do you want to update tag {tag_id} To {tag_to_update}?"
            # dash.set_props("modal-update-delete-tag-body", {"children": message})
            # dash.set_props("modal-update_delete-centered", {'is_open': True})

        return app.tags_table_data()

    @app.callback(
        dash.Output("modal-centered", "is_open"),
        dash.Input("close-centered", "n_clicks"),
        [dash.State("modal-centered", "is_open")],
    )
    def toggle_modal(n, is_open):
        r"""
        Documentation here
        """
        if n:

            return not is_open
        
        return is_open
    
    @app.callback(
        dash.Output("modal-update_delete-centered", "is_open"),
        [dash.Input("update-delete-tag-yes", "n_clicks"), dash.Input("update-delete-tag-no", "n_clicks")],
        [
            dash.State("modal-update_delete-centered", "is_open")
        ]
    )
    def toggle_modal_update_delete_tag(yes_n, no_n, is_open):
        r"""
        Documentation here
        """
        print(f"Yes: {yes_n} - no: {no_n} - is open: {is_open}")
        if yes_n:

            # if previous is None:
            #     dash.exceptions.PreventUpdate()

            # elif active_cell==None and current: # DELETE TAG

            #     removed_rows = [row for row in previous if row not in current]
                
            #     for row in removed_rows:
            #         _id = row['id']
            #         app.automation.cvt.delete_tag(id=_id)
                    
            # else: # UPDATE TAG DEFINITION

            #     row_id = active_cell['row'] - 1
            #     tag_attr = active_cell['column_id']
            #     tag_to_update = {
            #         f"{tag_attr}": current[row_id][tag_attr]
            #     }
            #     tag_id = active_cell['row_id']
            #     app.automation.cvt.update_tag(id=tag_id, **tag_to_update)

            return not is_open
        
        elif no_n:
            
            return not is_open

        else:

            return is_open