import os
from nicegui import ui, app
from web3 import Web3
from solidity_python_sdk.main import DigitalProductPassportSDK
import logging

passport = DigitalProductPassportSDK()

@ui.page('/')
def index():
    # Initialize the SDK and ProductPassport class
    ui.page_title('Demo')
    # Custom CSS for styling
    ui.add_head_html('''
        <style type="text/tailwindcss">
            @layer components {
                .leaflet-map {
                    width: 70%;
                    height: 400px;
                }
                .pdf-viewer {
                    width: 100%;
                    height: 100%;
                    min-height: 600px;
                }
            }
        </style>
    ''')
    cache = app.storage.client
    # UI components
    with ui.row().classes('w-full'):
        ui.image("https://www.web3digitalproductpassport.com/img/logo.png").classes('w-[50px]')
        ui.label('Demo - Digital Product Passport').style('color: #6E93D6; font-size: 200%; font-weight: 300')
    with ui.row().classes('w-full'):
        with ui.tabs().classes('w-full') as product_tabs:
            product_tab = ui.tab('Product Information').style('color: #6E93D6; font-size: 200%; font-weight: 300')
            batch_tab = ui.tab('Batch').style('color: #6E93D6; font-size: 200%; font-weight: 300')
        with ui.tab_panels(product_tabs, value=product_tab).classes('w-full'):
            with ui.tab_panel(product_tab):
                product_contract_address_input = ui.input('Product Contract Address', placeholder='ProductPassport address printed by deploy.py').classes('input-field')
                product_id_input = ui.input('Product ID (Numeric)', value='1').classes('input-field')
                ui.button('Get Product Details', on_click=lambda: get_product_details(product_contract_address_input.value, product_id_input.value)).classes('button')
                
        with ui.tab_panels(product_tabs, value=batch_tab).classes('w-full'):
            with ui.tab_panel(batch_tab):
                batch_contract_address_input = ui.input('Batch Contract Address', placeholder='Batch address printed by deploy.py').classes('input-field')
                batch_id_input = ui.input('Batch ID (Numeric)', placeholder='Enter numeric batch ID, use 1').classes('input-field')
                batch_product_id_input = ui.input('Product ID (Numeric)', value='1').classes('input-field')
                ui.button('Get Batch Details', on_click=lambda: get_batch_details(batch_contract_address_input.value, batch_id_input.value, batch_product_id_input.value)).classes('button')


def get_product_details(product_contract_address, product_id):
    product_details_output = ui.label(None)

    try:
        if not Web3.is_address(product_contract_address):
            product_details_output.set_text("Error: Invalid product contract address.").classes('w-full')
            return

        try:
            product_id_int = int(product_id)
        except ValueError:
            product_details_output.set_text("Error: Product ID must be a numeric value.").classes('w-full')
            return

        product_details = passport.product_passport.get_product_details(product_contract_address, product_id_int)

        print("Product Details Retrieved:", product_details)

        product = product_details["product"]

        with ui.card().classes('w-full'):
            with ui.grid(columns=1).classes('w-full'):
                plot_product_specifications(product)
                plot_geolocations([dict(product_details["origin"], label="Origin")])
                plot_product_documents(product)

    except ValueError as e:
        product_details_output.set_text(f"Input Error: {str(e)}")
    except Exception as e:
        product_details_output.set_text(f"Error: {str(e)}")
        logging.error(f"Failed to retrieve product details: {e}")

def get_batch_details(batch_contract_address, batch_id, product_id):
    batch_details_output = ui.label(None)
    try:
        if not Web3.is_address(batch_contract_address):
            batch_details_output.set_text("Error: Invalid batch contract address.")
            return

        try:
            batch_id_int = int(batch_id)
            product_id_int = int(product_id)
        except ValueError:
            batch_details_output.set_text("Error: Batch ID and Product ID must be numeric values.")
            return

        batch_details = passport.batch.get_batch_details(batch_contract_address, batch_id_int, product_id_int)

        print("Batch Data Retrieved:", batch_details)

        batch = batch_details["batch"]
        with ui.card().classes('w-full'):
            with ui.grid(columns=3).classes('w-full'):
                ui.label(f"Quantity: {batch['amount']}").classes('blue-box')
                ui.label(f"Assembling Time: {batch['assemblingTime']}").classes('blue-box')
                ui.label(f"Transport Details: {batch['transportDetails']}").classes('blue-box')
                ui.label(f"Product: {batch_details['product']['description']}").classes('blue-box')
                ui.label(f"Made at: {batch_details['complex']['complexName']}").classes('blue-box')

        plot_geolocations([
            dict(batch_details["originLocation"], label="Origin"),
            dict(batch_details["currentLocation"], label="Current location"),
        ])

    except ValueError as e:
        batch_details_output.set_text(f"Input Error: {str(e)}")
    except Exception as e:
        batch_details_output.set_text(f"Error: {str(e)}")
        logging.error(f"Failed to retrieve batch details: {e}")

