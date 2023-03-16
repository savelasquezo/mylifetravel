import app.models as model

def GlobalContext(request):
    
    """
    Generates a global context with basic user information for use by all views of the project.
    "app/core/settings.py"
    TEMPLATES = [{'OPTIONS': {'context_processors': ['app.functions.GlobalContext',],},},]
    """
    
    if request.user.id is not None:
        Setting = model.Settings.objects.filter(IsActive=True).first()
        return {'Setting':Setting,}
        
    return {}   
