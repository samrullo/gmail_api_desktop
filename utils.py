def get_chunked_list(original_list, chunk_size):
    chunked_list = [original_list[i:i + chunk_size] for i in range(0, len(original_list), chunk_size)]
    return chunked_list
