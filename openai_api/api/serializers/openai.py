from rest_framework import serializers

class OpenAIParametersSerializer(serializers.Serializer):
    MODEL_CHOICES = [
        ("gpt-3.5-turbo", "GPT-3.5 Turbo"),
        ("gpt-4", "GPT-4"),
        ("gpt-4-turbo-preview", "GPT-4 Turbo Preview"),
    ]
    model = serializers.ChoiceField(
        choices=MODEL_CHOICES,
        default="gpt-3.5-turbo",
        label="Model",
        help_text="The OpenAI model to use for generating the response. Choose from GPT-3.5 Turbo, GPT-4, or GPT-4 Turbo Preview."
    )
    prompt = serializers.CharField(
        required=True,
        label="Prompt",
        help_text="The input text or question that you want to send to the OpenAI model."
    )
    temperature = serializers.FloatField(
        default=0.7,
        min_value=0.0,
        max_value=2.0,
        label="Temperature",
        help_text="Controls the randomness of the output. Lower values make the output more deterministic, while higher values make it more creative."
    )
    max_tokens = serializers.IntegerField(
        default=100,
        min_value=1,
        label="Max Tokens",
        help_text="The maximum number of tokens (words or characters) to generate in the response."
    )
    top_p = serializers.FloatField(
        default=1.0,
        min_value=0.0,
        max_value=1.0,
        label="Top P",
        help_text="Controls the diversity of the output by sampling from the top P probability mass. Lower values make the output more focused."
    )
    frequency_penalty = serializers.FloatField(
        default=0.0,
        min_value=0.0,
        max_value=2.0,
        label="Frequency Penalty",
        help_text="Reduces the likelihood of repeating the same phrases in the output. Higher values discourage repetition."
    )
    presence_penalty = serializers.FloatField(
        default=0.0,
        min_value=0.0,
        max_value=2.0,
        label="Presence Penalty",
        help_text="Encourages the model to introduce new topics or concepts. Higher values increase the likelihood of new content."
    )