from playfab import PlayFabClientAPI, PlayFabSettings
import time

PlayFabSettings.TitleId = input("Enter Title ID: ")
custom_id = input("Enter Custom ID: ")

print("\n--- MENU ---")
print("[1] Get Catalog Items")
print("[2] Update Player Data")
print("[3] Get Account Info Using Display Name")
choice = input("Select an option (1, 2, 3): ").strip()

catalog_version = None
save_to_txt = "n"
disname = None

if choice in ("1"):
    catalog_version = input("Enter Catalog Version (Leave blank for default): ")
    if not catalog_version.strip():
        catalog_version = None
    save_to_txt = input("Do you want to save to txt [y,n]: ").lower().strip()

if choice in ("3"):
    disname = input("Enter the display name you want to search: ").strip()


def accountinfo(success, failure):
    if success:
        print("--- Account Info ---")
        account_info = success.get("AccountInfo", {})
        print(f"Playfab ID: {account_info.get("PlayFabId")}")
        print(f"Username: {account_info.get("Username", "N/A")}")
        print(f"Created At: {account_info.get("Created")}")

        title_info = account_info.get("TitleInfo", {})
        print(f"Display Name: {title_info.get("DisplayName", "N/A")}")
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

def login_callback(success, failure):
    if success:
        print("Logged In")
        print(f"Playfab ID: {success.get('PlayFabId')}\n")

        if choice in ("1"):
            catalog_request = {"CatalogVersion": catalog_version}
            PlayFabClientAPI.GetCatalogItems(catalog_request, catalog_callback)

        if choice in ("2"):
            data_request = {"Data": {"CurrentLevel": "5", "Class": "Larp"}}
            PlayFabClientAPI.UpdateUserData(data_request, update_callback)

        if choice in ("3"):
            account_request = {"TitleDisplayName": disname}
            PlayFabClientAPI.GetAccountInfo(account_request, accountinfo)

    elif failure:
        print(f"Login failed: {failure.GenerateErrorReport()}")

request = {
    "CustomId": custom_id,
    "CreateAccount": True
}

print("\nTrying to login...")
PlayFabClientAPI.LoginWithCustomID(request, login_callback)

time.sleep(5)