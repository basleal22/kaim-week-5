import pandas as pd
import re

def load_data(data):
    loaded_data=pd.read_csv(data)
    return loaded_data

def preprocessing_data(data):
    preprocessed = data.dropna(subset=['Message'])
    
    return preprocessed
def remove_emoji(data):
    emoji_pattern = re.compile(
        "[" 
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251" 
        "]+", 
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', data)

def label_message_utf8_with_birr(data):
    #Splitting the Message
    if '\n' in data:
        first_line, remaining_message = data.split('\n', 1)
    else:
        first_line, remaining_message = data, ""
    labeled_tokens = []
    #Tokenizing the First Line:
    first_line_tokens = re.findall(r'\S+', first_line)
    #labeling the first line tokens
    if first_line_tokens:
        labeled_tokens.append(f"{first_line_tokens[0]} B-PRODUCT")  # First token as B-PRODUCT
        for token in first_line_tokens[1:]:
            labeled_tokens.append(f"{token} I-PRODUCT")  # Remaining tokens as I-PRODUCT
    # Process the remaining message normally
    if remaining_message:
        lines = remaining_message.split('\n')
        for line in lines:
            tokens = re.findall(r'\S+', line)  # Tokenize each line while considering non-ASCII characters
            for token in tokens:
                # Check if token is a price (e.g., 500 ETB, $100, or ብር)
                if re.match(r'^\d{10,}$', token):
                    labeled_tokens.append(f"{token} O")  # Label as O for "other" or outside of any entity
                elif re.match(r'^\d+(\.\d{1,2})?$', token) or 'ETB' in token or 'ዋጋ' in token or '$' in token or 'ብር' in token:
                    labeled_tokens.append(f"{token} I-PRICE")
                # Check if token could be a location (e.g., cities or general location names)
                elif any(loc in token for loc in ['Addis Ababa', 'ለቡ', 'ለቡ መዳህኒዓለም', 'መገናኛ', 'ቦሌ', 'ሜክሲኮ']):
                    labeled_tokens.append(f"{token} I-LOC")
                # Assume other tokens are part of a product name or general text
                else:
                    labeled_tokens.append(f"{token} O")
    
    return "\n".join(labeled_tokens)
import re
import pandas as pd

# Example dataset (replace with your actual dataset)
data = {
    "Message": [
        "በ 1000 ብር የምርት አምራች በአዲስ አበባ ነበር", 
        "ማስላት ማንበብ አንድ ስልኩን በ 500 ብር"
    ]
}

df = pd.DataFrame(data)

# Step 1: Function to label each message
def label_message_utf8_with_birr(message):
    # Step 2: Tokenize the message into individual words/tokens
    tokens = re.findall(r'\S+', message)
    
    labeled_tokens = []  # List to store labeled tokens
    
    # Step 3: Loop through tokens and label them
    for i, token in enumerate(tokens):
        # Label Price Entity
        if re.match(r'^\d{10,}$', token):  # Price (e.g., large numbers)
            labeled_tokens.append(f"{token} B-PRICE")
        elif re.match(r'^\d+(\.\d{1,2})?$', token) or 'ETB' in token or 'ብር' in token:  # Price (e.g., 1000, ብር)
            labeled_tokens.append(f"{token} I-PRICE")
        # Label Location Entity
        elif 'አበባ' in token or 'ማንበብ' in token or 'አዲስ' in token:  # Location (e.g., Addis Ababa)
            labeled_tokens.append(f"{token} B-LOC")
        # Label Product Entity
        elif 'ምርት' in token:  # Product (e.g., Product names like ምርት)
            labeled_tokens.append(f"{token} B-PRODUCT")
        # Label as Outside Entity if it doesn't match any of the above categories
        else:
            labeled_tokens.append(f"{token} O")  # Outside any entity
    
    # Step 4: Return the labeled tokens as a formatted string (CoNLL format)
    return "\n".join(labeled_tokens)

# Step 5: Apply the function to the 'Message' column of the dataset
df['Labeled_Message'] = df['Message'].apply(label_message_utf8_with_birr)

# Step 6: Save the labeled dataset in CoNLL format to a text file
labeled_data_birr_path = 'labeled_telegram_product_price_location.txt'
with open(labeled_data_birr_path, 'w', encoding='utf-8') as f:
    for index, row in df.iterrows():
        f.write(f"{row['Labeled_Message']}\n\n")

print("Labeled data has been saved in CoNLL format.")

