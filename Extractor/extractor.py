import fitz

from Extractor.helpers import drop_tables, get_blocks,get_paras_headings
from Extractor.helpers import get_bullets, get_numbered_list, postprocessing, get_json, combine_structurally

def extract_para_head_bullet_num(doc_path):
  doc_path = doc_path
  doc = fitz.open(doc_path)
  no_of_pages = len(doc)
  blocks, avg_font_size = get_blocks(doc)
  non_table_blocks = drop_tables(blocks)
  para_heading_detections = get_paras_headings(non_table_blocks,avg_font_size)
  paragraphs = para_heading_detections[0]
  headings = para_heading_detections[1]

  bullets = get_bullets(blocks)
  numbered = get_numbered_list(blocks)

  combined_bullets = combine_structurally(bullets, no_of_pages)
  combined_numbered = combine_structurally(numbered, no_of_pages)

  final = postprocessing(paragraphs, headings, combined_bullets, combined_numbered, no_of_pages)
  paragraphs = final[0]
  headings = final[1]

  bullets = final[2]
  numbered = final[3]
  final_blocks = get_json(headings, paragraphs, bullets, numbered)

  return final_blocks