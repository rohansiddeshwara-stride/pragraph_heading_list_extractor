import re
import statistics
import math
import fitz
import fitz
import statistics
import math
import re
import math

def drop_tables(blocks):
  new_blocks = []
  for block in blocks: #for each block

    if not re.search("[.]{3,}", block[2]):
      avg_space = []
      ideal_space = 25
      # print(block[7])
      if len(block[4]) == 1:
          new_blocks.append(block)

      for i in range(len(block[4]) - 1): # for each word in each block
        if math.floor(block[4][i][3]) == math.floor(block[4][i + 1][3]): #check if the consecutive words are in the same line.
          avg_space.append(abs(block[4][i][2] - block[4][i + 1][0]))

      if len(avg_space) != 0:
        block_avg_space = sum(avg_space)/ len(avg_space)

        if block_avg_space <= ideal_space or (len(block[4]) > 1 and len(avg_space) == 0):
          new_blocks.append(block)

  return new_blocks

def group_text_to_blocks(words):

  # Create a dictionary to group tuples by their second element
  grouped_dict = {}

  for tup in words:
      key = tup[5]  # Use the second element as the key
      if key in grouped_dict:
          grouped_dict[key].append(tup)
      else:
          # print(key)
          grouped_dict[key] = [tup]

  # Convert the dictionary values to a list of lists
  list_of_lists = list(grouped_dict.values())

  return list_of_lists

def get_font_info(lines):
  block_info = {}
  overall_font_size = []
  for block in lines:

    if "lines" in block:
      spans = block["lines"]
      font_type = []
      font_size = []
      lines_ = []
      for span in spans:
        data = span["spans"]
        for line in data:
          # print(line)
          font_type.append(line["font"])
          font_size.append(line["size"])
          lines_.append(line)
      font_type = statistics.mode(font_type)
      font_size = statistics.mean(font_size)
      # print(font_type, spans)
      overall_font_size.append(font_size)
      block_info[block["number"]] = [font_type, font_size, lines_]
  final = [block_info, overall_font_size]
  return final



def get_blocks(doc):
  blocks = []
  texts = []
  avg_font_size_ = []
  i = 0
  for i, page in enumerate(doc):
      block = page.get_text("blocks")
      text = page.get_text("words")
      lines = page.get_text("dict")["blocks"]
      # print(lines[0])
      # if "image" in lines.keys():
      #   break
      page = doc.load_page(i)
      pix = page.get_pixmap()

      text = group_text_to_blocks(text)
      font_info = get_font_info(lines)
      lines = font_info[0]
      font = font_info[1]
      avg_font_size_.extend(font)
      # print(lines)
      # lines, avg_font_size = get_font_info(lines)
      new_block = []
      j = 0
      # print(len())
      try:
        for x0, y0, x1, y1, t, b, _ in block:
          tt = t.replace('\n', " ")
          if t[:7] != "<image:" and not tt.isspace():
            #here
            # print(b, t, text[j])
            # print("////////////")
            new_block.append(((x0, y0, x1, y1),i, t, b, text[j], lines[b][0], lines[b][1],  lines[b][2], (pix.width, pix.height)))
            j+=1
      except:
        print("list index out of range error - due to presence of little graphical images")

      #new_block format ( 0 bbox, 1 page_no, 2 text, 3 block_no, 4 individual words,5 font type+style, 6 font size, 7 Lines, 8( page width, page height))
      blocks.extend(new_block)
  avg_font_size = statistics.mean(avg_font_size_)
  return blocks, avg_font_size

def get_block_bbox(word_bboxes):
  # print(word_bboxes)
  # Initialize variables to store min and max coordinates
  min_x, min_y = float('inf'), float('inf')
  max_x, max_y = float('-inf'), float('-inf')

  # Iterate through word bounding boxes to find min and max coordinates
  for x0, y0, x1, y1 in word_bboxes:
      min_x = min(min_x, x0)
      min_y = min(min_y, y0)
      max_x = max(max_x, x1)
      max_y = max(max_y, y1)
  return (min_x, min_y, max_x, max_y)

