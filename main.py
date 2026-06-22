from playfab import PlayFabClientAPI, PlayFabSettings
import time

PlayFabSettings.TitleId = input("Enter Title ID: ")
custom_id = input("Enter Custom ID: ")
catalog_version = input("Enter Catalog Version (Leave blank for default): ")
if not catalog_version.strip():
    catalog_version = None

save_to_txt = input("Do you want to save to txt [y,n]: ").lower().strip()

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
                print(f"Item Name: {item.get("DisplayName", "No Name")} | ID: {item.get("ItemId")} | Price: {item.get("VirtualCurrencyPrices")}")

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
        print(f"Playfab ID: {success.get('PlayFabId')}")

        catalog_request = {"CatalogVersion": catalog_version}
        PlayFabClientAPI.GetCatalogItems(catalog_request, catalog_callback)

        data_request = {"Data": {"CurrentLevel": "5", "Class": "Larp"}}
        PlayFabClientAPI.UpdateUserData(data_request, update_callback)

    elif failure:
        print(f"Login failed: {failure.GenerateErrorReport()}")

request = {
    "CustomId": custom_id,
    "CreateAccount": True
}

print("\nTrying to login...")
PlayFabClientAPI.LoginWithCustomID(request, login_callback)

time.sleep(5)