from google.cloud import language_v1

def run_test():
    client = language_v1.LanguageServiceClient()

    text = "The Daily Indian Express"

    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_syntax(document=document)

    tokens = [token.text.content.lower() for token in response.tokens]
    print("Tokens:", tokens)

if __name__ == "__main__":
    run_test()
