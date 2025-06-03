from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from open_webui.utils.auth import get_admin_user
from open_webui.storage import provider

router = APIRouter()

class AzureStorageConfigForm(BaseModel):
    AZURE_STORAGE_ENDPOINT: str
    AZURE_STORAGE_CONTAINER_NAME: str
    AZURE_STORAGE_KEY: str

@router.get("/azure", response_model=AzureStorageConfigForm)
async def get_azure_storage_config(request: Request, user=Depends(get_admin_user)):
    return {
        "AZURE_STORAGE_ENDPOINT": request.app.state.config.AZURE_STORAGE_ENDPOINT,
        "AZURE_STORAGE_CONTAINER_NAME": request.app.state.config.AZURE_STORAGE_CONTAINER_NAME,
        "AZURE_STORAGE_KEY": request.app.state.config.AZURE_STORAGE_KEY,
    }

@router.post("/azure", response_model=AzureStorageConfigForm)
async def set_azure_storage_config(
    request: Request, form_data: AzureStorageConfigForm, user=Depends(get_admin_user)
):
    request.app.state.config.AZURE_STORAGE_ENDPOINT = form_data.AZURE_STORAGE_ENDPOINT
    request.app.state.config.AZURE_STORAGE_CONTAINER_NAME = form_data.AZURE_STORAGE_CONTAINER_NAME
    request.app.state.config.AZURE_STORAGE_KEY = form_data.AZURE_STORAGE_KEY

    provider.AZURE_STORAGE_ENDPOINT = form_data.AZURE_STORAGE_ENDPOINT
    provider.AZURE_STORAGE_CONTAINER_NAME = form_data.AZURE_STORAGE_CONTAINER_NAME
    provider.AZURE_STORAGE_KEY = form_data.AZURE_STORAGE_KEY
    provider.Storage = provider.get_storage_provider(provider.STORAGE_PROVIDER)

    return {
        "AZURE_STORAGE_ENDPOINT": request.app.state.config.AZURE_STORAGE_ENDPOINT,
        "AZURE_STORAGE_CONTAINER_NAME": request.app.state.config.AZURE_STORAGE_CONTAINER_NAME,
        "AZURE_STORAGE_KEY": request.app.state.config.AZURE_STORAGE_KEY,
    }
