from Extractor import extract_para_head_bullet_num

doc_path = "test.pdf"
block = extract_para_head_bullet_num(doc_path)
print(block)