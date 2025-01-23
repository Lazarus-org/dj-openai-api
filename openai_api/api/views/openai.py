from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from openai_api.api.serializers.openai import OpenAIParametersSerializer
from openai import OpenAI, APIError, APIConnectionError, RateLimitError, AuthenticationError
from django.conf import settings


class OpenAIChatViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = OpenAIParametersSerializer

    def create(self, request, *args, **kwargs):
        # Initialize the OpenAI client
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        # Validate and process the input data using the serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract validated data
        model = serializer.validated_data['model']
        prompt = serializer.validated_data['prompt']
        temperature = serializer.validated_data['temperature']
        max_tokens = serializer.validated_data['max_tokens']
        top_p = serializer.validated_data['top_p']
        frequency_penalty = serializer.validated_data['frequency_penalty']
        presence_penalty = serializer.validated_data['presence_penalty']

        try:
            # Send request to OpenAI API
            chat_completion = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
            )

            # Extract the response text
            response_text = chat_completion.choices[0].message.content

            # Return the response
            return Response({"response": response_text}, status=status.HTTP_200_OK)

        except AuthenticationError as e:
            # Handle authentication errors (e.g., invalid API key)
            return Response(
                {"error": "Authentication failed. Please check your API key."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        except RateLimitError as e:
            # Handle rate limit errors
            return Response(
                {"error": "Rate limit exceeded. Please try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        except APIConnectionError as e:
            # Handle API connection errors (e.g., network issues)
            return Response(
                {"error": "Unable to connect to the OpenAI API. Please check your network connection."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        except APIError as e:
            # Handle other API errors (e.g., invalid request, server errors)
            return Response(
                {"error": f"OpenAI API error: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            # Handle unexpected errors
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )