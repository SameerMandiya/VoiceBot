$env:OPENAI_API_KEY = Read-Host "AIzaSyCxoyPf3ZJwDAaVS9zI-SNk8yugTxdIJAY"
cd $PSScriptRoot
py -3 -m uvicorn app:app --reload
