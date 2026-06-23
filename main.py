from playfab import PlayFabClientAPI, PlayFabSettings
import time
import json  

PlayFabSettings.TitleId = input("Enter Title ID: ")
custom_id = input("Enter Custom ID: ")

print("\n--- MENU ---")
print("[1] Get Catalog Items")
print("[2] Update Player Data")
print("[3] Get Account Info Using Display Name")
print("[4] Get Title Info")
print("[5] Get Account Info Using Playfab ID")
print("[6] Purchase Item")
print("[7] Get User Inventory")
print("[8] Change Display Name")
print("[9] Add Virtual Currency")
choice = input("Select an option (1, 2, 3, 4, 5, 6, 7, 8, 9): ").strip()

catalog_version = None
save_to_txt = "n"
disname = None
gameID = None
newdisplayname = None

add_currency_code = None
add_currency_amount = 0

if choice in ("1"):
    catalog_version = input("Enter Catalog Version (Leave blank for default): ")
    if not catalog_version.strip():
        catalog_version = None
    save_to_txt = input("Do you want to save to txt [y,n]: ").lower().strip()

if choice in ("3"):
    disname = input("Enter the display name you want to search: ").strip()

if choice in ("4"):
    save_to_txt = input("Do you want to save Title Info to txt [y,n]: ").lower().strip()

if choice in ("5"):
    gameID = input("Enter the playfab ID: ").strip()

if choice in ("6"):
    item_id = input("Enter your Item ID: ").strip()
    currency_code = input("Enter your currency code: ").strip()
    price_amount = int(input("Etner the price: ").strip())
    catalog_version = input("Enter Catalog Version (Leave blank for default): ").strip()
    if not catalog_version:
        catalog_version = None
    
if choice in ("8"):
    new_display_name = input("Enter new display name: ").strip()

if choice in ("9"):
    add_currency_code = input("Enter the currency code: ").strip()
    add_currency_amount = int(input("Enter the amount: ").strip())

def pulltitle(success, failure):
    if success:
        print("\n--- Title Info ---")
        titleinfo = success.get("Data", {})

        if titleinfo:
            if save_to_txt == "y":
                with open("titleoutput.txt", "w", encoding="utf-8") as file:
                    file.write("--- Title Info ---\n\n")
                    for key, value in titleinfo.items():
                        file.write(f"Key: {key}\n")
                        try:
                            parsed_json = json.loads(value)
                            formatted_value = json.dumps(parsed_json, indent=4)
                            file.write(f"Value:\n{formatted_value}\n")
                            print(f"Key: {key} -> (JSON saved to file)")
                        
                        except (ValueError, TypeError):
                            file.write(f"Value: {value}\n")
                            print(f"Key: {key} -> (Text saved to file)")
                        
                        file.write("-" * 40 + "\n")
                print("\nSuccessfully saved to titleoutput.txt")
            else:
                for key, value in titleinfo.items():
                    print(f"Key: {key}")
                    try:
                        parsed_json = json.loads(value)
                        print("Value:\n" + json.dumps(parsed_json, indent=4))
                    except (ValueError, TypeError):
                        print(f"Value: {value}")
                    print("-" * 40)
        else:
            print("No Title Info found or the data object is empty.")

    elif failure:
        print(f"\nLookup failed: {failure.GenerateErrorReport()}")

def accountinfo(success, failure):
    if success:
        print("--- Account Info ---")
        account_info = success.get("AccountInfo", {})
        print(f"Playfab ID: {account_info.get('PlayFabId')}")
        print(f"Username: {account_info.get('Username', 'N/A')}")
        print(f"Created At: {account_info.get('Created')}")

        title_info = account_info.get('TitleInfo', {})
        print(f"Display Name: {title_info.get('DisplayName', 'N/A')}")
    elif failure:
        print(f"\nLookup failed: {failure.GenerateErrorReport()}")

def accountinfoID(success, failure):
    if success:
        print("--- Account Info ---")
        account_info = success.get("AccountInfo", {})
        print(f"Playfab ID: {account_info.get('PlayFabId')}")
        print(f"Username: {account_info.get('Username', 'N/A')}")
        print(f"Created At: {account_info.get('Created')}")

        title_info = account_info.get('TitleInfo', {})
        print(f"Display Name: {title_info.get('DisplayName', 'N/A')}")
    elif failure:
        print(f"\nLookup failed: {failure.GenerateErrorReport()}")

def catalog_callback(success, failure):
    if success:
        print("\n--- Catalog Items ---")
        items = success.get("Catalog", [])

        if save_to_txt == "y":
            with open("catalogoutput.txt", "w", encoding="utf-8") as file:
                file.write("--- Catalog Items ---\n\n")
                for item in items:
                    name = item.get("DisplayName", "No Name")
                    item_id = item.get("ItemId", "No ID")
                    desc = item.get("Description", "No Description")
                    price = item.get("VirtualCurrencyPrices", "No Price")
                    
                    file.write(f"Name: {name}\nID: {item_id}\nDescription: {desc}\n Price: {price}\n")
                    file.write("-" * 30 + "\n")
                    
                    print(f"Item Name: {name} | ID: {item_id} | Price: {price}")
            print("\nSuccessfully saved to catalogoutput.txt")
        else:
            for item in items:
                print(f"Item Name: {item.get('DisplayName', 'No Name')} | ID: {item.get('ItemId')} | Price: {item.get('VirtualCurrencyPrices')}")

    elif failure:
        print(f"Failed to get catalog: {failure.GenerateErrorReport()}")

