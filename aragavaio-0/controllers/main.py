from odoo import http
from odoo.http import request
import json
import gzip
import base64


def encode(string: str) -> str:
    compressed = gzip.compress(string.encode('utf8'), 9)
    return base64.b64encode(compressed).decode('utf8')


class AragavaioRedirectController(http.Controller):
    @http.route('/aragavaio/redirect', type='http', auth='user')
    def report(self, **kwargs):
        res = {'table_name': 'odoo', 'devices': {}, 'cables': []}

        records = request.env['product.template'].search([])
        for record in records:
            if record.aragavaio_type == 'device':
                category = record.categ_id.name
                manual_url = record.manual_url
                ports = []
                for port in record.port_ids:
                    p = {
                        'connector': port.connector.name,
                        'type': port.type,
                        'direction': port.direction,
                        'interface': port.interface.name,
                        'count': port.amount,
                        'require': port.required
                    }
                    if port.name:
                        p['name'] = port.name
                    ports.append(p)

                for variant in record.product_variant_ids:
                    count = int(variant.qty_available)
                    cn = variant.product_template_attribute_value_ids._get_combination_name()
                    d = {
                        'name': cn and f'{variant.name} ({cn})' or variant.name,
                        'count': count,
                        'ports': ports,
                        'custom_properties': {v.attribute_line_id.attribute_id.name: v.name
                                              for v in variant.product_template_attribute_value_ids}
                    }
                    if manual_url:
                        d['specification'] = manual_url

                    res['devices'][category] = res['devices'].get(category, []) + [d]

            elif record.aragavaio_type == 'cable':
                res['cables'].append({
                    'left_connector': {
                        'connector': record.left_connector_connector.name,
                        'type': record.left_connector_type
                    },
                    'right_connector': {
                        'connector': record.right_connector_connector.name,
                        'type': record.right_connector_type
                    },
                    'length': record.cable_length,
                    'count': int(record.qty_available)
                })
        res['devices'] = [{'group_name': cat, 'group_list': objs}
                          for cat, objs in res['devices'].items()]

        data = encode(json.dumps(res))

        response = request.make_response('''
            <script>
            function redirect() {
            var mapForm = document.createElement("form");
            mapForm.method = "POST";
            mapForm.action = "https://constructor.dev.aragava.io/redirect";
            var mapInput = document.createElement("input");
            mapInput.type = "text";
            mapInput.name = "library";
            mapInput.style = "display: none";''' +
                                         f'mapInput.value = "{data}";\n' +
                                         '''
            mapForm.appendChild(mapInput);
            document.body.appendChild(mapForm);
            mapForm.submit();
            }
            window.onload = redirect;
            </script>''',
                                         headers=[('Content-Type', 'text/html')])
        return response
