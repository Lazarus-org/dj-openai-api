from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class OpenaiApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "openai_api"
    verbose_name = _("Django OpenAi Api")
