# Base64 format
Base64 is an encoding scheme that converts binary data into a text string using a limited set of 64 ASCII characters: uppercase letters (A-Z), lowercase letters (a-z), digits (0-9), and two additional symbols (`+` and `/`). A URL-safe variant of Base64 replaces `+` and `/` with `-` and `_` to ensure compatibility with URLs and file paths. Base64 is commonly used to encode data so that it can be safely transmitted over media that only support text.

### Why Use Base64?
Base64 encoding is useful in a variety of scenarios where binary data needs to be represented as text:

1. **Email Attachments**: 
   - In the MIME (Multipurpose Internet Mail Extensions) standard, binary data like images, documents, or other files in an email need to be converted into text. Since emails are typically transmitted as text, Base64 encoding ensures that all content, including binary attachments, remains intact across different email servers.

2. **Web Data Transmission**:
   - When binary data needs to be sent in HTTP headers, URLs, or cookies, which may not support arbitrary binary data, Base64 encoding ensures compatibility.

3. **Data Storage in Text Files**:
   - When storing binary data in JSON or XML files, encoding it in Base64 ensures that it remains compatible with text processing systems.

### How Does Base64 Work?
Base64 takes binary data and encodes it as text by breaking it down into 6-bit chunks:
1. Each 6-bit chunk is represented by a single ASCII character from the Base64 set (totaling 64 unique characters).
2. If the input length isn’t a multiple of 3 bytes, padding characters (`=`) are added to ensure the output length is divisible by 4.

### Example of Base64 Encoding:
Suppose you want to encode the text "Hello":
1. Convert "Hello" to binary: `01001000 01100101 01101100 01101100 01101111`.
2. Group the binary string into 6-bit chunks and map each chunk to a Base64 character.
3. The result is "SGVsbG8=" in Base64, which represents "Hello" as text-safe data.