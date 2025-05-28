# 🔐 Azure AD User Reset Tool

This script is a lightweight administrative tool that allows Azure AD administrators to:

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

### 📥 Installation

Install the necessary dependencies using `pip`:

```bash
pip install msal requests azure-identity msgraph-sdk