def plot_geolocations(geolocations):
    leaflet_map = ui.leaflet(center=(0, 0), zoom=2).classes('leaflet-map')
    leaflet_map.clear_layers()
    rows = []
    if not geolocations:
        leaflet_map.marker([0, 0], "No geolocations available.")
        return
    for loc in geolocations:
        try:
            latitude, longitude = float(loc["latitude"]), float(loc["longitude"])
            leaflet_map.marker(latlng=(latitude, longitude))
            rows.append(
                {
                    'label': loc.get("label", ""),
                    'latitude': loc["latitude"],
                    'longitude': loc["longitude"],
                    'additional_info': loc["additionalInfo"]
                }
            )
        except (KeyError, TypeError, ValueError) as e:
            logging.error(f"Failed to plot geolocation: {e}")
    if rows:
        leaflet_map.set_center(center=(float(rows[-1]['latitude']), float(rows[-1]['longitude'])))
        leaflet_map.set_zoom(3)
    columns = [
            {'name': 'label', 'label': 'Location', 'field': 'label', 'required': False, 'align': 'left'},
            {'name': 'latitude', 'label': 'Latitude', 'field': 'latitude', 'required': True, 'align': 'left'},
            {'name': 'longitude', 'label': 'Longitude', 'field': 'longitude', 'required': True, 'align': 'left'},
            {'name': 'additional_info', 'label': 'Additional Info', 'field': 'additional_info', 'required': False, 'align': 'left'}
        ]

    ui.table(columns=columns, rows=rows, row_key='label').classes('w-full')    

def get_pinata_url(ipfs_hash):
    pinata_gateway_token = os.getenv('PINATA_GATEWAY_TOKEN')
    pinata_gateway_url = os.getenv('PINATA_GATEWAY_URL')
    return f"https://{pinata_gateway_url}/ipfs/{ipfs_hash}?pinataGatewayToken={pinata_gateway_token}"

def plot_product_specifications(product):
    with ui.grid(columns=2):
        ui.label(f"Description: {product['description']}").classes('blue-box')
        ui.label(f"Batch: {product['batchNumber']}").classes('blue-box')
        ui.label(f"Production date: {product['productionDate']}").classes('blue-box')
        ui.label(f"Expiry date: {product['expiryDate']}").classes('blue-box')
        ui.label(f"Certifications: {product['certifications']}").classes('blue-box')
        ui.label(f"Warranty: {product['warrantyInfo']}").classes('blue-box')
        ui.label(f"Material Composition: {', '.join(product['materialComposition'])}").classes('blue-box')
        ui.label(f"Complex: {product['complexId']}").classes('blue-box')

def plot_product_documents(product):
    manuals, specifications = product['manuals'], product['specifications']
    with ui.grid(columns=1).classes('w-full'):
        with ui.column():
            with ui.tabs().classes('w-full') as tabs:
                tab_manuals = ui.tab('Manuals')
                tab_specifications = ui.tab('Specifications')
            with ui.tab_panels(tabs, value=tab_manuals).classes('w-full'):
                with ui.tab_panel(tab_manuals):
                    for each in manuals:
                        ipfs = get_pinata_url(each)
                        ui.html(f'<embed src="{ipfs}" type="application/pdf" class="pdf-viewer">').classes('w-full')
                with ui.tab_panel(tab_specifications):
                    for each in specifications:
                        ipfs = get_pinata_url(each)
                        ui.html(f'<embed src="{ipfs}" type="application/pdf" class="pdf-viewer">').classes('w-full')

ui.run()
