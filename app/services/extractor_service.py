# from bs4 import BeautifulSoup
# import re
# from collections import defaultdict
#
# def extract_questions_from_html(html: str):
#     try:
#         print("Extraction started")
#
#         soup = BeautifulSoup(html, 'html.parser')
#         all_elements = soup.body.find_all(True)
#         elements = [elem for elem in soup.find_all(True) if len(elem.find_all(True)) == 0]
#
#         question_dict = defaultdict(list)
#         option_dict = defaultdict(dict)
#
#         current_qn = None
#         option_pattern = re.compile(r'^([a-dA-D]\.|\([a-dA-D]\))')  # Matches (a), (A), etc.
#         option_f = False
#         quetion_f = False
#         current_o = None
#         for elem in elements:
#             text = elem.get_text(strip=True)
#             # Match question number (e.g., 1. or 10.)
#             question_match = re.match(r'^(\d+)\.', text)
#             if question_match:
#                 current_qn = question_match.group(1)
#                 question_dict[current_qn].append(str(elem))
#                 option_f = False
#                 question_f = True
#                 continue
#
#             # If question already started
#             if current_qn:
#                 opt_match = option_pattern.match(text)
#                 if opt_match:
#                     current_o = opt_match.group().lower().strip('()')
#                     option_dict[current_qn][current_o] = [str(elem)]
#                     question_f = False
#                     option_f = True
#                     continue
#                 if option_f:
#                     option_dict[current_qn][current_o].append(str(elem))
#                     continue
#                 if question_f:
#                     question_dict[current_qn].append(str(elem))
#                     continue
#
#
#
#         # Output example
#         questions=[]
#         for qn in question_dict:
#             questions.append({
#                 "question": "\n".join(question_dict[qn]),
#                 "options": option_dict[qn],
#                 "correct_option": "A",
#             })
#             print(questions[-1])
#         return questions
#     except(Exception) as e:
#         print(e)