def get_paras_headings(blocks, avg_font_size):

  para = []
  heading = []
  for block in blocks: #for each block

      # print(block[2], block[2].isupper(),len(block[4]) > 5,block[5], block[2])
      if  not block[2].isupper() and len(block[4]) > 7 and not re.search("Bold", block[5]) and not re.search("^[•●○*◦▪▫■◆◘‣⁌❖⮞⬑➔⇒➢✓-]", block[2]):
        # check if the block doesnot contains text which is all upper and no of words in the block > 10 and if the text is not bold
        para.append(block)

      elif  (block[2].isupper() and block[6] > avg_font_size) or block[6] > avg_font_size  or re.search("Bold", block[5]) :
        # check if the block doesnot contains text which is all upper and no of words in the block > 10 and if the text is not bold
        heading.append(block)
  final = [para, heading]
  return final

def get_bullets(blocks):

  lines =  []
  new_blocks = []
  for block in blocks:
    # print(block[1], block[2])
    page_no = block[1]
    page_size = block[8]
    for b in block[7]:
      b["page_no"] = page_no
      b["page_size"] = page_size
      lines.append(b)
  # print(lines)

  text = ''
  line_no=0
  for line in lines:
    line_no+=1
    if not line["text"].isspace():
      if re.search("^[•●○*◦▪▫■◆◘‣⁌❖⮞⬑➔⇒➢✓-]", line["text"]):

        if text!='':
          new_blocks.append([get_block_bbox(bbox), page_no,text, line["page_size"]])

        text = ''
        bbox = []
        origin = []
        page_no = line["page_no"]
        o = (-50, -50)

        text+=line["text"]
        bbox.append(line["bbox"])
        origin.append(line["origin"])
        o = origin[0]
        # print(line["origin"], line["text"])

      elif text!='':
        # print(line["origin"], o[0], math.floor(o[0]) - 20<= math.floor(line["origin"][0]), math.floor(origin[-1][1]) + 20>= math.floor(line["origin"][1]),math.floor(o[0]) + 20>= math.floor(line["origin"][0]), line["text"])
        if line["page_no"] == page_no and ((math.floor(o[1]) == math.floor(line["origin"][1]))or ((math.floor(o[0]) + 10<= math.floor(line["origin"][0]))and (math.floor(o[0]) + 20>= math.floor(line["origin"][0])) and ( math.floor(origin[-1][1]) + 20>= math.floor(line["origin"][1])))):

            origin.append(line["origin"])
            # o = origin[1]
            text+= ' ' + line["text"]
            bbox.append(line["bbox"])

        else:
          new_blocks.append([get_block_bbox(bbox), page_no,text, line["page_size"]])
          text = ''
          bbox = []
          origin = []
      if line_no == len(lines) and text!='':
        new_blocks.append([get_block_bbox(bbox), page_no,text, line["page_size"]])

  return new_blocks

def get_numbered_list(blocks):

  lines =  []
  new_blocks = []
  for block in blocks:
    # print(block[1], block[2])
    page_no = block[1]
    page_size = block[8]
    for b in block[7]:
      b["page_no"] = page_no
      b["page_size"] = page_size
      lines.append(b)

  text = ''
  line_no = 0
  for line in lines:
    # print(line)
    line_no+=1
    if not line["text"].isspace():
      if re.search("^(((M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))&(\.|\ ))|([0-9]{1,2}\.|[a-zA-Z]\.\ |\(\ ?[a-zA-Z]\ ?\))|((m{0,4}(cm|cd|d?c{0,3})(xc|xl|l?X{0,3})(ix|iv|v?i{0,3}))&(\.|\ ))|[0-9])", line["text"]) :
        if text!='':
          new_blocks.append([get_block_bbox(bbox), page_no,text, line["page_size"]])

        text = ''
        bbox = []
        origin = []
        page_no = line["page_no"]
        o = (-50, -50)

        text+=line["text"]
        bbox.append(line["bbox"])
        origin.append(line["origin"])
        o = origin[0]

      elif text!='':
        if line["page_no"] == page_no and ((math.floor(o[1]) == math.floor(line["origin"][1]))or ((math.floor(o[0]) + 10<= math.floor(line["origin"][0]))and (math.floor(o[0]) + 20>= math.floor(line["origin"][0])) and ( math.floor(origin[-1][1]) + 20>= math.floor(line["origin"][1])))):
# check if the two lines are in same page and the new lines y origin matches with the previos lines y origin
# or if the new line is indented within a range of the previous line
            origin.append(line["origin"])
            # o = origin[1]
            text+= ' ' + line["text"]
            bbox.append(line["bbox"])

        else:
          new_blocks.append([get_block_bbox(bbox), page_no,text, line["page_size"]])
          text = ''
          bbox = []
          origin = []
      if line_no == len(lines) and text!='':
        new_blocks.append([get_block_bbox(bbox), page_no,text, line["page_size"]])

  return new_blocks