def update_callback(success, failure):
    if success:
        print("Updated data")
    elif failure:
        print(f"Failed to update: {failure.GenerateErrorReport()}")

def purchase(success, failure):
    if success:
        print("--- Item Purchased ---")
        items_bought = success.get("Items", [])
        for bought_item in items_bought:
            print(f"Bought: {bought_item.get('DisplayName')} (Instance ID: {bought_item.get('ItemInstanceId')})")
    elif failure:
        error_msg = failure.get("errorMessage", "Unknown Error")
        error_code = failure.get("errorCode", "N/A")
        print(f"Failed to Purchase: {failure.GenerateErrorReport()}")

def inventory(success, failure):
    if success:
        print("--- Player Inventory ---")
        inventory = success.get("Inventory", [])

        if not inventory:
            print("Inventory is empty")
        else:
            for item in inventory:
                display_name = item.get("DisplayName", "No Name")
                item_id = item.get("ItemId")
                instance_id = item.get("ItemInstanceId")
                print(f"Item: {display_name} | ID: {item_id} | Instance ID: {instance_id}")

        print("--- Virtual Currency Balance")
        balances = success.get("VirtualCurrency", {})
        if not balances:
            print("No virtual currency")
        else:
            for currency, amount in balances.items():
                print(f"{currency}: {amount}")
        
    elif failure:
        error_msg = failure.get("errorMessage", "Unknown")
        error_code = failure.get("errorCode", "N/A")
        print(f"Failed to get inventory: [{error_code}] {error_msg}")

def display_name(success, failure):
    if success:
        print("--- Display Name ---")
        print(f"New Display Name: {success.get('DisplayName')}")
    elif failure:
        error_msg = failure.get("errorMessage", "Unknown Error")
        error_code = failure.get("errorCode", "N/A")
        print(f"Failed to update Display Name: [{error_code}] {error_msg}")

def givecurrency(success, failure):
    if success:
        print("--- Currency Added ---")
        print(f"Currency Code: {success.get('VirtualCurrency')}")
        print(f"Amount Added: {success.get('BalanceChange')}")
        print(f"New Wallet Balance: {success.get('Balance')}")
    elif failure:
        error_msg = failure.get("errorMessage", "Unknown Error",)
        error_code = failure.get("errorCode", "N/A")
        print(f"Failed to add currency: [{error_code}] {error_msg}")

def login_callback(success, failure):
    if success:
        print("Logged In")
        print(f"Playfab ID: {success.get('PlayFabId')}\n")
        print(f"Session Ticket: {success.get('SessionTicket')}\n")

        if choice in ("1"):
            catalog_request = {"CatalogVersion": catalog_version}
            PlayFabClientAPI.GetCatalogItems(catalog_request, catalog_callback)

        if choice in ("2"):
            data_request = {"Data": {"CurrentLevel": "5", "Class": "Larp"}}
            PlayFabClientAPI.UpdateUserData(data_request, update_callback)

        if choice in ("3"):
            account_request = {"TitleDisplayName": disname}
            PlayFabClientAPI.GetAccountInfo(account_request, accountinfo)

        if choice in ("4"):
            titleinfo_request = {}
            PlayFabClientAPI.GetTitleData(titleinfo_request, pulltitle)

        if choice in ("5"):
            account_requestID = {"PlayFabId": gameID}
            PlayFabClientAPI.GetAccountInfo(account_requestID, accountinfoID)

        if choice in ("6"):
            purchase_request = {
                "ItemId": item_id,
                "VirtualCurrency": currency_code,
                "Price": price_amount
            }
            if catalog_version:
                purchase_request["CatalogVersion"] = catalog_version
            print(f"Attempting to purchase item {item_id} from catalog {catalog_version}")
            PlayFabClientAPI.PurchaseItem(purchase_request, purchase)
        
        if choice in ("7"):
            inventory_request = {}
            print("Fetching Inventory")
            PlayFabClientAPI.GetUserInventory(inventory_request, inventory)

        if choice in ("8"):
            display_name_request = {
                "DisplayName": new_display_name
            }
            print(f"Attempting to update display name to {new_display_name}")
            PlayFabClientAPI.UpdateUserTitleDisplayName(display_name_request, display_name)

        if choice in ("9"):
            add_currency_request = {
                "VirtualCurrency": add_currency_code,
                "Amount": add_currency_amount
            }
            print(f"Attempting to give currency {add_currency_amount} {add_currency_code}")

    elif failure:
        print(f"Login failed: {failure.GenerateErrorReport()}")

request = {
    "CustomId": custom_id,
    "CreateAccount": True
}

print("\nTrying to login...")
PlayFabClientAPI.LoginWithCustomID(request, login_callback)

time.sleep(5)