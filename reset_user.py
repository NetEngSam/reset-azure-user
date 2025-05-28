import asyncio
import msal
import requests
from msgraph import GraphServiceClient
from azure.identity import ClientSecretCredential

# Azure 
client_id = "{YOUR_CLIENT_ID}"
tenant_id = "{YOUR_TENANT_ID}"
client_secret = "{YOUR_CLIENT_SECRET}"
authority = f"https://login.microsoftonline.com/{tenant_id}"

# User details
user_principal_name = input("Enter the user's email or UPN?")
new_password = "JRKprops2024???"  # New password for the user

# Acquire a token using msal
app = msal.ConfidentialClientApplication(client_id, authority=authority, client_credential=client_secret)
token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

if "access_token" in token:
    #Check if the user exists in the domain
    headers = {
        "Authorization": f"Bearer {token['access_token']}",
        "Content-Type": "application/json"
    }
    user_url = f"https://graph.microsoft.com/v1.0/users/{user_principal_name}"
    user_response = requests.get(user_url, headers=headers)

    if user_response.status_code == 200:
        print(f"User {user_principal_name} found in the domain.")

        # Reset the user's password
        password_reset_url = f"https://graph.microsoft.com/v1.0/users/{user_principal_name}"
        password_data = {
            "passwordProfile": {
                "password": new_password,
                "forceChangePasswordNextSignIn": False
            }
        }

        password_response = requests.patch(password_reset_url, headers=headers, json=password_data)

        if password_response.status_code == 204:
            print(f"Password for user {user_principal_name} has been reset successfully.")
            
            #Reset all MFA methods for the user
            async def reset_authentication_methods(user_id):
                try:
                    # Authenticate using ClientSecretCredential for GraphServiceClient
                    credentials = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
                    graph_client = GraphServiceClient(credentials, ["https://graph.microsoft.com/.default"])
                    
                    # Get the user's authentication methods
                    auth_methods_response = await graph_client.users.by_user_id(user_id).authentication.methods.get()
                    auth_methods = auth_methods_response.value

                    if auth_methods:
                        for method in auth_methods:
                            try:
                                if method.odata_type == "#microsoft.graph.phoneAuthenticationMethod":
                                    await graph_client.users.by_user_id(user_id).authentication.phone_methods.by_phone_authentication_method_id(method.id).delete()
                                elif method.odata_type == "#microsoft.graph.emailAuthenticationMethod":
                                    await graph_client.users.by_user_id(user_id).authentication.email_methods.by_email_authentication_method_id(method.id).delete()
                                elif method.odata_type == "#microsoft.graph.fido2AuthenticationMethod":
                                    await graph_client.users.by_user_id(user_id).authentication.fido2_methods.by_fido2_authentication_method_id(method.id).delete()
                                else:
                                    print(f"Unknown method type: {method.odata_type}")
                                print(f"Successfully deleted method with ID: {method.id}, Type: {method.odata_type}")
                            except Exception as e:
                                print(f"Failed to delete method with ID: {method.id}: {e}")
                    else:
                        print(f"No authentication methods found for user {user_id}.")
                except Exception as e:
                    print(f"Failed to reset authentication methods: {e}")

            # Run the async function to reset MFA methods
            asyncio.run(reset_authentication_methods(user_principal_name))

        else:
            print(f"Failed to reset password: {password_response.status_code} {password_response.text}")
    else:
        print(f"User {user_principal_name} not found in the domain: {user_response.status_code} {user_response.text}")
else:
    print(f"Failed to acquire token: {token.get('error')}, {token.get('error_description')}")
