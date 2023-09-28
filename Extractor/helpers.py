import re
import statistics
import math
import fitz
import fitz
import statistics
import math
def get_json(headings, paras, bullets, nums):

  para = []
  for x in paras:
    para_json = {
                "bbox" : x[0],
                "text" : x[2],
                "page_no" : x[1],
                "font_type" : x[5],
                "font_size" : x[6],
                "page_size" : x[8]

    }
    para.append(para_json)

  heading = []
  for x in headings:
    heading_json = {
                "bbox" : x[0],
                "text" : x[2],
                "page_no" : x[1],
                "font_type" : x[5],
                "font_size" : x[6],
                "page_size" : x[8]

    }
    heading.append(heading_json)

  bullet = []
  for x in bullets:
    bullet_json = {
                "bbox" : x[0],
                "text" : x[2],
                "page_no" : x[1],
                "page_size" : x[3]
    }
    bullet.append(bullet_json)

  num = []
  for x in nums:
    # print(x[1], x[2])
    num_json = {
                "bbox" : x[0],
                "text" : x[2],
                "page_no" : x[1],
                "page_size" : x[3]
    }
    num.append(num_json)

  final_list = {
                "heading" : heading,
                "paragraph" : para,
                "bullet_list" :bullet,
                "numbered_list" : num
                }

  return final_list