import dash
import dash_bootstrap_components as dbc
from automation import PyAutomation
from automation.variables import VARIABLES
from automation.utils import generate_dropdown_conditional

app = PyAutomation()

if hasattr(app, 'dash_app'):

    data = app.dash_app.alarms_table_data()

else:

    data = list()

class AlarmsComponents:

    @classmethod
    def create_alarm_form(cls):
        r"""
        Documentation here
        """
        return dash.html.Div(
            [
                dash.dcc.Location(id='alarms_page', refresh=False),
                dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            dbc.Row([
                                dbc.Col([
                                    dbc.InputGroup([dbc.Input(placeholder="Tag Name", id="tag_name_input")], size="md"),
                                    dbc.InputGroup(
                                        [
                                            dbc.InputGroupText("Variable"),
                                            dbc.Select(
                                                options=[
                                                    {"label": variable, "value": variable} for variable in VARIABLES.keys()
                                                ],
                                                id="variable_input"
                                            ),
                                            
                                        ],
                                        size="md"
                                    )
                                ],
                                width=3),
                                dbc.Col([
                                    dbc.InputGroup([dbc.InputGroupText("Unit"), dbc.Select(options=[], id="unit_input", disabled=True )],
                                        size="md"
                                    ),
                                    dbc.InputGroup(
                                        [
                                            dbc.InputGroupText("Datatype"),
                                            dbc.Select(
                                                options=[
                                                    {'label': 'Float', 'value': 'float'},
                                                    {'label': 'Integer', 'value': 'integer'},
                                                    {'label': 'Boolean', 'value': 'boolean'},
                                                    {'label': 'String', 'value': 'string'}
                                                ],
                                                id="datatype_input"
                                            ),
                                            
                                        ],
                                        size="md"
                                    ),
                                ],
                                width=2),
                                dbc.Col([
                                    dbc.InputGroup([dbc.InputGroupText(dbc.RadioButton(id="description_radio_button"), class_name="radiobutton-box"), dbc.Input(placeholder="Description (Optional)", id="description_input", disabled=True)], size="md"),
                                    dbc.InputGroup([dbc.InputGroupText(dbc.RadioButton(id="display_name_radio_button"), className="radiobutton-box"), dbc.Input(placeholder="Display Name (Optional)", id="display_name_input", disabled=True)], size="md")
                                ],
                                width=3),
                                dbc.Col([
                                    dbc.InputGroup([dbc.InputGroupText("OPCUA"), dbc.Select(options=[], id="opcua_address_input")],
                                        size="md"
                                    ),
                                    dbc.InputGroup([dbc.InputGroupText("Node"), dbc.Select(options=[], id="node_namespace_input", disabled=True)],
                                        size="md",
                                    )
                                ],
                                width=2),
                                dbc.Col([
                                    dbc.InputGroup([dbc.Input(placeholder="Scan Time", type="number", step=50, min=100, max=600000, id="scan_time_input", disabled=True), dbc.InputGroupText('ms')], size="md"),
                                    dbc.InputGroup([dbc.Input(placeholder="Dead-Band", type="number", step=0.1, id="dead_band_input", disabled=True), dbc.InputGroupText('', id="dead_band_unit")], size="md")
                                ],
                                width=2)
                            ]),
                            dbc.Button("Create", color="primary", outline=True, disabled=True, id="create_tag_button"),
                        ],
                        title="Create Tag",
                    )
                ],
                start_collapsed=True,
                )
            ]
        )

    @classmethod
    def alarms_table(cls)->dash.dash_table.DataTable:
        r"""
        Documentation here
        """

        return dash.dash_table.DataTable(
            data=data,
            columns=[
                {'name': 'id', 'id': 'id', 'editable': False}, 
                {'name': 'name', 'id': 'name'}, 
                {'name': 'unit', 'id': 'unit', 'presentation': 'dropdown'}, 
                {'name': 'data_type', 'id': 'data_type', 'presentation': 'dropdown'}, 
                {'name': 'description', 'id': 'description'}, 
                {'name': 'display_name', 'id': 'display_name'}, 
                {'name': 'opcua_address', 'id': 'opcua_address', 'presentation': 'dropdown'}, 
                {'name': 'node_namespace', 'id': 'node_namespace', 'presentation': 'dropdown'},
                {'name': 'scan_time', 'id': 'scan_time'}, 
                {'name': 'dead_band', 'id': 'dead_band'}
            ],
            id="alarms_datatable",
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_deletable=True,
            selected_columns=[],
            dropdown = {
                'data_type': {
                    'options': [
                        {'label': 'Float', 'value': 'float'},
                        {'label': 'Integer', 'value': 'integer'},
                        {'label': 'Boolean', 'value': 'boolean'},
                        {'label': 'String', 'value': 'string'}
                    ]
                },
                'opcua_address': {
                    'options': []
                }
            },
            page_action="native",
            page_current= 0,
            page_size= 10,
            persistence=True,
            editable=True,
            persisted_props=['data'],
            export_format='xlsx',
            export_headers='display',
        )