def cal_area(bbox):

  width = abs(bbox[2]- bbox[0])
  height = abs(bbox[3]- bbox[1])
  area = width*height

  return area

def filter_overlap(list_one, list_two):
  result = [item for item in list_one if item not in list_two]
  return result

def do_bboxes_overlap(box1, box2):
    # Extract coordinates of the first box
    x1a, y1a, x2a, y2a = box1
    # Extract coordinates of the second box
    x1b, y1b, x2b, y2b = box2

    # Calculate the area of the first box
    area1 = (x2a - x1a) * (y2a - y1a)
    # Calculate the area of the second box
    area2 = (x2b - x1b) * (y2b - y1b)

    # Calculate the coordinates of the intersection rectangle
    x_intersection = max(0, min(x2a, x2b) - max(x1a, x1b))
    y_intersection = max(0, min(y2a, y2b) - max(y1a, y1b))

    # Calculate the area of the intersection rectangle
    intersection_area = x_intersection * y_intersection

    # Calculate the percentage of overlap
    overlap_percentage = (intersection_area / min(area1, area2)) * 100

    # Return True if overlap percentage is above 75%, otherwise return False
    return overlap_percentage > 75


def remove_para_headings(paragraphs, headings, target_list):
  non_para = []
  non_head = []
  non_target = []

  for each_block in target_list:
    for each_para in paragraphs:
      if do_bboxes_overlap(each_block[0], each_para[0]):

        bullet_area = cal_area(each_block[0])
        para_area = cal_area(each_para[0])
        diff = para_area - bullet_area

        if diff <= 100:
          #if difference in area is too much then its 
          non_para.append(each_para)
          # print("np", each_para[2])
        else:
          non_target.append(each_block)
          # print("nb", each_block[2])


  for each_block in target_list:
    for each_head in headings:
      if do_bboxes_overlap(each_block[0], each_head[0]):

        # bullet_area = cal_area(each_block[0])
        # para_area = cal_area(each_head[0])
        # diff = para_area - bullet_area
        # if abs(diff) > = 100:
        non_target.append(each_block)
          # print("nbh",diff, each_block[2], each_head[2])
        # else:
        # non_head.append(each_head)
          # print("nh",diff, each_block[2], each_head[2])

  para = filter_overlap(paragraphs, non_para)
  head = filter_overlap(headings, non_head)
  target = filter_overlap(target_list, non_target)
  # print(head)

  return [para, head, target]

def postprocessing(paragraphs, headings, bullets, numbered, no_of_pages):

  paragraphs_new = []
  headings_new = []
  bullets_new = []
  numbered_new = []

  for i in range(no_of_pages):
    para = [x for x in paragraphs if x[1] == i]
    head = [x for x in headings if x[1] == i]
    bullet = [x for x in bullets if x[1] == i]
    num = [x for x in numbered if x[1] == i]
    paragraphs_new_temp, headings_new_temp, bullets_new_temp = remove_para_headings(para,head,bullet)
    paragraphs_new_temp, headings_new_temp, numbered_new_temp = remove_para_headings(paragraphs_new_temp,headings_new_temp,num)
    paragraphs_new.extend(paragraphs_new_temp)
    headings_new.extend(headings_new_temp)
    bullets_new.extend(bullets_new_temp)
    numbered_new.extend(numbered_new_temp)
  # print(len(paragraphs_new),len(headings_new),len(bullets_new),len(numbered_new))

  final = [paragraphs_new, headings_new, bullets_new, numbered_new]
  return final

def combine_structurally(target, no_of_pages):

  combined_target = [[target[0]]]
  i = 0
  for each_line in target[1:]:
    if math.floor(each_line[0][0]) == math.floor(combined_target[-1][-1][0][0]) and each_line[1] == combined_target[-1][-1][1] and (each_line[0][1] - combined_target[-1][-1][0][3]) <=5:
      #check if two blocks are in same page and if they have the same x0 and if the difference between
      # the y1 of first block and y0 of second block is below some threshold
      combined_target[i].append(each_line)
    else:
      i+=1
      combined_target.append([each_line])

  new_block = []
  for each_line in combined_target:

    text = '\n'.join(item[2] for item in each_line)
    bboxs = [item[0] for item in each_line]
    final_bbox = get_block_bbox(bboxs)
    page_no = each_line[0][1]
    page_size = each_line[0][3]
    new_block.append([final_bbox, page_no, text, page_size])

  return new_block

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