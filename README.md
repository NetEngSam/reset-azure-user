
# 🔐 Azure AD User Reset Tool

This Python script is a lightweight administrative tool that allows Azure AD administrators to:

1. Reset a user's password.
2. Remove all registered Multi-Factor Authentication (MFA) methods using the Microsoft Graph API.

---

## 📦 Requirements

- Python 3.8 or later
- Microsoft Entra ID (Azure AD) App Registration:
  - **Client ID**
  - **Tenant ID**
  - **Client Secret**
- Required Python libraries:
  - `msal`
  - `requests`
  - `azure-identity`
  - `msgraph-sdk`

---

## 🔧 Azure App Registration & Permissions Setup

Follow these steps to register your app and assign the correct permissions:

### 1. Register the App in Azure

1. Go to the **[Azure Portal](https://portal.azure.com)**
2. Navigate to **Microsoft Entra ID** > **App registrations** > **New registration**
3. Enter a name like `ResetUserTool`, choose **Accounts in this organizational directory only** and click **Register**
4. Save the **Application (client) ID** and **Directory (tenant) ID**

### 2. Create a Client Secret

1. Go to **Certificates & secrets** > **New client secret**.
2. Add a description and choose an expiration period.
3. Save the **client secret value** immediately (you won’t be able to view it again later)

### 3. Assign API Permissions

1. Go to **API permissions** > **Add a permission**.
2. Select **Microsoft Graph** > **Application permissions**.
3. Add the following:
   - `User.Read.All`
   - `User.ReadWrite.All`
   - `UserAuthenticationMethod.Read.All`
   - `UserAuthenticationMethod.ReadWrite.All`
4. Click **Add permissions**.
5. Click **Grant admin consent** for your tenant.

---
## 📥 Installation

Install the necessary dependencies using `pip`:

```bash
pip install msal requests azure-identity msgraph-sd
```

---

## ⚙️ Configuration

Update the ```reset_user.py``` script with you Azure AD app details: 
```python
client_id = "{YOUR_CLIENT_ID}"
tenant_id = "{YOUR_TENANT_ID}"
client_secret = "{YOUR_CLIENT_SECRET}"
```

---
## 🚀 Usage

Run the script from the terminal:
```bash
python reset_user.py
```
The script will:
- Check if the user exists
- Reset their password
- Delete their MFA methods (phone, email, FIDO2)


## 🧠 How it works 

- **Token Acquisition**: Uses `msal` to acquire a token via client credentials.
- **Password Reset**: Sends a PATCH request to Microsoft Graph API to reset the user's password.
- **MFA Reset**: Uses `GraphServiceClient` and `azure-identity` to:
    - Retrieve all authentication methods
    - Delete each method based on its type


## 🛡️ Notes & Warnings

- Ensure the app registration has appropriate **API permissions** and **admin consent**.
- MFA deletion is **permanent** and should only be done with full administrative intent.
- You must run this script with proper directory and network permissions to access Graph API.

## 🧾 License
MIT License – use freely, modify responsibly, and don’t forget to secure your credentials.

## 🙋 Support

Feel free to open an issue or submit a pull request if you'd like to improve the functionality!


Let me know if you want this broken out into separate setup scripts, or if you'd like `.env` support added to the Python script too!
