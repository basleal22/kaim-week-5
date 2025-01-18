import os
import re
import pandas
def label_message_utf8_with_birr(data):
    # Step 2: Tokenize the message into individual words/tokens
    tokens = re.findall(r'\S+', data)
    
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
