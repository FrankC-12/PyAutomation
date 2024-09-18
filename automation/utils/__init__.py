from .observer import Observer
import logging
from automation.variables import VARIABLES
from automation.alarms.states import ACTIONS

def log_detailed(e, message):
    
    logging.error(message)
    logging.error(e, exc_info=True)

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def find_differences_between_lists(prev_list, curr_list):
    r"""
    Documentation here
    """
    
    differences = []

    for prev_dict, curr_dict in zip(prev_list, curr_list):
        diff = {'id': prev_dict['id']}
        for key in prev_dict:
            if prev_dict[key] != curr_dict[key]:
                diff[key] = curr_dict[key]
        if len(diff) > 1:  # Only add if there are differences other than 'id'
            differences.append(diff)
    
    return differences

def find_keys_values_by_unit(d, unit):
    r"""
    Documentation here
    """
    result = []
    
    for _, sub_dict in d.items():
        
        if unit in sub_dict.values():
            
            for k, v in sub_dict.items():
                
                result.append({'label': k, 'value': v})

    return result

def generate_dropdown_conditional():
    r"""
    Documentation here
    """
    from automation import PyAutomation
    app = PyAutomation()
    data = VARIABLES
    dropdown_conditional = []
    # dropdown conditional for unit column in table
    for _, sub_dict in data.items():

        for unit in sub_dict.values():

            options = find_keys_values_by_unit(data, unit)
            
            dropdown_conditional.append({
                'if': {'column_id': 'unit', 'filter_query': f'{{unit}} eq "{unit}"'},
                'options': options
            })

            dropdown_conditional.append({
                'if': {'column_id': 'display_unit', 'filter_query': f'{{unit}} eq "{unit}"'},
                'options': options
            })

    # dropdown conditional for node_namespace column in table
    dropdown_conditional.append({
        'if': {'column_id': 'node_namespace', 'filter_query': f'{{opcua_address}} eq ""'},
        'options': []
    })
    for client_name, info in app.get_opcua_clients().items():
        
        tree = app.get_opcua_tree(client_name=client_name)
        options = list()
        for node in tree[0]["Objects"][0]["children"]:
            options.append({
                "label": node["title"],
                "value": node["key"]
            })
            server = info['server_url']
            dropdown_conditional.append({
                'if': {'column_id': 'node_namespace', 'filter_query': f'{{opcua_address}} eq "{server}"'},
                'options': options
            })

    # dropdown conditional for operations in alarms definition table
    for state, actions in ACTIONS.items():

        dropdown_conditional.append({
                'if': {'column_id': 'operations', 'filter_query': f'{{state}} eq "{state}"'},
                'options': [{'label': action, 'value': action.replace(" ", "_")} for action in actions]
            })

    return dropdown_conditional

def get_nodes_info(selected_files:list):
    r"""
    Documentation here
    """
    to_get_node_values = dict()
    for file in selected_files:
        
        if file:

            info = file[0].split("/")
            client_name = info[0]
            namespace = info[1]
            
            if client_name in to_get_node_values:

                to_get_node_values[client_name].append(namespace)

            else:

                to_get_node_values[client_name] = [namespace]

    return to_get_node_values


def get_data_to_update_into_opcua_table(app, to_get_node_values:dict):
    r"""
    Documentation here
    """
    data = list()
    for client_name, namespaces in to_get_node_values.items():
        
        infos = app.automation.get_node_attributes(client_name=client_name, namespaces=namespaces)
        
        for info in infos:
            _info = info[0]
            namespace = _info["Namespace"]
            data.append(
                {
                    "server": client_name,
                    "namespace": namespace,
                    "data_type": _info["DataType"],
                    "display_name": _info["DisplayName"],
                    "value": _info["Value"],
                    "source_timestamp": _info["DataValue"].SourceTimestamp,
                    "status_code": _info["DataValue"].StatusCode.name
                }
            )
    
    return data