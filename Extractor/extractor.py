import fitz

from Extractor.helpers import drop_tables, get_blocks,get_paras_headings
from Extractor.helpers import get_bullets, get_numbered_list, postprocessing, get_json

def extract_para_head_bullet_num(doc_path):
    doc_path = doc_path
    doc = fitz.open(doc_path)

    blocks, avg_font_size = get_blocks(doc)
    non_table_blocks = drop_tables(blocks)
    para_heading_detections = get_paras_headings(non_table_blocks,avg_font_size)
    paragraphs = para_heading_detections[0]
    headings = para_heading_detections[1]

    bullets = get_bullets(blocks)
    numbered = get_numbered_list(blocks)

    final = postprocessing(paragraphs, headings, bullets, numbered, len(doc))
    paragraphs = final[0]
    headings = final[1]

    bullets = final[2]
    numbered = final[3]
    final_blocks = get_json(headings, paragraphs, bullets, numbered)

    return final_blocks



