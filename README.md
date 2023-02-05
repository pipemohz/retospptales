# retos-presupuestales-app
App for consulting sales of products on current month and calculating commissions based on a plan of sales of products available for each salesman. It is based on Azure functions technology with python's Flask Framework as function App.

## Installation 🔧

Clone the repository in a your work folder.

## Configuration

### Prerequisites

* Azure account with active suscription.
* [Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Cwindows%2Ccsharp%2Cportal%2Cbash) 4.x.
* If you are going to use Vscode to manage Azure Functions, you will need [The Azure Functions extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions).
* If you are going to use command line to manage Azure Funcions, you will need one of the following tools:
  * [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) version 2.4 or later.
  * The Azure Az [PowerShell module](https://docs.microsoft.com/en-us/powershell/azure/install-az-ps) version 5.9.0 or later.
* A python version supported by Azure Functions. See details [here](https://docs.microsoft.com/en-us/azure/azure-functions/supported-languages#languages-by-runtime-version).

### Create a virtual environment
```
python -m venv .venv
```
### Activate virtul environment

#### Windows
```
.venv\Scripts\activate
```
#### Linux
```
source .venv/bin/activate
```
### Download all packages required
```
pip install -r requirements.txt
```
### Create an environment file

You must create an .env file for the project configuration with variables according to .env.example
```
##################
# Flask settings #
##################

# Flask app secret key
SECRET_KEY=

# JWT secret key
JWT_SECRET_KEY=

#####################
# Database settings #
#####################

DB_HOST=
DB_NAME=
DB_USERNAME=
DB_PASSWORD=

```

## Running tests
### Start Azure Function
```
func start
```
### Check the app is running on localhost
```
http://localhost:7071
````

