class PromptTemplate:
    prompt_template="""Identify the type of this document from the following categories: 
    - Passport
    - Driving License
    - Resume
    - I-9
    - SSN
    - Time Sheet
    - Invoice
    - Educational Certificate.

    Once classified, extract everything from the documents.

    Follow this format: 
    ---
    Document Type: [Detected Type]
    Extracted Fields:
    {Field Name}: {Value}
    {Field Name}: {Value}
    ...

    Ensure:
    1. **Preserve original text formatting** when extracting fields.
    2. **Return structured outputs** (avoid excess explanations).
    3. If a field is missing, return `"N/A"` instead of ignoring it.
    ---
    """