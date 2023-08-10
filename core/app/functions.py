import app.models as model

def GlobalContext(request):
    
    """
    Generates a global context with basic user information for use by all views of the project.
    "core/settings.py"
    TEMPLATES = [{'OPTIONS': {'context_processors': ['app.functions.GlobalContext',],},},]
    """
      
    try:
        Settings = model.Settings.objects.filter(IsActive=True).first()
    except:
        Settings = None

    return {
        'Settings':Settings,    
        }
